import convert

SWARM_DESCRIPTION = {
    "includedFields": [
        {
            "fieldName": "timestamp",
            "fieldType": "datetime"
        },
        {
            "fieldName": "value",
            "fieldType": "float",
            "maxValue": convert.MAX,
            "minValue": convert.MIN
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
