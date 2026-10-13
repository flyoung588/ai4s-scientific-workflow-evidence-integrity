{
  "arguments": [
    {
      "position": 2,
      "valueFrom": "evaluate"
    }
  ],
  "class": "CommandLineTool",
  "cwlVersion": "v1.2",
  "inputs": {
    "contract": {
      "inputBinding": {
        "position": 4,
        "prefix": "--contract"
      },
      "type": "File"
    },
    "evaluator": {
      "inputBinding": {
        "position": 8,
        "prefix": "--evaluator"
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
    },
    "receipt": {
      "inputBinding": {
        "position": 7,
        "prefix": "--receipt"
      },
      "type": "File"
    },
    "result": {
      "inputBinding": {
        "position": 6,
        "prefix": "--result"
      },
      "type": "File"
    }
  },
  "outputs": {
    "evaluation_receipt_json": {
      "outputBinding": {
        "glob": "evaluation-receipt.json"
      },
      "type": "File"
    },
    "evaluation_report_json": {
      "outputBinding": {
        "glob": "evaluation-report.json"
      },
      "type": "File"
    }
  },
  "permanentFailCodes": [],
  "requirements": {
    "NetworkAccess": {
      "networkAccess": false
    }
  },
  "stderr": "evaluate.stderr",
  "stdout": "evaluate.stdout",
  "successCodes": [
    0
  ]
}
