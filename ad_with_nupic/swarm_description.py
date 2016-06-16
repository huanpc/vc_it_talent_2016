SWARM_DESCRIPTION = {
    "includedFields": [
        {
            "fieldName": "timestamp",
            "fieldType": "datetime"
        },
        {
            "fieldName": "value",
            "fieldType": "float",
            "maxValue": 0.5,
            "minValue": 0.0
        }
    ],
    "streamDef": {
        "info": "value",
        "version": 1,
        "streams": [
            {
                "info": "Metric Value",
                "source": "file://test.csv",
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
