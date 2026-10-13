# Proposed §5 case study — execution, evidence and evaluation

Status: candidate; not submitted. Prepared with substantial AI assistance for Fei Yang’s review. The proposed text below is 186 words by whitespace count. Placement, credit and acceptance remain with the working group.

## Proposed text

A local CWL reference workflow illustrates how completed execution can coexist with invalid evidence or a failed evaluation. Using synthetic integer inputs, a process writes a checkpoint and is deliberately interrupted. A second process verifies the checkpoint and resumes. A committed side effect then loses its acknowledgement and is retried: a stable logical key and database uniqueness constraint leave one record, while an unsafe control leaves two.

Additional controls attach a correct numerical result to the wrong experiment, alter checkpoint state, or break the result-to-evaluation link. Application checks reject the affected claim; a corrupt checkpoint stops the workflow before evaluation. Another case completes normally but records a failed numerical evaluation. Existing native PROV records and BagIt validation preserve execution history and detect a controlled byte mutation, without certifying scientific validity.

Separate component checks show that an incomplete cache key can reuse a stale value and that a retained telemetry span can lose its evidence attribute. The cache controls use local Python implementations, not deployed workflow caches. All scientific inputs are synthetic; this is local engineering evidence, not an Argo/Kubernetes deployment, independent scientific validation or a discovery.

## Evidence and scope

The original local software observations were reproduced by the unified entrypoint on 2026-10-13, 05:19:09–05:19:28 UTC: `PASS_SCOPED_ENGINEERING_ACCEPTANCE`. See [reference receipt](../results/reference-run/summary.json) and [evidence matrix](../EVIDENCE_MATRIX.md). No independent third-party replication has been performed. CWL and BagIt are supporting technologies and are not represented as CNCF projects.

Primary references: [CWL workflow semantics](https://www.commonwl.org/user_guide/topics/workflows.html), [W3C PROV-DM](https://www.w3.org/TR/prov-dm/), [Workflow Run RO-Crate](https://www.researchobject.org/workflow-run-crate/), and [BagIt-python](https://github.com/LibraryOfCongress/bagit-python). Public personal proposal; working-group review pending; code licensing remains Apache-2.0 for original reproduction code.


Publication note: human approval now permits this personal technical case and Apache-2.0 original reproduction code. Historical preparation fields are retained as history. Working-group adoption and independent third-party replication remain unproven.
