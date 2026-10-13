#!/usr/bin/env python3
"""Bounded adversarial study: real local components, synthetic scientific inputs.
Run with the pinned environment: python research.py --out NEW_DIRECTORY
No network, container, model, XREM runtime, or external publication.
"""
import argparse
import copy
import functools
import hashlib
import importlib.metadata as md
import inspect
import json
import os
from pathlib import Path
import platform
import random
import select
import shutil
import sqlite3
import subprocess
import sys
import time
from tenacity import retry, stop_after_attempt, retry_if_exception_type
from opentelemetry.sdk.trace import TracerProvider, SpanLimits
from opentelemetry.sdk.trace.sampling import ALWAYS_OFF, ALWAYS_ON
from opentelemetry.sdk.trace.export import SimpleSpanProcessor
from opentelemetry.sdk.trace.export.in_memory_span_exporter import InMemorySpanExporter
from opentelemetry.trace import Status, StatusCode
from rocrate.rocrate import ROCrate
from rocrate.model.contextentity import ContextEntity

BASELINE = Path(__file__).resolve().parent / 'baseline'
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def dump(p,x): Path(p).write_text(json.dumps(x,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
def load(p): return json.loads(Path(p).read_text())
def oracle(d):
    n=len(d['data']);a=d['a'];m=d['modulus']
    return (pow(a,n,m)*d['x0']+sum(pow(a,n-i-1,m)*v for i,v in enumerate(d['data'])))%m

def main(out):
    out.mkdir(parents=True,exist_ok=False)
    records=[];processes=[]
    def check(name, ok, observed, boundary, kind='REAL_COMPONENT_SYNTHETIC_INPUT'):
        row={'id':name,'expectation_met':bool(ok),'observed':observed,'scope_limit':boundary,'evidence_class':kind}
        records.append(row);dump(out/(name+'.json'),row)
    def proc(name,args):
        started=time.time();p=subprocess.run(args,capture_output=True,text=True,timeout=10)
        row={'id':name,'command':args,'start_unix':started,'end_unix':time.time(),
             'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
        processes.append(row);dump(out/(name+'.process.json'),row);return p
    inp=out/'input.json';d={'a':3,'x0':7,'modulus':997,'data':list(range(1,21))};dump(inp,d)
    # Predeclared contract and trusted local reference hashes before adversarial edits.
    dump(out/'contract.json',{'origin':'SYNTHETIC_FIXTURE','scientific_scope':'integer equality only',
         'experiment':'experiment-A','input_sha256':sha(inp),'comparison':'closed-form exact equality',
         'tests':'binding, corruption, hidden dependency, idempotency, sampling, attribute loss, crate packing',
         'independence':'same author; distinct algorithms only; no external independent review'})
    oldeval=BASELINE/'evaluate.py';oldworker=BASELINE/'case.py'
    foreign=out/'foreign-result.json';dump(foreign,{'value':oracle(d),'experiment':'foreign-experiment',
        'input_sha256':'0'*64,'attempt':'foreign-attempt'})
    r=proc('old-evaluator-foreign',[sys.executable,str(oldeval),str(inp),str(foreign)])
    check('C01_old_evaluator_accepts_foreign_binding',r.returncode==0 and json.loads(r.stdout)['status']=='SUPPORTED',
          {'old_evaluation':json.loads(r.stdout),'binding_matches':False},
          'Observed weakness in our old fixture: numerical equality does not validate experiment/input provenance.')
    def bound_evaluate(result, expected_experiment, input_path):
        v=load(result)
        if v.get('experiment')!=expected_experiment or v.get('input_sha256')!=sha(input_path):
            return {'status':'UNQUALIFIED_BINDING','scientific_status':'NOT_EVALUATED'}
        return {'status':'SUPPORTED' if v['value']==oracle(load(input_path)) else 'FAILED',
                'scientific_status':'SYNTHETIC_NUMERICAL_ONLY'}
    guarded=bound_evaluate(foreign,'experiment-A',inp)
    check('C02_binding_guard_rejects_foreign',guarded['status']=='UNQUALIFIED_BINDING',guarded,
          'Trusted reference comes from this local contract; no signature or trusted identity root.')
    alias=copy.deepcopy(d);alias['data'][-1]+=d['modulus'];dump(out/'aliased-input.json',alias)
    baseline_result=out/'baseline-result.json';dump(baseline_result,{'value':oracle(d),
        'experiment':'experiment-A','input_sha256':sha(inp),'attempt':'baseline'})
    r=proc('old-evaluator-alias',[sys.executable,str(oldeval),str(out/'aliased-input.json'),str(baseline_result)])
    check('C03_equal_value_different_input_binding',r.returncode==0 and oracle(alias)==oracle(d)
          and bound_evaluate(baseline_result,'experiment-A',out/'aliased-input.json')['status']=='UNQUALIFIED_BINDING',
          {'old_evaluation':json.loads(r.stdout),'old_input_hash':sha(inp),'new_input_hash':sha(out/'aliased-input.json')},
          'Same numerical answer can be valid for both inputs; it is not evidence that the old artifact was produced from the new bytes.')
    cp=load(BASELINE/'checkpoint.json');dump(out/'original-checkpoint.json',cp)
    original_cp_digest=sha(out/'original-checkpoint.json')
    def checkpoint_guard(path,exp):
        x=load(path)
        if sha(path)!=original_cp_digest:return 'CHECKPOINT_BYTES_CHANGED'
        if x['experiment']!=exp:return 'EXPERIMENT_MISMATCH'
        if not 0<=x['i']<=len(d['data']):return 'INDEX_OUTSIDE_SCOPE'
        return 'ACCEPT_LOCAL_BOUND_CHECKPOINT'
    bad=copy.deepcopy(cp);bad['x']+=1;dump(out/'corrupted-checkpoint.json',bad)
    args=[sys.executable,str(oldworker),'--worker','--input',str(inp),'--result',str(out/'corrupt-resume-result.json'),
          '--resume',str(out/'corrupted-checkpoint.json'),'--experiment','experiment-A','--attempt','corrupt-resume']
    r=proc('old-corrupted-checkpoint',args)
    er=proc('old-corrupted-evaluation',[sys.executable,str(oldeval),str(inp),str(out/'corrupt-resume-result.json')])
    check('C04_old_worker_accepts_state_corruption',r.returncode==0 and er.returncode==1,
          {'worker_rc':r.returncode,'evaluation':json.loads(er.stdout),'guard':checkpoint_guard(out/'corrupted-checkpoint.json','experiment-A')},
          'Input/code hash fields inside a checkpoint do not protect checkpoint state bytes.')
    args=[sys.executable,str(oldworker),'--worker','--input',str(inp),'--result',str(out/'relabeled-result.json'),
          '--resume',str(out/'original-checkpoint.json'),'--experiment','new-independent-experiment','--attempt','relabel']
    r=proc('old-relabeled-checkpoint',args)
    check('C05_old_worker_allows_experiment_relabel',r.returncode==0 and checkpoint_guard(out/'original-checkpoint.json','new-independent-experiment')=='EXPERIMENT_MISMATCH',
          {'result':load(out/'relabeled-result.json'),'guard':'EXPERIMENT_MISMATCH'},
          'New ID cannot make continuation independent; real identity migration needs explicit relation, not silent relabel.')
    # Standard-library RNG state: continuation is same stream, not an independent replicate.
    rng=random.Random(588);stream=[rng.randrange(10000) for _ in range(20)]
    part=random.Random(588);prefix=[part.randrange(10000) for _ in range(8)];state=part.getstate()
    restarted=random.Random(588);wrong=prefix+[restarted.randrange(10000) for _ in range(12)]
    restored=random.Random();restored.setstate(state);correct=prefix+[restored.randrange(10000) for _ in range(12)]
    dump(out/'rng-state.json',state)
    check('C06_rng_continuity_requires_rng_state',correct==stream and wrong!=stream,
          {'clean':stream,'missing_state_resume':wrong,'restored_resume':correct,'state_sha256':sha(out/'rng-state.json')},
          'Actual Python random state only; GPU/distributed RNG and cross-version portability are untested.')
    coeff={'v':3}
    @functools.lru_cache(maxsize=4)
    def hidden_dependency(x):return coeff['v']*x
    a=hidden_dependency(7);coeff['v']=4;b=hidden_dependency(7)
    @functools.lru_cache(maxsize=4)
    def explicit_dependency(x,c):return x*c
    c=explicit_dependency(7,4)
    check('C07_real_lru_cache_hidden_dependency',a==b==21 and c==28,
          {'cached_after_dependency_change':b,'explicit_dependency_result':c,'cache_info':str(hidden_dependency.cache_info())},
          'Actual CPython lru_cache, not an Argo memoization deployment; demonstrates application-defined key incompleteness.')
    db=out/'retry.db';con=sqlite3.connect(db);con.executescript('CREATE TABLE unsafe_effects(id INTEGER); CREATE TABLE safe_effects(id TEXT PRIMARY KEY);');con.close()
    unsafe_attempts=[]
    @retry(stop=stop_after_attempt(2),retry=retry_if_exception_type(OSError),reraise=True)
    def non_idempotent():
        unsafe_attempts.append(len(unsafe_attempts)+1)
        with sqlite3.connect(db) as c:c.execute('INSERT INTO unsafe_effects VALUES (?)',(unsafe_attempts[-1],))
        if len(unsafe_attempts)==1:raise OSError('controlled lost acknowledgement AFTER commit')
        return 'completed'
    non_idempotent();safe_attempts=[]
    @retry(stop=stop_after_attempt(2),retry=retry_if_exception_type(OSError),reraise=True)
    def idempotent():
        safe_attempts.append(len(safe_attempts)+1)
        with sqlite3.connect(db) as c:c.execute('INSERT OR IGNORE INTO safe_effects VALUES (?)',('experiment-A:logical-effect',))
        if len(safe_attempts)==1:raise OSError('controlled lost acknowledgement AFTER commit')
        return 'completed'
    idempotent()
    with sqlite3.connect(db) as c:
        unsafe_n=c.execute('SELECT count(*) FROM unsafe_effects').fetchone()[0];safe_n=c.execute('SELECT count(*) FROM safe_effects').fetchone()[0]
    check('C08_retry_repeats_committed_effect',unsafe_n==2 and safe_n==1,
          {'tenacity_attempts_unsafe':unsafe_attempts,'tenacity_attempts_safe':safe_attempts,'unsafe_rows':unsafe_n,'safe_rows':safe_n},
          'Actual Tenacity and SQLite; not K8s/Argo exactly-once test. Unique effect key mitigates this DB case, not all external side effects.')
    domain_calls=[]
    @retry(stop=stop_after_attempt(2),retry=retry_if_exception_type(OSError),reraise=True)
    def scientific_failure_as_data():
        domain_calls.append('executed')
        return {'process':'COMPLETED','scientific_status':'FAILED'}
    result=scientific_failure_as_data()
    check('C09_scientific_failure_does_not_trigger_exception_retry',result['scientific_status']=='FAILED' and len(domain_calls)==1,dict(result,actual_attempt_count=len(domain_calls)),
          'Retry configured for execution exceptions; domain failure as a value is a separate application decision.')
    # Real process termination in uncommitted SQLite transaction.
    crashdb=out/'crash.db'
    with sqlite3.connect(crashdb) as c:c.execute('CREATE TABLE checkpoint(i INTEGER,x INTEGER)');c.execute('INSERT INTO checkpoint VALUES (8,123)')
    code="import sqlite3,sys,time; c=sqlite3.connect(sys.argv[1]); c.execute('UPDATE checkpoint SET i=20,x=767'); print('UNCOMMITTED',flush=True); time.sleep(30)"
    p=subprocess.Popen([sys.executable,'-c',code,str(crashdb)],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
    ready=select.select([p.stdout],[],[],5)[0]
    if not ready:p.kill();p.communicate();raise RuntimeError('SQLite handshake timed out')
    handshake=p.stdout.readline().strip();p.kill();stdout,stderr=p.communicate(timeout=5)
    with sqlite3.connect(crashdb) as c:recovered=c.execute('SELECT i,x FROM checkpoint').fetchone()
    check('C10_sqlite_uncommitted_crash_recovery',handshake=='UNCOMMITTED' and p.returncode==-9 and recovered==(8,123),
          {'child_rc':p.returncode,'recovered':recovered,'stderr':stderr},
          'Real SIGKILL rollback with local SQLite; does not test power-loss/fsync/hardware durability.')
    def otel_case(label,sampler,limits=None,attrs=None):
        exporter=InMemorySpanExporter();provider=TracerProvider(sampler=sampler,span_limits=limits,shutdown_on_exit=False)
        provider.add_span_processor(SimpleSpanProcessor(exporter))
        with provider.get_tracer('ai4s.component.study').start_as_current_span(label) as span:
            for k,v in (attrs or {}).items():span.set_attribute(k,v)
            span.set_status(Status(StatusCode.OK))
        provider.force_flush();spans=exporter.get_finished_spans()
        serialized=[json.loads(s.to_json()) for s in spans];dump(out/(label+'.spans.json'),serialized)
        provider.shutdown();return spans,serialized
    spans,_=otel_case('otel-off',ALWAYS_OFF,attrs={'scientific.evidence_ref':'retained.json'})
    check('C11_otel_always_off_exports_no_span',len(spans)==0,{'exported_spans':len(spans),'sampler':'ALWAYS_OFF'},
          'Actual OTel SDK1.39.0, in-memory exporter; no collector/network/exporter loss test.')
    spans,serialized=otel_case('otel-on',ALWAYS_ON,attrs={'scientific.verdict':'FAILED','experiment.id':'experiment-A'})
    check('C12_otel_OK_coexists_with_failed_verdict',spans[0].status.status_code==StatusCode.OK and spans[0].attributes['scientific.verdict']=='FAILED',
          {'span_status':'OK','scientific.verdict':'FAILED','exported_spans':len(spans)},
          'OTel describes instrumentation status; a domain-specific attribute carries a distinct verdict, not an automatically validated scientific claim.')
    spans,_=otel_case('otel-limited',ALWAYS_ON,SpanLimits(max_attributes=2),
        {'scientific.evidence_ref':'retained.json','noise.1':'x','noise.2':'y'})
    check('C13_otel_attribute_limit_drops_binding', 'scientific.evidence_ref' not in spans[0].attributes and spans[0].dropped_attributes==1,
          {'attributes':dict(spans[0].attributes),'dropped_attributes':spans[0].dropped_attributes},
          'This SDK/limit configuration loses an essential evidence link even when the span itself is retained.')
    # Actual RO-Crate serializer/reloader does not execute scientific evaluation.
    crate=ROCrate();crate.name='Synthetic negative-control package';crate.description='Local component evidence only; not a scientific validation certificate.'
    crate.add_file(inp,dest_path='input.json');crate.add_file(foreign,dest_path='result.json')
    dump(out/'evaluation-report.json',json.loads(processes[0]['stdout']))
    crate.add_file(out/'evaluation-report.json',dest_path='evaluation-report.json')
    tool=crate.add(ContextEntity(crate,'#old-evaluator',properties={'@type':'SoftwareApplication','name':'Original integer evaluator','softwareVersion':'baseline-20261012'}))
    action=crate.add(ContextEntity(crate,'#evaluation-attempt',properties={'@type':'CreateAction','name':'Actual original evaluator execution',
        'instrument':tool,'object':[{'@id':'input.json'},{'@id':'result.json'}],'result':{'@id':'evaluation-report.json'},'actionStatus':{'@id':'http://schema.org/CompletedActionStatus'},
        'description':'The evaluator returned success for a numerically equal but foreign-bound result. This is a negative control, not independent scientific validation.'}))
    crate.root_dataset.append_to('mentions',action);crate.write(out/'crate')
    reloaded=ROCrate(out/'crate')
    check('C14_rocrate_packages_binding_invalid_result',reloaded.get('#evaluation-attempt') is not None and bound_evaluate(out/'crate/result.json','experiment-A',out/'crate/input.json')['status']=='UNQUALIFIED_BINDING',
          {'serialization':'SUCCESS','reload':'SUCCESS','application_binding':'UNQUALIFIED_BINDING'},
          'Actual rocrate-py0.16.0 serializer/reloader. Not a full Process Run profile validator; packaging does not establish scientific validity.')
    oldhash=sha(out/'crate/input.json');shutil.copytree(out/'crate',out/'crate-tampered')
    dd=load(out/'crate-tampered/input.json');dd['a']=4;dump(out/'crate-tampered/input.json',dd)
    ROCrate(out/'crate-tampered')
    check('C15_rocrate_reload_does_not_verify_external_digest',sha(out/'crate-tampered/input.json')!=oldhash,
          {'reload':'SUCCESS','trusted_reference_sha256':oldhash,'actual_sha256':sha(out/'crate-tampered/input.json')},
          'Specific library read operation without supplied checksum verification; not evidence that RO-Crate standards or all validators lack integrity support.')
    # Minimal adaptive interface: consume actual bound/invalid results, no new research allocation.
    def next_action(evaluation,execution_state):
        if execution_state!='COMPLETED':return 'HANDLE_EXECUTION_FAILURE'
        if evaluation['status']=='UNQUALIFIED_BINDING':return 'WITHHOLD_CLAIM_REPAIR_BINDING'
        if evaluation['status']=='FAILED':return 'RECORD_NEGATIVE_RETURN_TO_PORTFOLIO'
        if evaluation['status']=='SUPPORTED':return 'RECORD_SCOPED_RESULT_RETURN_TO_PORTFOLIO'
        return 'NOT_EVALUATED_NO_CLAIM'
    good=bound_evaluate(baseline_result,'experiment-A',inp)
    bad_result=out/'numerical-failure.json';dump(bad_result,{'value':0,'experiment':'experiment-A','input_sha256':sha(inp)})
    failed=bound_evaluate(bad_result,'experiment-A',inp)
    transitions={label:next_action(e,'COMPLETED') for label,e in [('binding-invalid',guarded),('numerical-supported',good),('numerical-failed',failed)]}
    dump(out/'adaptive-transitions.json',{'transitions':transitions,'allocation_effect':'NONE','feedback_exposure':'ALL_SYNTHETIC_INPUTS_ALREADY_SEEN'})
    check('C16_completed_execution_different_scientific_actions',len(set(transitions.values()))==3,transitions,
          'Controlled interface demonstration based on actual evaluator results; no autonomous experiment generation, search superiority or RSI evidence.',kind='SYNTHETIC_ADAPTIVE_INTERFACE')
    versions={n:md.version(n) for n in ['opentelemetry-api','opentelemetry-sdk','rocrate','tenacity']}
    modules={'otel-exporter':inspect.getfile(InMemorySpanExporter),'otel-provider':inspect.getfile(TracerProvider),
             'rocrate':inspect.getfile(ROCrate),'tenacity-retry':inspect.getfile(retry)}
    dump(out/'component-identity.json',{'versions':versions,'python':sys.version,'platform':platform.platform(),
         'sqlite':sqlite3.sqlite_version,'module_hashes':{n:{'path':p,'sha256':sha(p)} for n,p in modules.items()},
         'baseline_hashes':{'worker':sha(oldworker),'evaluator':sha(oldeval)},'script_sha256':sha(__file__)})
    dump(out/'process-events.json',processes)
    dump(out/'summary.json',{'checks':records,'expectations_met':sum(x['expectation_met'] for x in records),
         'total':len(records),'actual_product_defects_claimed':False,'real_scientific_validation':False,
         'independent_review':'NOT_PERFORMED','external_contact':'HOLD_NOT_SENT','xrem_adoption':'NOT_REQUESTED_NOT_GRANTED'})
    dump(out/'hashes.json',{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*')) if p.is_file() and p.name!='hashes.json'})
    print(json.dumps({'expectations_met':sum(x['expectation_met'] for x in records),'total':len(records),'out':str(out)},indent=2))
    return 0 if all(x['expectation_met'] for x in records) else 1
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--out',required=True);args=ap.parse_args();sys.exit(main(Path(args.out)))
