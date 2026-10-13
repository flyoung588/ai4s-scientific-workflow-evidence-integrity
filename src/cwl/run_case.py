#!/usr/bin/env python3
"""Generate/run only the bounded real CWL integration scenarios; preserve failures."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p,x):Path(p).write_text(json.dumps(x,sort_keys=True,indent=2)+'\n')
def load(p):return json.loads(Path(p).read_text())
def generate():
    tools=ROOT/'workflow';tools.mkdir(exist_ok=True)
    specs={
      'checkpoint':({'input':'File','contract':'File','fault':'string'},['checkpoint.json','anchor.json','checkpoint-receipt.json']),
      'resume':({'input':'File','contract':'File','fault':'string','checkpoint':'File','anchor':'File'},['result.json','resume-receipt.json','attempt-spans.json','effects.db']),
      'evaluate':({'input':'File','contract':'File','fault':'string','result':'File','receipt':'File','evaluator':'File'},['evaluation-report.json','evaluation-receipt.json']),
      'package':({'input':'File','contract':'File','fault':'string','checkpoint':'File','anchor':'File','checkpoint-receipt':'File',
          'result':'File','receipt':'File','report':'File','evaluation-receipt':'File','spans':'File','database':'File'},['bundle'])}
    keys={}
    for mode,(ins,outs) in specs.items():
        allinputs={'python':{'type':'string','inputBinding':{'position':0}},'program':{'type':'File','inputBinding':{'position':1}}}
        for i,(k,t) in enumerate(ins.items(),3):allinputs[k]={'type':t,'inputBinding':{'position':i,'prefix':'--'+k}}
        outputs={n.replace('.','_').replace('-','_'):{'type':'Directory' if n=='bundle' else 'File','outputBinding':{'glob':n}} for n in outs}
        keys[mode]=list(outputs)
        put(tools/(mode+'.cwl'),{'cwlVersion':'v1.2','class':'CommandLineTool','inputs':allinputs,
           'arguments':[{'position':2,'valueFrom':mode}], 'outputs':outputs,
           'stdout':mode+'.stdout','stderr':mode+'.stderr','successCodes':[0],
           'permanentFailCodes':[22] if mode=='resume' else [],
           'requirements':{'NetworkAccess':{'networkAccess':False}}})
    common={'python':'python','program':'program','input':'input','contract':'contract','fault':'fault'}
    wf={'cwlVersion':'v1.2','class':'Workflow','inputs':{'python':'string','program':'File','evaluator':'File','input':'File','contract':'File','fault':'string'},
        'outputs':{'bundle':{'type':'Directory','outputSource':'package/bundle'}},'steps':{}}
    def step(name,ins):wf['steps'][name]={'run':name+'.cwl','in':ins,'out':keys[name]}
    step('checkpoint',common)
    step('resume',dict(common,checkpoint='checkpoint/checkpoint_json',anchor='checkpoint/anchor_json'))
    step('evaluate',dict(common,result='resume/result_json',receipt='resume/resume_receipt_json',evaluator='evaluator'))
    step('package',dict(common,checkpoint='checkpoint/checkpoint_json',anchor='checkpoint/anchor_json',
        **{'checkpoint-receipt':'checkpoint/checkpoint_receipt_json','evaluation-receipt':'evaluate/evaluation_receipt_json'},
        result='resume/result_json',receipt='resume/resume_receipt_json',report='evaluate/evaluation_report_json',
        spans='resume/attempt_spans_json',database='resume/effects_db'))
    put(tools/'workflow.cwl',wf)
def main(out):
    out.mkdir(parents=True,exist_ok=False)
    data={'a':3,'x0':7,'modulus':997,'data':list(range(1,21))};put(out/'input.json',data)
    put(out/'contract.json',{'experiment':'synthetic-experiment-A','origin':'SYNTHETIC_FIXTURE',
      'input_sha256':sha(out/'input.json'),'worker_sha256':sha(ROOT/'worker.py'),
      'evaluator_sha256':sha(ROOT/'evaluator.py'),'criterion':'exact integer equality AND explicit local evidence checks',
      'real_scientific_claim':'NOT_EVALUATED','independence':'same author; no independent data/reviewer'})
    exe=str(Path(sys.executable).with_name('cwltool'))
    validate=subprocess.run([exe,'--validate',str(ROOT/'workflow/workflow.cwl')],capture_output=True,text=True,timeout=30)
    put(out/'workflow-validation.receipt.json',{'command':[exe,'--validate',str(ROOT/'workflow/workflow.cwl')],
       'exit_code':validate.returncode,'stdout':validate.stdout,'stderr':validate.stderr})
    if validate.returncode:print(validate.stderr);return 1
    scenarios=['none','foreign-result','checkpoint-corrupt','retry-unsafe','broken-link','numerical-failure']
    results=[]
    for fault in scenarios:
        case=out/fault;case.mkdir();(case/'outputs').mkdir();(case/'tmp').mkdir()
        job={'python':sys.executable,'program':{'class':'File','path':str(ROOT/'worker.py')},
          'evaluator':{'class':'File','path':str(ROOT/'evaluator.py')},'input':{'class':'File','path':str(out/'input.json')},
          'contract':{'class':'File','path':str(out/'contract.json')},'fault':fault}
        put(case/'job.json',job)
        cmd=[exe,'--no-container','--leave-tmpdir','--outdir',str(case/'outputs'),
             '--tmp-outdir-prefix',str(case/'tmp')+'/',str(ROOT/'workflow/workflow.cwl'),str(case/'job.json')]
        started=time.time();r=subprocess.run(cmd,capture_output=True,text=True,timeout=45)
        put(case/'run.receipt.json',{'command':cmd,'exit_code':r.returncode,'start_unix':started,'end_unix':time.time(),
           'stdout':r.stdout,'stderr':r.stderr,'no_container':True,'fault_is_controlled':fault!='none'})
        bundle=case/'outputs/bundle';boundary=load(bundle/'boundary.json') if (bundle/'boundary.json').exists() else None
        if fault=='checkpoint-corrupt':
            receipts=[load(p) for p in (case/'tmp').rglob('resume-receipt.json')]
            ok=r.returncode!=0 and any(x.get('execution')=='REJECTED' and x.get('checks',{}).get('checkpoint_bytes') is False for x in receipts)
            actual={'workflow_rc':r.returncode,'resume_rejections':receipts,'downstream_bundle_exists':bundle.exists()}
        else:
            ok=r.returncode==0 and boundary is not None
            if ok:
                if fault=='none':ok=boundary['claim_disposition']=='RECORD_SCOPED_FIXTURE'
                elif fault=='broken-link':ok=boundary['linkage']=='REJECTED_LINKAGE'
                elif fault=='numerical-failure':ok=boundary['fixture_numeric_status']=='FAILED_FIXTURE' and boundary['claim_disposition']=='WITHHOLD_FIXTURE_CLAIM'
                else:ok=boundary['evidence_integrity']=='REJECTED_BINDING_OR_EFFECT'
            actual={'workflow_rc':r.returncode,'boundary':boundary}
        row={'scenario':fault,'expectation_met':ok,'actual':actual};results.append(row);put(case/'expectation.json',row)
        print(fault,'workflow_rc',r.returncode,'expectation_met',ok,flush=True)
    put(out/'summary.json',{'scenarios':results,'expectations_met':sum(r['expectation_met'] for r in results),
       'total':len(results),'workflow_engine':'ACTUAL_CWLTOOL','argo_k8s':'NOT_TESTED','science':'SYNTHETIC_ONLY',
       'external_contact':'HOLD_NOT_SENT','independent_review':'NOT_PERFORMED'})
    put(out/'hashes.json',{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='hashes.json'})
    return 0 if all(r['expectation_met'] for r in results) else 1
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--generate',action='store_true');ap.add_argument('--out');a=ap.parse_args()
    if a.generate:generate();sys.exit(0)
    sys.exit(main(Path(a.out).resolve()))
