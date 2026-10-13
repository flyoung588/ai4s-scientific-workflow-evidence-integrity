{
    "$graph": [
        {
            "arguments": [
                {
                    "position": 2,
                    "valueFrom": "checkpoint"
                }
            ],
            "class": "CommandLineTool",
            "inputs": [
                {
                    "inputBinding": {
                        "position": 4,
                        "prefix": "--contract"
                    },
                    "type": "File",
                    "id": "#checkpoint.cwl/contract"
                },
                {
                    "inputBinding": {
                        "position": 5,
                        "prefix": "--fault"
                    },
                    "type": "string",
                    "id": "#checkpoint.cwl/fault"
                },
                {
                    "inputBinding": {
                        "position": 3,
                        "prefix": "--input"
                    },
                    "type": "File",
                    "id": "#checkpoint.cwl/input"
                },
                {
                    "inputBinding": {
                        "position": 1
                    },
                    "type": "File",
                    "id": "#checkpoint.cwl/program"
                },
                {
                    "inputBinding": {
                        "position": 0
                    },
                    "type": "string",
                    "id": "#checkpoint.cwl/python"
                }
            ],
            "permanentFailCodes": [],
            "requirements": [
                {
                    "networkAccess": false,
                    "class": "NetworkAccess"
                }
            ],
            "stderr": "checkpoint.stderr",
            "stdout": "checkpoint.stdout",
            "successCodes": [
                0
            ],
            "id": "#checkpoint.cwl",
            "outputs": [
                {
                    "outputBinding": {
                        "glob": "anchor.json"
                    },
                    "type": "File",
                    "id": "#checkpoint.cwl/anchor_json"
                },
                {
                    "outputBinding": {
                        "glob": "checkpoint.json"
                    },
                    "type": "File",
                    "id": "#checkpoint.cwl/checkpoint_json"
                },
                {
                    "outputBinding": {
                        "glob": "checkpoint-receipt.json"
                    },
                    "type": "File",
                    "id": "#checkpoint.cwl/checkpoint_receipt_json"
                }
            ]
        },
        {
            "arguments": [
                {
                    "position": 2,
                    "valueFrom": "evaluate"
                }
            ],
            "class": "CommandLineTool",
            "inputs": [
                {
                    "inputBinding": {
                        "position": 4,
                        "prefix": "--contract"
                    },
                    "type": "File",
                    "id": "#evaluate.cwl/contract"
                },
                {
                    "inputBinding": {
                        "position": 8,
                        "prefix": "--evaluator"
                    },
                    "type": "File",
                    "id": "#evaluate.cwl/evaluator"
                },
                {
                    "inputBinding": {
                        "position": 5,
                        "prefix": "--fault"
                    },
                    "type": "string",
                    "id": "#evaluate.cwl/fault"
                },
                {
                    "inputBinding": {
                        "position": 3,
                        "prefix": "--input"
                    },
                    "type": "File",
                    "id": "#evaluate.cwl/input"
                },
                {
                    "inputBinding": {
                        "position": 1
                    },
                    "type": "File",
                    "id": "#evaluate.cwl/program"
                },
                {
                    "inputBinding": {
                        "position": 0
                    },
                    "type": "string",
                    "id": "#evaluate.cwl/python"
                },
                {
                    "inputBinding": {
                        "position": 7,
                        "prefix": "--receipt"
                    },
                    "type": "File",
                    "id": "#evaluate.cwl/receipt"
                },
                {
                    "inputBinding": {
                        "position": 6,
                        "prefix": "--result"
                    },
                    "type": "File",
                    "id": "#evaluate.cwl/result"
                }
            ],
            "outputs": [
                {
                    "outputBinding": {
                        "glob": "evaluation-receipt.json"
                    },
                    "type": "File",
                    "id": "#evaluate.cwl/evaluation_receipt_json"
                },
                {
                    "outputBinding": {
                        "glob": "evaluation-report.json"
                    },
                    "type": "File",
                    "id": "#evaluate.cwl/evaluation_report_json"
                }
            ],
            "permanentFailCodes": [],
            "requirements": [
                {
                    "networkAccess": false,
                    "class": "NetworkAccess"
                }
            ],
            "stderr": "evaluate.stderr",
            "stdout": "evaluate.stdout",
            "successCodes": [
                0
            ],
            "id": "#evaluate.cwl"
        },
        {
            "arguments": [
                {
                    "position": 2,
                    "valueFrom": "package"
                }
            ],
            "class": "CommandLineTool",
            "inputs": [
                {
                    "inputBinding": {
                        "position": 7,
                        "prefix": "--anchor"
                    },
                    "type": "File",
                    "id": "#package.cwl/anchor"
                },
                {
                    "inputBinding": {
                        "position": 6,
                        "prefix": "--checkpoint"
                    },
                    "type": "File",
                    "id": "#package.cwl/checkpoint"
                },
                {
                    "inputBinding": {
                        "position": 8,
                        "prefix": "--checkpoint-receipt"
                    },
                    "type": "File",
                    "id": "#package.cwl/checkpoint-receipt"
                },
                {
                    "inputBinding": {
                        "position": 4,
                        "prefix": "--contract"
                    },
                    "type": "File",
                    "id": "#package.cwl/contract"
                },
                {
                    "inputBinding": {
                        "position": 14,
                        "prefix": "--database"
                    },
                    "type": "File",
                    "id": "#package.cwl/database"
                },
                {
                    "inputBinding": {
                        "position": 12,
                        "prefix": "--evaluation-receipt"
                    },
                    "type": "File",
                    "id": "#package.cwl/evaluation-receipt"
                },
                {
                    "inputBinding": {
                        "position": 5,
                        "prefix": "--fault"
                    },
                    "type": "string",
                    "id": "#package.cwl/fault"
                },
                {
                    "inputBinding": {
                        "position": 3,
                        "prefix": "--input"
                    },
                    "type": "File",
                    "id": "#package.cwl/input"
                },
                {
                    "inputBinding": {
                        "position": 1
                    },
                    "type": "File",
                    "id": "#package.cwl/program"
                },
                {
                    "inputBinding": {
                        "position": 0
                    },
                    "type": "string",
                    "id": "#package.cwl/python"
                },
                {
                    "inputBinding": {
                        "position": 10,
                        "prefix": "--receipt"
                    },
                    "type": "File",
                    "id": "#package.cwl/receipt"
                },
                {
                    "inputBinding": {
                        "position": 11,
                        "prefix": "--report"
                    },
                    "type": "File",
                    "id": "#package.cwl/report"
                },
                {
                    "inputBinding": {
                        "position": 9,
                        "prefix": "--result"
                    },
                    "type": "File",
                    "id": "#package.cwl/result"
                },
                {
                    "inputBinding": {
                        "position": 13,
                        "prefix": "--spans"
                    },
                    "type": "File",
                    "id": "#package.cwl/spans"
                }
            ],
            "outputs": [
                {
                    "outputBinding": {
                        "glob": "bundle"
                    },
                    "type": "Directory",
                    "id": "#package.cwl/bundle"
                }
            ],
            "permanentFailCodes": [],
            "requirements": [
                {
                    "networkAccess": false,
                    "class": "NetworkAccess"
                }
            ],
            "stderr": "package.stderr",
            "stdout": "package.stdout",
            "successCodes": [
                0
            ],
            "id": "#package.cwl"
        },
        {
            "arguments": [
                {
                    "position": 2,
                    "valueFrom": "resume"
                }
            ],
            "class": "CommandLineTool",
            "inputs": [
                {
                    "inputBinding": {
                        "position": 7,
                        "prefix": "--anchor"
                    },
                    "type": "File",
                    "id": "#resume.cwl/anchor"
                },
                {
                    "inputBinding": {
                        "position": 6,
                        "prefix": "--checkpoint"
                    },
                    "type": "File",
                    "id": "#resume.cwl/checkpoint"
                },
                {
                    "inputBinding": {
                        "position": 4,
                        "prefix": "--contract"
                    },
                    "type": "File",
                    "id": "#resume.cwl/contract"
                },
                {
                    "inputBinding": {
                        "position": 5,
                        "prefix": "--fault"
                    },
                    "type": "string",
                    "id": "#resume.cwl/fault"
                },
                {
                    "inputBinding": {
                        "position": 3,
                        "prefix": "--input"
                    },
                    "type": "File",
                    "id": "#resume.cwl/input"
                },
                {
                    "inputBinding": {
                        "position": 1
                    },
                    "type": "File",
                    "id": "#resume.cwl/program"
                },
                {
                    "inputBinding": {
                        "position": 0
                    },
                    "type": "string",
                    "id": "#resume.cwl/python"
                }
            ],
            "outputs": [
                {
                    "outputBinding": {
                        "glob": "attempt-spans.json"
                    },
                    "type": "File",
                    "id": "#resume.cwl/attempt_spans_json"
                },
                {
                    "outputBinding": {
                        "glob": "effects.db"
                    },
                    "type": "File",
                    "id": "#resume.cwl/effects_db"
                },
                {
                    "outputBinding": {
                        "glob": "result.json"
                    },
                    "type": "File",
                    "id": "#resume.cwl/result_json"
                },
                {
                    "outputBinding": {
                        "glob": "resume-receipt.json"
                    },
                    "type": "File",
                    "id": "#resume.cwl/resume_receipt_json"
                }
            ],
            "permanentFailCodes": [
                22
            ],
            "requirements": [
                {
                    "networkAccess": false,
                    "class": "NetworkAccess"
                }
            ],
            "stderr": "resume.stderr",
            "stdout": "resume.stdout",
            "successCodes": [
                0
            ],
            "id": "#resume.cwl"
        },
        {
            "class": "Workflow",
            "inputs": [
                {
                    "type": "File",
                    "id": "#main/contract"
                },
                {
                    "type": "File",
                    "id": "#main/evaluator"
                },
                {
                    "type": "string",
                    "id": "#main/fault"
                },
                {
                    "type": "File",
                    "id": "#main/input"
                },
                {
                    "type": "File",
                    "id": "#main/program"
                },
                {
                    "type": "string",
                    "id": "#main/python"
                }
            ],
            "outputs": [
                {
                    "outputSource": "#main/package/bundle",
                    "type": "Directory",
                    "id": "#main/bundle"
                }
            ],
            "steps": [
                {
                    "in": [
                        {
                            "source": "#main/contract",
                            "id": "#main/checkpoint/contract"
                        },
                        {
                            "source": "#main/fault",
                            "id": "#main/checkpoint/fault"
                        },
                        {
                            "source": "#main/input",
                            "id": "#main/checkpoint/input"
                        },
                        {
                            "source": "#main/program",
                            "id": "#main/checkpoint/program"
                        },
                        {
                            "source": "#main/python",
                            "id": "#main/checkpoint/python"
                        }
                    ],
                    "out": [
                        "#main/checkpoint/checkpoint_json",
                        "#main/checkpoint/anchor_json",
                        "#main/checkpoint/checkpoint_receipt_json"
                    ],
                    "run": "#checkpoint.cwl",
                    "id": "#main/checkpoint"
                },
                {
                    "in": [
                        {
                            "source": "#main/contract",
                            "id": "#main/evaluate/contract"
                        },
                        {
                            "source": "#main/evaluator",
                            "id": "#main/evaluate/evaluator"
                        },
                        {
                            "source": "#main/fault",
                            "id": "#main/evaluate/fault"
                        },
                        {
                            "source": "#main/input",
                            "id": "#main/evaluate/input"
                        },
                        {
                            "source": "#main/program",
                            "id": "#main/evaluate/program"
                        },
                        {
                            "source": "#main/python",
                            "id": "#main/evaluate/python"
                        },
                        {
                            "source": "#main/resume/resume_receipt_json",
                            "id": "#main/evaluate/receipt"
                        },
                        {
                            "source": "#main/resume/result_json",
                            "id": "#main/evaluate/result"
                        }
                    ],
                    "out": [
                        "#main/evaluate/evaluation_report_json",
                        "#main/evaluate/evaluation_receipt_json"
                    ],
                    "run": "#evaluate.cwl",
                    "id": "#main/evaluate"
                },
                {
                    "in": [
                        {
                            "source": "#main/checkpoint/anchor_json",
                            "id": "#main/package/anchor"
                        },
                        {
                            "source": "#main/checkpoint/checkpoint_json",
                            "id": "#main/package/checkpoint"
                        },
                        {
                            "source": "#main/checkpoint/checkpoint_receipt_json",
                            "id": "#main/package/checkpoint-receipt"
                        },
                        {
                            "source": "#main/contract",
                            "id": "#main/package/contract"
                        },
                        {
                            "source": "#main/resume/effects_db",
                            "id": "#main/package/database"
                        },
                        {
                            "source": "#main/evaluate/evaluation_receipt_json",
                            "id": "#main/package/evaluation-receipt"
                        },
                        {
                            "source": "#main/fault",
                            "id": "#main/package/fault"
                        },
                        {
                            "source": "#main/input",
                            "id": "#main/package/input"
                        },
                        {
                            "source": "#main/program",
                            "id": "#main/package/program"
                        },
                        {
                            "source": "#main/python",
                            "id": "#main/package/python"
                        },
                        {
                            "source": "#main/resume/resume_receipt_json",
                            "id": "#main/package/receipt"
                        },
                        {
                            "source": "#main/evaluate/evaluation_report_json",
                            "id": "#main/package/report"
                        },
                        {
                            "source": "#main/resume/result_json",
                            "id": "#main/package/result"
                        },
                        {
                            "source": "#main/resume/attempt_spans_json",
                            "id": "#main/package/spans"
                        }
                    ],
                    "out": [
                        "#main/package/bundle"
                    ],
                    "run": "#package.cwl",
                    "id": "#main/package"
                },
                {
                    "in": [
                        {
                            "source": "#main/checkpoint/anchor_json",
                            "id": "#main/resume/anchor"
                        },
                        {
                            "source": "#main/checkpoint/checkpoint_json",
                            "id": "#main/resume/checkpoint"
                        },
                        {
                            "source": "#main/contract",
                            "id": "#main/resume/contract"
                        },
                        {
                            "source": "#main/fault",
                            "id": "#main/resume/fault"
                        },
                        {
                            "source": "#main/input",
                            "id": "#main/resume/input"
                        },
                        {
                            "source": "#main/program",
                            "id": "#main/resume/program"
                        },
                        {
                            "source": "#main/python",
                            "id": "#main/resume/python"
                        }
                    ],
                    "out": [
                        "#main/resume/result_json",
                        "#main/resume/resume_receipt_json",
                        "#main/resume/attempt_spans_json",
                        "#main/resume/effects_db"
                    ],
                    "run": "#resume.cwl",
                    "id": "#main/resume"
                }
            ],
            "id": "#main"
        }
    ],
    "cwlVersion": "v1.2"
}