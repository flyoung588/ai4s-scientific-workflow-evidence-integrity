#!/usr/bin/env python3
"""Audit native CWL PROV/BagIt output and a length-preserving corrupt copy."""
import argparse,json,shutil
from pathlib import Path
from importlib.metadata import version
import bagit
from rdflib import Graph,Namespace,RDF
def main(bag,out,boundary):
    out.mkdir(parents=True,exist_ok=False)
    bagit.Bag(str(bag)).validate()
    copy=out/'tampered-bag';shutil.copytree(bag,copy)
    target=next(x for x in sorted((copy/'data').rglob('*')) if x.is_file() and x.stat().st_size)
    b=target.read_bytes();target.write_bytes(bytes([b[0]^1])+b[1:])
    error=None;detected=False
    try:bagit.Bag(str(copy)).validate()
    except bagit.BagValidationError as e:detected=True;error=str(e)
    g=Graph();g.parse(bag/'metadata/provenance/primary.cwlprov.ttl',format='turtle')
    prov=Namespace('http://www.w3.org/ns/prov#')
    counts={'triples':len(g),'activities':len(set(g.subjects(RDF.type,prov.Activity))),
       'used_relations':len(list(g.triples((None,prov.used,None)))),
       'generation_relations':len(list(g.triples((None,prov.wasGeneratedBy,None)))),
       'qualified_usage_relations':len(list(g.triples((None,prov.qualifiedUsage,None)))),
       'qualified_generation_relations':len(list(g.triples((None,prov.qualifiedGeneration,None))))}
    report={'bagit_version':version('bagit'),'rdflib_version':version('rdflib'),
       'original_manifest_validation':'PASS','tampered_manifest_validation':'REJECTED' if detected else 'UNEXPECTED_ACCEPT',
       'changed_relative_file':str(target.relative_to(copy)),'tamper_preserved_length':len(b)==target.stat().st_size,
       'failure':error,'prov_graph_parse':counts,'actual_boundary':json.loads(boundary.read_text()),
       'scope':'Native workflow provenance and manifest integrity only; default CWL payload SHA1, no authentication or scientific validation'}
    (out/'audit.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
    return 0 if detected and counts['activities']>=4 else 1
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bag',required=True);ap.add_argument('--out',required=True);ap.add_argument('--boundary',required=True);a=ap.parse_args()
    raise SystemExit(main(Path(a.bag),Path(a.out),Path(a.boundary)))
