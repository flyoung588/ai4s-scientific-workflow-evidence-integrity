{
  "arguments": [
    {
      "position": 2,
      "valueFrom": "package"
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
    "checkpoint-receipt": {
      "inputBinding": {
        "position": 8,
        "prefix": "--checkpoint-receipt"
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
    "database": {
      "inputBinding": {
        "position": 14,
        "prefix": "--database"
      },
      "type": "File"
    },
    "evaluation-receipt": {
      "inputBinding": {
        "position": 12,
        "prefix": "--evaluation-receipt"
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
        "position": 10,
        "prefix": "--receipt"
      },
      "type": "File"
    },
    "report": {
      "inputBinding": {
        "position": 11,
        "prefix": "--report"
      },
      "type": "File"
    },
    "result": {
      "inputBinding": {
        "position": 9,
        "prefix": "--result"
      },
      "type": "File"
    },
    "spans": {
      "inputBinding": {
        "position": 13,
        "prefix": "--spans"
      },
      "type": "File"
    }
  },
  "outputs": {
    "bundle": {
      "outputBinding": {
        "glob": "bundle"
      },
      "type": "Directory"
    }
  },
  "permanentFailCodes": [],
  "requirements": {
    "NetworkAccess": {
      "networkAccess": false
    }
  },
  "stderr": "package.stderr",
  "stdout": "package.stdout",
  "successCodes": [
    0
  ]
}
