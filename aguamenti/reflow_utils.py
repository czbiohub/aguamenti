import click
import json
import os


def write_config(csv_filename, output, reflow_workflows_path, workflow):
    """Write config.json to path with workflow and samples files"""
    rf = os.path.join(reflow_workflows_path, workflow)
    config = {"program": rf, "runs_file": csv_filename}
    json_filename = os.path.join(output, 'config.json')
    click.echo(f"Writing {json_filename} ...")
    with open(json_filename, 'w') as f:
        json.dump(config, f)
    click.echo("\tDone.")


def write_samples(output, samples):
    """Write samples.csv file to path

    Parameters
    ----------
    output : str
        Folder to write samples.csv file to
    samples : pandas.DataFrame
        Dataframe containing samples for reflow runbatch

    Returns
    -------
    csv : str
        Full path to the output samples.csv
    """
    csv = os.path.join(output, 'samples.csv')
    click.echo(f"Writing {csv} ...")
    samples.to_csv(csv)
    click.echo("\tDone.")
    return csv
