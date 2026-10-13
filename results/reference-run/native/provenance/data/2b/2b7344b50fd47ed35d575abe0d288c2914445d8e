#!/usr/bin/env python3
"""CWL stage tools. Synthetic experiment; local subprocess/SQLite/OTel/RO-Crate."""
import argparse, hashlib, json, os, select, sqlite3, subprocess, sys, time
from pathlib import Path
from tenacity import retry, stop_after_attempt, retry_if_exception_type
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())
def put(p,v):
    tmp=Path(str(p)+'.tmp');tmp.write_text(json.dumps(v,sort_keys=True,indent=2)+'\n')
    with tmp.open('rb') as f:os.fsync(f.fileno())
    os.replace(tmp,p)
def calc(d,start=0,value=None,end=None):
    x=d['x0'] if value is None else value
    for v in d['data'][start:end]:x=(d['a']*x+v)%d['modulus']
    return x
def child_checkpoint(a):
    d=read(a.input);c=read(a.contract)
    put('checkpoint.json',{'index':8,'state':calc(d,end=8),'experiment':c['experiment'],
       'input_sha256':sha(a.input),'worker_sha256':sha(__file__),'producer_attempt':'compute-attempt-1'})
    print('CHECKPOINT_WRITTEN',flush=True)
    time.sleep(30)
def checkpoint(a):
    cmd=[sys.executable,str(Path(__file__).resolve()),'child-checkpoint','--input',a.input,'--contract',a.contract]
    p=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    if not select.select([p.stdout],[],[],5)[0]:p.kill();p.communicate();raise RuntimeError('checkpoint handshake timeout')
    first=p.stdout.readline();put('anchor.json',{'checkpoint_sha256':sha('checkpoint.json'),
       'experiment':read(a.contract)['experiment'],'input_sha256':sha(a.input),
       'producer_attempt':'compute-attempt-1','reference_origin':'LOCAL_PRE_MUTATION_ANCHOR_NOT_SIGNATURE'})
    p.terminate();out,err=p.communicate(timeout=5)
    put('checkpoint-receipt.json',{'command':cmd,'exit_code':p.returncode,'stdout':first+out,'stderr':err,
       'controlled_interruption':True,'science_origin':'SYNTHETIC_FIXTURE','fault':a.fault})
    if a.fault=='checkpoint-corrupt':
        cp=read('checkpoint.json');cp['state']+=1;put('checkpoint.json',cp)
    if p.returncode!=-15:raise RuntimeError('expected actual SIGTERM termination')
def effect(a):
    d=read(a.contract);key=hashlib.sha256((d['experiment']+d['input_sha256']+'logical-effect').encode()).hexdigest()
    con=sqlite3.connect('effects.db');con.execute('CREATE TABLE IF NOT EXISTS effects(effect_key TEXT)')
    if a.fault!='retry-unsafe':con.execute('CREATE UNIQUE INDEX IF NOT EXISTS one_logical_effect ON effects(effect_key)')
    con.execute(('INSERT INTO' if a.fault=='retry-unsafe' else 'INSERT OR IGNORE INTO')+' effects VALUES (?)',(key,));con.commit();con.close()
    put('effect-attempt-'+a.attempt+'.json',{'attempt':a.attempt,'effect_key':key,'commit_completed':True,
       'lost_ack_after_commit':a.attempt=='1'})
    print('COMMIT_COMPLETED_ACK_'+('LOST' if a.attempt=='1' else 'RETURNED'),flush=True)
    return 75 if a.attempt=='1' else 0
