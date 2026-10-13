#!/usr/bin/env python3
"""Adjudicate saved outputs from bytes/DB/receipts; never rerun the workflow."""
import argparse,hashlib,json,sqlite3
from pathlib import Path
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify(run,out):
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists():raise RuntimeError('refuse to overwrite adjudication')
    rows=[]
    for fault in ['none','foreign-result','checkpoint-corrupt','retry-unsafe','broken-link','numerical-failure']:
        case=run/fault;rc=load(case/'run.receipt.json')['exit_code'];b=case/'outputs/bundle'
        if fault=='checkpoint-corrupt':
            rejects=[load(x) for x in (case/'tmp').rglob('resume-receipt.json')]
            ok=rc!=0 and not b.exists() and any(x.get('exit_code')==22 and x['checks']==
              {'input':True,'experiment':True,'checkpoint_bytes':False,'code':True,'state_index':True} for x in rejects)
            observed={'workflow_rc':rc,'actual_rejections':rejects}
        else:
            result=load(b/'result.json');report=load(b/'evaluation-report.json');receipt=load(b/'resume-receipt.json');index=load(b/'evidence-index.json');boundary=load(b/'boundary.json')
            with sqlite3.connect('file:'+str((b/'effects.db').resolve())+'?mode=ro',uri=True) as c:db_rows=c.execute('SELECT count(*) FROM effects').fetchone()[0]
            expected_checks={'input_binding':fault!='foreign-result','experiment_binding':fault!='foreign-result',
               'producer_result_binding':True,'checkpoint_binding':True,'side_effect_idempotency':fault!='retry-unsafe'}
            artifact_hashes=all(sha(b/n)==h for n,h in index['artifacts'].items())
            ok=rc==0 and report['checks']==expected_checks and result['value']==(0 if fault=='numerical-failure' else 767)
            ok=ok and db_rows==(2 if fault=='retry-unsafe' else 1) and [x['exit_code'] for x in receipt['effect_attempts']]==[75,0]
            ok=ok and receipt['result_sha256']==sha(b/'result.json')==report['subject_result_sha256'] and artifact_hashes
            ok=ok and ((index['links']['evaluation_subject_result_sha256']==sha(b/'result.json'))==(fault!='broken-link'))
            ok=ok and boundary['real_scientific_status']=='NOT_EVALUATED'
            ok=ok and ((boundary['claim_disposition']=='RECORD_SCOPED_FIXTURE')==(fault=='none'))
            observed={'workflow_rc':rc,'value':result['value'],'DB_rows_directly_read':db_rows,
                'report_check_axes':report['checks'],'all_retained_artifact_digests_match':artifact_hashes,
                'evaluation_report_subject_binds_actual_result':report['subject_result_sha256']==sha(b/'result.json'),
                'index_link_binds_actual_result':index['links']['evaluation_subject_result_sha256']==sha(b/'result.json')}
        rows.append({'scenario':fault,'raw_evidence_expectation_met':ok,'observed':observed})
    obj={'checks':rows,'expectations_met':sum(x['raw_evidence_expectation_met'] for x in rows),'total':6,
      'workflow_rerun':False,'independent_author_review':False}
    out.write_text(json.dumps(obj,indent=2)+'\n');print(json.dumps({'expectations_met':obj['expectations_met'],'total':6}))
    return 0 if obj['expectations_met']==6 else 1
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--run',required=True);p.add_argument('--out',required=True);a=p.parse_args();raise SystemExit(verify(Path(a.run),Path(a.out)))
