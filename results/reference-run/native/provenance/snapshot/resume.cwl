{
  "arguments": [
    {
      "position": 2,
      "valueFrom": "resume"
    }
  ],
  "class": "CommandLineTool",
  "cwlVersion": "v1.2",
  "inputs": {
    "anchor": {
      "inputBinding": {
        "position": 7,
        "prefix": "--anchor"
      },
      "type": "File"
    },
    "checkpoint": {
      "inputBinding": {
        "position": 6,
        "prefix": "--checkpoint"
      },
      "type": "File"
    },
    "contract": {
      "inputBinding": {
        "position": 4,
        "prefix": "--contract"
      },
      "type": "File"
    },
    "fault": {
      "inputBinding": {
        "position": 5,
        "prefix": "--fault"
      },
      "type": "string"
    },
    "input": {
      "inputBinding": {
        "position": 3,
        "prefix": "--input"
      },
      "type": "File"
    },
    "program": {
      "inputBinding": {
        "position": 1
      },
      "type": "File"
    },
    "python": {
      "inputBinding": {
        "position": 0
      },
      "type": "string"
    }
  },
  "outputs": {
    "attempt_spans_json": {
      "outputBinding": {
        "glob": "attempt-spans.json"
      },
      "type": "File"
    },
    "effects_db": {
      "outputBinding": {
        "glob": "effects.db"
      },
      "type": "File"
    },
    "result_json": {
      "outputBinding": {
        "glob": "result.json"
      },
      "type": "File"
    },
    "resume_receipt_json": {
      "outputBinding": {
        "glob": "resume-receipt.json"
      },
      "type": "File"
    }
  },
  "permanentFailCodes": [
    22
  ],
  "requirements": {
    "NetworkAccess": {
      "networkAccess": false
    }
  },
  "stderr": "resume.stderr",
  "stdout": "resume.stdout",
  "successCodes": [
    0
  ]
}