def resume(a):
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import SimpleSpanProcessor
    from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
    from opentelemetry.trace import Status,StatusCode
    c=read(a.contract);cp=read(a.checkpoint);anchor=read(a.anchor)
    checks={'input':sha(a.input)==c['input_sha256']==cp['input_sha256']==anchor['input_sha256'],
            'experiment':cp['experiment']==c['experiment']==anchor['experiment'],
            'checkpoint_bytes':sha(a.checkpoint)==anchor['checkpoint_sha256'],
            'code':cp['worker_sha256']==sha(__file__)==c['worker_sha256'],
            'state_index':0<=cp['index']<=len(read(a.input)['data'])}
    if not all(checks.values()):
        put('resume-receipt.json',{'execution':'REJECTED','checks':checks,'exit_code':22,
             'scientific_status':'NOT_EVALUATED','fault':a.fault})
        return 22
    exporter=InMemorySpanExporter();provider=TracerProvider(shutdown_on_exit=False)
    provider.add_span_processor(SimpleSpanProcessor(exporter));events=[]
    @retry(stop=stop_after_attempt(2),retry=retry_if_exception_type(OSError),reraise=True)
    def retry_effect():
        n=str(len(events)+1)
        cmd=[sys.executable,str(Path(__file__).resolve()),'effect','--contract',a.contract,'--attempt',n,'--fault',a.fault]
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=5)
        events.append({'attempt':n,'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
        if r.returncode==75:raise OSError('controlled post-commit acknowledgement loss')
        if r.returncode:raise RuntimeError('unexpected effect error')
    with provider.get_tracer('p1b.workflow').start_as_current_span('resume-and-effect') as span:
        span.set_attribute('experiment.id',c['experiment']);span.set_attribute('attempt.id','compute-attempt-2')
        value=calc(read(a.input),cp['index'],cp['state'])
        retry_effect();span.set_status(Status(StatusCode.OK))
    provider.force_flush();put('attempt-spans.json',[json.loads(s.to_json()) for s in exporter.get_finished_spans()]);provider.shutdown()
    with sqlite3.connect('effects.db') as con:n=con.execute('SELECT count(*) FROM effects').fetchone()[0]
    result={'value':0 if a.fault=='numerical-failure' else value,'experiment':c['experiment'],
         'input_sha256':sha(a.input),'checkpoint_sha256':sha(a.checkpoint),'attempt':'compute-attempt-2',
         'parent_attempt':cp['producer_attempt'],'origin':'SYNTHETIC_FIXTURE'}
    if a.fault=='foreign-result':result['experiment']='foreign-experiment';result['input_sha256']='0'*64
    put('result.json',result)
    put('resume-receipt.json',{'execution':'COMPLETED','checks':checks,'effect_attempts':events,'effect_count':n,
         'result_sha256':sha('result.json'),'checkpoint_sha256':sha(a.checkpoint),'fault':a.fault,
         'scientific_status':'NOT_DECIDED_BY_WORKER'})
    return 0
def evaluate(a):
    c=read(a.contract)
    if sha(a.evaluator)!=c['evaluator_sha256']:raise RuntimeError('evaluator code binding mismatch')
    cmd=[sys.executable,a.evaluator,a.input,a.contract,a.result,a.receipt]
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=5)
    put('evaluation-receipt.json',{'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr,
       'evaluator_sha256':sha(a.evaluator)})
    if r.returncode:raise RuntimeError('evaluation tool execution failed')
    put('evaluation-report.json',json.loads(r.stdout))
def package(a):
    from rocrate.rocrate import ROCrate
    from rocrate.model.contextentity import ContextEntity
    mapping={'input.json':a.input,'contract.json':a.contract,'checkpoint.json':a.checkpoint,'anchor.json':a.anchor,
         'checkpoint-receipt.json':a.checkpoint_receipt,'result.json':a.result,'resume-receipt.json':a.receipt,
         'evaluation-report.json':a.report,'evaluation-receipt.json':a.evaluation_receipt,'attempt-spans.json':a.spans,
         'effects.db':a.database}
    crate=ROCrate();crate.name='Synthetic workflow integrity case';crate.description='Actual CWL execution; not real scientific validation.'
    for name,path in mapping.items():crate.add_file(path,dest_path=name)
    for stage,inputs,outputs in [
       ('checkpoint',['input.json','contract.json'],['checkpoint.json','anchor.json','checkpoint-receipt.json']),
       ('resume',['input.json','contract.json','checkpoint.json','anchor.json'],['result.json','resume-receipt.json','attempt-spans.json','effects.db']),
       ('evaluation',['input.json','contract.json','result.json','resume-receipt.json'],['evaluation-report.json','evaluation-receipt.json'])]:
        tool=crate.add(ContextEntity(crate,'#tool-'+stage,properties={'@type':'SoftwareApplication','name':stage}))
        act=crate.add(ContextEntity(crate,'#action-'+stage,properties={'@type':'CreateAction','instrument':tool,
             'object':[{'@id':n} for n in inputs],'result':[{'@id':n} for n in outputs],
             'actionStatus':{'@id':'http://schema.org/CompletedActionStatus'},
             'description':'Tool wrapper completed; checkpoint wrapper records its intentionally interrupted child separately.'}))
        crate.root_dataset.append_to('mentions',act)
    crate.write('bundle')
    refs={n:sha(Path('bundle')/n) for n in mapping}
    links={'evaluation_subject_result_sha256':read(a.report)['subject_result_sha256'],
           'producer_result_sha256':read(a.receipt)['result_sha256']}
    if a.fault=='broken-link':links['evaluation_subject_result_sha256']='f'*64
    put('bundle/evidence-index.json',{'artifacts':refs,'links':links,'origin':'SYNTHETIC_FIXTURE',
          'authority':'LOCAL_RECORDS_NOT_SIGNED','telemetry_is_not_sole_link':True})
    ok=links['evaluation_subject_result_sha256']==refs['result.json']==links['producer_result_sha256']
    report=read(a.report)
    put('bundle/boundary.json',{'execution':'COMPLETED','linkage':'VERIFIED_LOCAL' if ok else 'REJECTED_LINKAGE',
          'fixture_numeric_status':report['numeric_status'],'evidence_integrity':report['integrity_status'],
          'claim_disposition':report['claim_disposition'] if ok else 'WITHHOLD_INVALID_EVIDENCE_LINK',
          'real_scientific_status':'NOT_EVALUATED','extra_resources_authorized':False,'fault':a.fault})
def main():
    p=argparse.ArgumentParser();p.add_argument('mode')
    for x in ['input','contract','fault','checkpoint','anchor','result','receipt','evaluator','report','spans','database','checkpoint-receipt','evaluation-receipt','attempt']:
        p.add_argument('--'+x,default='none' if x=='fault' else None)
    a=p.parse_args()
    if a.mode=='effect':return effect(a)
    if a.mode=='resume':return resume(a)
    {'child-checkpoint':child_checkpoint,'checkpoint':checkpoint,'evaluate':evaluate,'package':package}[a.mode](a)
    return 0
if __name__=='__main__':sys.exit(main())
