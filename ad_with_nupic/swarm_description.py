SWARM_DESCRIPTION = None


def set_swarm_description(input_path, max_value, min_value):
    global SWARM_DESCRIPTION
    SWARM_DESCRIPTION = {
        "includedFields": [
            {
                "fieldName": "timestamp",
                "fieldType": "datetime"
            },
            {
                "fieldName": "value",
                "fieldType": "float",
                "maxValue": max_value,
                "minValue": min_value
            }
        ],
        "streamDef": {
            "info": "value",
            "version": 1,
            "streams": [
                {
                    "info": "Metric Value",
                    "source": "file://" + input_path,
                    "columns": [
                        "*"
                    ]
                }
            ]
        },

        "inferenceType": "TemporalAnomaly",
        "inferenceArgs": {
            "predictionSteps": [
                1
            ],
            "predictedField": "value"
        },
        "iterationCount": -1,
        "swarmSize": "medium"
    }
