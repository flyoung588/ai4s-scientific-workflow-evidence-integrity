{
  "arguments": [
    {
      "position": 2,
      "valueFrom": "checkpoint"
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
    "anchor_json": {
      "outputBinding": {
        "glob": "anchor.json"
      },
      "type": "File"
    },
    "checkpoint_json": {
      "outputBinding": {
        "glob": "checkpoint.json"
      },
      "type": "File"
    },
    "checkpoint_receipt_json": {
      "outputBinding": {
        "glob": "checkpoint-receipt.json"
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
  "stderr": "checkpoint.stderr",
  "stdout": "checkpoint.stdout",
  "successCodes": [
    0
  ]
}
