import json
import os
import warnings

import click

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd


import pandas as pd


SAMPLES_CSV = 'samples.csv'
CONFIG_JSON = 'config.json'


def write_config(csv_filename, output, reflow_workflows_path, workflow):
    """Write config.json to path with workflow and samples files"""
    rf = os.path.join(reflow_workflows_path, workflow)
    config = {"program": rf, "runs_file": os.path.basename(csv_filename)}
    json_filename = os.path.join(output, CONFIG_JSON)
    click.echo(f"Writing {json_filename} ...")
    with open(json_filename, 'w') as f:
        json.dump(config, f)
    click.echo("\tDone.")


def write_samples(output, samples):
    """Write samples.csv file to path"""
    csv = os.path.join(output, SAMPLES_CSV)
    click.echo(f"Writing {csv} ...")
    samples.to_csv(csv)
    click.echo("\tDone.")
    return csv


def read_config(config_filename):
    with open(config_filename) as f:
        config = json.load(f)
    return config


def read_samples(csv_filename):
    return pd.read_csv(csv_filename, index_col=0)
