# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, REFLOW_WORKFLOWS, sanitize_path

import json
import subprocess

import click
import pandas as pd

from .reflow_utils import write_config, write_samples
from .s3_utils import S3_INPUT_PATH, get_fastqs_as_r1_r2_columns


REGION = 'west'
WORKFLOW = 'rnaseq.rf'

# Taxons (species) with available references
SUPPORTED_TAXA = ('mus',)
TAXA_GENOMES = {'mus': 'mouse/vM19'}


@click.command(short_help="Submit the first line of a reflow runbatch "
                          "samples.csv to check for errors")
@click.option("--path", default='.',
              help="Where to look for samples.csv and config.json files. "
                   "Default is the current directory")
def check_batch(path):
    """Reflow run the first line of a samples.csv"""
    path = sanitize_path(path)

    samples = pd.read_csv(os.path.join(path, 'samples.csv'), index_col=0)

    with open(os.path.join(path, 'config.json')) as f:
        config = json.load(f)

    program = config['program']

    first_row = samples.iloc[0]
    arguments = []
    for key, value in first_row.items():
        arguments.append(f'-{key}')
        arguments.append(str(value))

    command = ["reflow", "run", program] + arguments
    print(command)

    click.echo(f"Running '{' '.join(command)}'")
    subprocess.run(command)
