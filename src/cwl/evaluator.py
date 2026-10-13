#!/usr/bin/env python3
"""Separate arithmetic implementation; same author, not qualified independent science."""
import hashlib,json,sys
from pathlib import Path
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
read=lambda p:json.loads(Path(p).read_text())
d,c,r,receipt=[read(p) for p in sys.argv[1:5]]
n=len(d['data']);a=d['a'];m=d['modulus']
expected=(pow(a,n,m)*d['x0']+sum(pow(a,n-i-1,m)*v for i,v in enumerate(d['data'])))%m
checks={'input_binding':sha(sys.argv[1])==c['input_sha256']==r['input_sha256'],
        'experiment_binding':c['experiment']==r['experiment'],
        'producer_result_binding':receipt['result_sha256']==sha(sys.argv[3]),
        'checkpoint_binding':receipt['checkpoint_sha256']==r['checkpoint_sha256'],
        'side_effect_idempotency':receipt['effect_count']==1}
numeric='SUPPORTED_FIXTURE' if r['value']==expected else 'FAILED_FIXTURE'
integrity='VERIFIED_LOCAL' if all(checks.values()) else 'REJECTED_BINDING_OR_EFFECT'
disposition='RECORD_SCOPED_FIXTURE' if integrity=='VERIFIED_LOCAL' and numeric=='SUPPORTED_FIXTURE' else 'WITHHOLD_FIXTURE_CLAIM'
print(json.dumps({'numeric_status':numeric,'expected':expected,'observed':r['value'],'integrity_status':integrity,
    'checks':checks,'claim_disposition':disposition,'subject_result_sha256':sha(sys.argv[3]),
    'real_scientific_status':'NOT_EVALUATED','independent_review':'NOT_PERFORMED'}))
