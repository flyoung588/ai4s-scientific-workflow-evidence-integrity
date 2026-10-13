{
  "class": "Workflow",
  "cwlVersion": "v1.2",
  "inputs": {
    "contract": "File",
    "evaluator": "File",
    "fault": "string",
    "input": "File",
    "program": "File",
    "python": "string"
  },
  "outputs": {
    "bundle": {
      "outputSource": "package/bundle",
      "type": "Directory"
    }
  },
  "steps": {
    "checkpoint": {
      "in": {
        "contract": "contract",
        "fault": "fault",
        "input": "input",
        "program": "program",
        "python": "python"
      },
      "out": [
        "checkpoint_json",
        "anchor_json",
        "checkpoint_receipt_json"
      ],
      "run": "checkpoint.cwl"
    },
    "evaluate": {
      "in": {
        "contract": "contract",
        "evaluator": "evaluator",
        "fault": "fault",
        "input": "input",
        "program": "program",
        "python": "python",
        "receipt": "resume/resume_receipt_json",
        "result": "resume/result_json"
      },
      "out": [
        "evaluation_report_json",
        "evaluation_receipt_json"
      ],
      "run": "evaluate.cwl"
    },
    "package": {
      "in": {
        "anchor": "checkpoint/anchor_json",
        "checkpoint": "checkpoint/checkpoint_json",
        "checkpoint-receipt": "checkpoint/checkpoint_receipt_json",
        "contract": "contract",
        "database": "resume/effects_db",
        "evaluation-receipt": "evaluate/evaluation_receipt_json",
        "fault": "fault",
        "input": "input",
        "program": "program",
        "python": "python",
        "receipt": "resume/resume_receipt_json",
        "report": "evaluate/evaluation_report_json",
        "result": "resume/result_json",
        "spans": "resume/attempt_spans_json"
      },
      "out": [
        "bundle"
      ],
      "run": "package.cwl"
    },
    "resume": {
      "in": {
        "anchor": "checkpoint/anchor_json",
        "checkpoint": "checkpoint/checkpoint_json",
        "contract": "contract",
        "fault": "fault",
        "input": "input",
        "program": "program",
        "python": "python"
      },
      "out": [
        "result_json",
        "resume_receipt_json",
        "attempt_spans_json",
        "effects_db"
      ],
      "run": "resume.cwl"
    }
  }
}
