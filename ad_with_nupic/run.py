import importlib
import sys
import csv
from datetime import datetime

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

import nupic_anomaly_output

from convert import convert_json_to_csv

DESCRIPTION = (
    "Starts a NuPIC model from the model params returned by the swarm\n"
    "and pushes each line of input from the gym into the model. Results\n"
    "are written to an output file (default) or plotted dynamically if\n"
    "the --plot option is specified.\n"
)

METRIC_NAME = "test"
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"
# '1970-01-01 08:00:01'
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def create_model(model_params):
    model = ModelFactory.create(model_params)
    model.enableInference({"predictedField": "value"})
    return model


def get_model_params_from_name(metric_name):
    import_name = "model_params.%s_model_params" % (
        metric_name.replace(" ", "_").replace("-", "_")
    )
    print "Importing model params from %s" % import_name
    try:
        imported_model_params = importlib.import_module(
            import_name).MODEL_PARAMS
    except ImportError:
        raise Exception("No model params exist for '%s'. Run swarm first!"
                        % metric_name)
    return imported_model_params


def run_io_through_nupic(input_data, model, metric_name, plot):
    input_file = open(input_data, "rb")
    csv_reader = csv.reader(input_file)
    # skip header rows
    csv_reader.next()
    csv_reader.next()
    csv_reader.next()

    shifter = InferenceShifter
    if plot:
        output = nupic_anomaly_output.NuPICPlotOutput(metric_name)
    else:
        output = nupic_anomaly_output.NuPICFileOutput(metric_name)

    counter = 0
    for row in csv_reader:
        counter += 1
        if (counter % 100 == 0):
            print "Read %i lines..." % counter
        timestamp = datetime.strptime(row[1], DATE_FORMAT)
        value = float(row[0])
        result = model.run({
            "timestamp": timestamp,
            "value": value
        })

        if plot:
            result = shifter.shift(result)

        print "Line %d" % counter

        prediction = result.inferences["multiStepBestPredictions"][1]
        anomaly_score = result.inferences["anomalyScore"]
        output.write(timestamp, value, prediction, anomaly_score)

    input_file.close()
    output.close()


def run_model(metric_name, plot=False):
    print "Creating model from %s..." % metric_name
    model = create_model(get_model_params_from_name(metric_name))
    input_data = "%s/%s.csv" % (DATA_DIR, metric_name.replace(" ", "_"))
    run_io_through_nupic(input_data, model, metric_name, plot)

if __name__ == "__main__":
    print DESCRIPTION
    plot = False
    args = sys.argv[1:]
    if "--plot" in args:
        plot = True

    convert_json_to_csv('test.json')

    run_model(METRIC_NAME, plot=plot)
