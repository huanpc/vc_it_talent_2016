import os
import pprint

# add logging to output errors to stdout
import logging
logging.basicConfig()

from nupic.swarming import permutations_runner
from swarm_description import SWARM_DESCRIPTION
from convert import convert_json_to_csv

INPUT_FILE = "test.csv"
DESCRIPTION = (
    "This script runs a swarm on the input data (test.csv) and\n"
    "creates a model parameters file in the `model_params` directory containing\n"
    "the best model found by the swarm. Dumps a bunch of crud to stdout because\n"
    "that is just what swarming does at this point. You really don't need to\n"
    "pay any attention to it.\n"
)


def model_params_to_string(model_params):
    pp = pprint.PrettyPrinter(indent=2)
    return pp.pformat(model_params)


def write_model_params_to_file(model_params, name):
    clean_name = name.replace(" ", "_").replace("-", "_")
    params_name = "%s_model_params.py" % clean_name
    out_dir = os.path.join(os.getcwd(), 'model_params')
    if not os.path.isdir(out_dir):
        os.mkdir(out_dir)
    out_path = os.path.join(os.getcwd(), 'model_params', params_name)
    with open(out_path, "wb") as out_file:
        model_params_string = model_params_to_string(model_params)
        out_file.write("MODEL_PARAMS = \\\n%s" % model_params_string)
    return out_path


def swarm_for_best_model_params(swarm_config, name, max_workers=4):
    output_label = name
    perm_work_dir = os.path.abspath('swarm')
    if not os.path.exists(perm_work_dir):
        os.mkdir(perm_work_dir)
    model_params = permutations_runner.runWithConfig(
        swarm_config,
        {"maxWorkers": max_workers, "overwrite": True},
        outputLabel=output_label,
        outDir=perm_work_dir,
        permWorkDir=perm_work_dir,
        verbosity=0
    )
    model_params_file = write_model_params_to_file(model_params, name)
    return model_params_file


def print_swarm_size_warning(size):
    if size is "small":
        print "= THIS IS A DEBUG SWARM. DON'T EXPECT YOUR MODEL RESULTS TO BE GOOD."
    elif size is "medium":
        print "= Medium swarm. Sit back and relax, this could take awhile."
    else:
        print "= LARGE SWARM! Might as well load up the Star Wars Trilogy."


def swarm(file_path):
    name = os.path.splitext(os.path.basename(file_path))[0]
    print "================================================="
    print "= Swarming on %s data..." % name
    print_swarm_size_warning(SWARM_DESCRIPTION["swarmSize"])
    print "================================================="
    model_params = swarm_for_best_model_params(SWARM_DESCRIPTION, name)
    print "\nWrote the following model param files:"
    print "\t%s" % model_params


if __name__ == "__main__":
    print DESCRIPTION
    convert_json_to_csv('test.json')
    swarm(INPUT_FILE)
