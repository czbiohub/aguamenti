import click
import json
import os

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
