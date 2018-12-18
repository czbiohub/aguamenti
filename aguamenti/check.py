# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, sanitize_path, get_stdout_from_command

from itertools import chain
import json
import subprocess

import click
import pandas as pd

from .reflow_utils import SAMPLES_CSV, CONFIG_JSON, read_config, read_samples
from .s3_utils import S3_INPUT_PATH, get_fastqs_as_r1_r2_columns


REGION = 'west'
WORKFLOW = 'rnaseq.rf'

# Taxons (species) with available references
SUPPORTED_TAXA = ('mus',)
TAXA_GENOMES = {'mus': 'mouse/vM19'}

def get_parameter_order(reflow_program):
    lines = get_stdout_from_command(["reflow", "doc", reflow_program])

    # Save the parameters from the command
    parameter_order = []
    for line in lines:
        if line.startswith('val'):
            val, parameter, *rest = line.split()
            parameter_order.append(parameter)

        # First section is always parameters, then function definitions.
        # Ignore all function definitions since they're not parameters
        if line.startswith('Declarations'):
            break
    return parameter_order


@click.command(short_help="Submit the first line of a reflow runbatch "
                          "samples.csv to check for errors")
@click.option("--path", default='.',
              help="Where to look for samples.csv and config.json files. "
                   "Default is the current directory")
def check_batch(path):
    """Reflow run the first line of a samples.csv"""
    path = sanitize_path(path)

    samples = read_samples(os.path.join(path, SAMPLES_CSV))
    config = read_config(os.path.join(path, CONFIG_JSON))

    program = config['program']

    parameter_order = get_parameter_order(program)

    first_row = samples.iloc[0]
    arguments = {}
    for key, value in first_row.items():
        arguments[key] = str(value)

    arguments_ordered = list(chain(*[
        # Add '-' before parameter name to show it's a flag
        (f"-{param}", arguments[param]) for param in parameter_order
    ]))

    command = ["reflow", "run", program] + arguments_ordered

    click.echo("---")
    click.echo(f"Running '{' '.join(command)}'")
    click.echo("---")
    subprocess.run(command)
