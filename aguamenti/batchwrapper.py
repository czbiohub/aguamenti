# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, REFLOW_WORKFLOWS, REFLOW_BATCHES

import click
import pandas as pd

from .reflow_utils import write_config, write_samples
from .rnaseq import _align

REGION = 'west'
WORKFLOW = 'rnaseq.rf'

# Taxons (species) with available references
SUPPORTED_TAXA = ('mus',)
TAXA_GENOMES = {'mus': 'mouse/vM19'}


@click.command(short_help="Create run batch jobs for every experiment ID in "
                          "the input.")
@click.argument("parameters_csv")
@click.argument("project_name")
@click.option('--reflow-workflows-path', default=REFLOW_WORKFLOWS,
              help='Location of reflow-workflows directory containing .rf '
                   f'files. Default: {REFLOW_WORKFLOWS}')
@click.option('--output', default=REFLOW_BATCHES,
              help="Location of reflow-batches directory containing "
                   "config.json and samples.csv files. "
                   f"Default: {REFLOW_BATCHES}")
@click.option('--workflow', default=WORKFLOW,
              help="Which workflow to run on these files")
@click.option('--merge-split-runs', default=False,
              help="Align read pairs from split runs at once. Output "
                   "location for the alignment must be the same. "
              )
def wrap(parameters_csv, project_name,
         reflow_workflows_path=REFLOW_WORKFLOWS,
         output=REFLOW_BATCHES,
         workflow=WORKFLOW, merge_split_runs=False):
    """Create folders for each experiment ID in parameters_csv that
    contain the samples.csv and config.json for reflow runbatch

    \b
    Parameters
    ----------
    parameters_csv : str
        A csv file with column names that are are the input parameters
        for reflow runbatch with rnaseq workflow. Inputs are EXPERIMENT_ID,
        TAXON, S3_INPUT_PATH, and S3_OUTPUT_PATH

    """
    print(f"parameters_csv: {parameters_csv}")
    # Import the csv as pandas df
    data = pd.read_csv(parameters_csv)

    # Get the workflow name and generate an output dir for the sample file
    # and json in reflow_batches dir
    workflow_name = workflow.split('.')[0]

    output = os.path.join(output, workflow_name,
                          project_name)
    os.makedirs(output, exist_ok=True)

    # Make directories for every experiment ID in the list
    dfs = []
    for i, row in data.iterrows():
        df = _align(write=False, **row)
        dfs.append(df)
    samples = pd.concat(dfs)

    # Concatonate samples if runs were split
    if merge_split_runs is True:
        pass

        # n_merged = merged_samples.shape[0]
        # click.echo(f"Merged samples to {n_merged} fastq.gz R1,
        # R2 read pairs")

    # Write concatenated samples.csv and a single json for all
    click.echo(f"Writing mega csv of all input samples to this folder: "
               f"{output}")
    csv_filename = write_samples(output, samples)
    write_config(csv_filename, output, reflow_workflows_path, workflow)
