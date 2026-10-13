# Optional addition to §4.4 — Reproducibility & Provenance

Status: candidate; not submitted. Prepared with substantial AI assistance for Fei Yang’s review. This is a small additional point beyond the previous sampling discussion; it does not replace or repeat the earlier contribution.

## Proposed text

Even a retained trace span can lose an evidence reference when attribute limits apply. Preserve and validate essential result-to-input and result-to-evaluation links in an evidence index that does not depend on a span attribute as its only connection. Reuse provenance and manifest-validation tools, while reporting artifact integrity, evaluation outcomes and scientific independence separately.

## Evidence and scope

The local OpenTelemetry SDK control C13 retains a span but drops its early evidence-reference attribute under a two-attribute limit. This is an actual in-memory SDK observation, not a collector/backend retention experiment or a claim that telemetry cannot preserve references. The fresh reference run records the observation in `results/reference-run/components/C13_otel_attribute_limit_drops_binding.json`. The proposed index is an application example, not a new standard.

Primary reference: [OpenTelemetry tracing SDK limits](https://opentelemetry.io/docs/specs/otel/trace/sdk/). Supporting local evidence: [matrix](../EVIDENCE_MATRIX.md). Public personal proposal; working-group review pending; license remains Apache-2.0 for original reproduction code.


Publication note: human approval now permits this personal technical case and Apache-2.0 original reproduction code. Historical preparation fields are retained as history. Working-group adoption and independent third-party replication remain unproven.
