# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, REFLOW_WORKFLOWS, sanitize_path # noqa: F401


import click
import pandas as pd

from .reflow_utils import write_config, write_samples
from .s3_utils import S3_INPUT_PATH, get_fastqs_as_r1_r2_columns
from .rnaseq import _align

REGION = 'west'
WORKFLOW = 'rnaseq.rf'

# Taxons (species) with available references
SUPPORTED_TAXA = ('mus',)
TAXA_GENOMES = {'mus': 'mouse/vM19'}


@click.command(short_help="Create run batch jobs for every experiment ID in "
                          "the input.")
@click.argument("parameters_csv")
@click.option('--output', default='.',
              help='Where to output the samples.csv and config.json files to.'
                   ' Default is the current directory.')
@click.option('--reflow-workflows-path', default=REFLOW_WORKFLOWS,
              help='Location of reflow-workflows directory containing .rf '
                   'files')
@click.option('--workflow', default=WORKFLOW,
              help="Which workflow to run on these files")
def wrap(parameters_csv, output='.', reflow_workflows_path=REFLOW_WORKFLOWS,
         workflow=WORKFLOW):
    """Create folders for each experiment ID in parameters_csv that
    contain the samples.csv and config.json for reflow runbatch

    \b
    Parameters
    ----------
    parameters_csv : str
        A csv file with column names that are are the input parameters
        for aguamenti rnaseq-align function. Inputs are EXPERIMENT_ID,
        TAXON, S3_INPUT_PATH, and S3_OUTPUT_PATH

    """
    print(f"parameters_csv: {parameters_csv}")
    # Import the csv as pandas df
    data = pd.read_csv(parameters_csv)

    # Make directories for every experiment ID in the list
    dfs = []
    for i, row in data.iterrows():
        reflow_batch_output = sanitize_path(
            os.path.join("~", "reflow-batches", 'rnaseq', 'mus',
                              row['experiment_id']))
        df = _align(output=reflow_batch_output, **row)
        dfs.append(df)
    samples = pd.concat(dfs)

    # Write concatonated samples.csv and a single json for all
    csv_filename = write_samples(output, samples)
    write_config(csv_filename, output, reflow_workflows_path, workflow)
