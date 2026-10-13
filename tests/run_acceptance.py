#!/usr/bin/env python3
"""Run preserved engineering cases; acceptance is not scientific qualification."""
import argparse
import datetime as dt
import hashlib
import importlib.metadata as md
import json
import os
from pathlib import Path
import platform
import site
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def put(p, v): Path(p).write_text(json.dumps(v, indent=2, sort_keys=True)+'\n')
def load(p): return json.loads(Path(p).read_text())

def main(out, components_only, native):
    out.mkdir(parents=True, exist_ok=False)
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    # Fixed contract was created before this entrypoint's first final run.
    contract = load(ROOT/'fixtures/acceptance-contract.json')
    env = os.environ.copy()
    removed = ['CWL_FULL_NAME', 'ORCID', 'CWLTOOL_OPTIONS', 'PYTHONPATH']
    for name in removed: env.pop(name, None)
    events = []
    def run(name, cmd, timeout=180):
        t0 = time.time()
        try:
            p = subprocess.run(cmd, cwd=ROOT, env=env, capture_output=True,
                               text=True, timeout=timeout)
            rc, stdout, stderr = p.returncode, p.stdout, p.stderr
        except subprocess.TimeoutExpired as e:
            rc, stdout, stderr = 'TIMEOUT', str(e.stdout or ''), str(e.stderr or '')
        row = {'name': name, 'command': cmd, 'start_unix': t0,
               'end_unix': time.time(), 'exit_code': rc,
               'stdout': stdout, 'stderr': stderr}
        put(out/(name+'.receipt.json'), row)
        events.append(row)
        return rc
    versions = {x.metadata['Name']: x.version for x in md.distributions()}
    cfg = Path(sys.prefix)/'pyvenv.cfg'
    isolated_venv = sys.prefix != sys.base_prefix and cfg.is_file() and \
                    'include-system-site-packages = false' in cfg.read_text().lower()
    environment = {'os': platform.platform(), 'python': sys.version,
                   'packages': versions, 'isolated_venv':isolated_venv,
                   'user_site_enabled':site.ENABLE_USER_SITE,
                   'removed_environment_variable_names': removed,
                   'network_isolation': 'NOT_CERTIFIED',
                   'environment_identity_scope': 'declared OS/Python/packages only'}
    # Stable identity covers the declared fields, not all hidden machine state.
    environment['declared_environment_identity'] = hashlib.sha256(
        json.dumps(environment,sort_keys=True).encode()).hexdigest()
    put(out/'environment.json',environment)
    py = sys.executable
    component_rc = run('components', [py,str(ROOT/'src/components/research.py'),
                                     '--out',str(out/'components')])
    baseline_rc = run('baseline', [py,str(ROOT/'src/components/baseline/case.py'),
                                 '--out',str(out/'baseline')])
    cwl_rc = raw_rc = 'NOT_RUN'
    native_rc = native_audit_rc = 'NOT_RUN'
    if not components_only:
        cwl_rc = run('cwl', [py,str(ROOT/'src/cwl/run_case.py'),
                            '--out',str(out/'cwl')],360)
        if cwl_rc == 0:
            raw_rc = run('cwl-byte-adjudication',
                         [py,str(ROOT/'src/cwl/verify_existing.py'),'--run',str(out/'cwl'),
                          '--out',str(out/'cwl-adjudication.json')])
        if native and cwl_rc == 0:
            n = out/'native';(n/'outputs').mkdir(parents=True);(n/'tmp').mkdir()
            native_rc = run('native-provenance',
                [str(Path(py).with_name('cwltool')),'--no-container','--leave-tmpdir',
                 '--no-doc-cache','--disable-user-provenance','--disable-host-provenance',
                 '--provenance',str(n/'provenance'),'--outdir',str(n/'outputs'),
                 '--tmp-outdir-prefix',str(n/'tmp')+'/',
                 str(ROOT/'src/cwl/workflow/workflow.cwl'),
                 str(out/'cwl/numerical-failure/job.json')])
            if native_rc == 0:
                native_audit_rc = run('native-audit',
                    [py,str(ROOT/'src/cwl/audit_native.py'),'--bag',str(n/'provenance'),
                     '--out',str(n/'audit'),'--boundary',str(n/'outputs/bundle/boundary.json')])
    cs = load(out/'components/summary.json') if component_rc == 0 else None
    bs = load(out/'baseline/summary.json') if baseline_rc == 0 else None
    checks = {'isolated_venv':isolated_venv and not site.ENABLE_USER_SITE,
              'components_original_16': cs is not None and cs['total']==16 and
              len(cs['checks'])==16 and all(x['expectation_met'] for x in cs['checks']),
              'baseline_preserved_10':bs is not None and bs['total']==10 and bs['passed']==10}
    if not components_only:
        checks['cwl_original_six'] = cwl_rc==0 and load(out/'cwl/summary.json')['expectations_met']==6
        checks['cwl_raw_bytes_DB_adjudication'] = raw_rc==0
    if native:
        checks['native_PROV_and_BagIt'] = native_rc==0 and native_audit_rc==0
    status = 'PASS_SCOPED_ENGINEERING_ACCEPTANCE' if all(checks.values()) else 'FAIL_ACCEPTANCE'
    summary = {'status':status, 'checks':checks, 'started_utc':started,
               'ended_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
               'acceptance_contract_sha256':sha(ROOT/'fixtures/acceptance-contract.json'),
               'runner_sha256':sha(__file__), 'components_only':components_only,
               'native_requested':native, 'native_execution':native_rc,
               'native_audit':native_audit_rc,
               'L1':'SOFTWARE_BEHAVIOR_CHECKED_FOR_ENUMERATED_CONTROLS',
               'L2':'LOCAL_RETAINED_BYTES_AND_RELATIONS_CHECKED_NOT_AUTHENTICATED',
               'L3':'EXACT_SYNTHETIC_INTEGER_CRITERION_ONLY',
               'L4':'INDEPENDENT_THIRD_PARTY_REPLICATION_NOT_PERFORMED',
               'argo_kubernetes':'ARGO_INTEGRATION_NOT_RUN',
               'scientific_discovery':False, 'external_publication':'HOLD_NOT_SENT',
               'original_case_counts_are_not_new_experiments':True}
    put(out/'summary.json',summary)
    put(out/'process-events.json',events)
    put(out/'hashes.json',{str(p.relative_to(out)):sha(p) for p in sorted(out.rglob('*'))
                           if p.is_file() and p.name!='hashes.json'})
    print(json.dumps(summary,indent=2))
    return 0 if all(checks.values()) else 1

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',required=True)
    a.add_argument('--components-only',action='store_true');a.add_argument('--native',action='store_true')
    v=a.parse_args()
    if v.native and v.components_only:a.error('--native requires the CWL suite')
    raise SystemExit(main(Path(v.out).resolve(),v.components_only,v.native))
