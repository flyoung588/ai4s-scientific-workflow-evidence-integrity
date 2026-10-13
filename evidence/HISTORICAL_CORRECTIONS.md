# Preserved failures and corrections

The original first component run was retained. Its RO-Crate evaluation action mistakenly represented the evaluated candidate as a result, rather than as an input to an action producing the evaluation report. The corrected second script is the preserved component source included here; its original first-run source and receipt remain in the separate, private preparation baseline. They were not overwritten.

The earlier integer-only evaluator deliberately remains in src/components/baseline: it accepts correct numbers with foreign experiment/input identities. The original worker deliberately remains there too: input/code fields alone do not protect checkpoint payload state. The corrupt checkpoint completes with 807 instead of 767; these failing observations are retained in the new reference run.

The native-provenance study historically encountered a missing BagIt dependency. Its failed receipt was retained in the original study; bagit==1.9.0 is now an explicit pin. The first RO-Crate relation was corrected in the retained CWL tools. None of these local corrections establish scientific qualification.

The SDEI v1.7 background disposition supplied for this task remains EXPERIMENT_COMPLETED / VALIDATION_FAILED / RETURN_TO_PORTFOLIO: 23/28 held-out expectations, one false acceptance and four false blocks. Those counts were not rerun or independently inspected in this package. SDEI is neither its main case nor a qualified decision checker; no v1.8 was started.

Packaging QA caught a personal home path in a pip-cache warning. The original receipt and failed QA were retained outside the candidate archive. A second dependency check with an isolated temporary cache completed cleanly; fixture source and runtime evidence were unchanged.
