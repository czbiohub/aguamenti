# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, REFLOW_WORKFLOWS, sanitize_path


import click

from .reflow_utils import write_config, write_samples
from .s3_utils import S3_INPUT_PATH, get_fastqs_as_r1_r2_columns


REGION = 'west'

# Taxons (species) with available references
SUPPORTED_TAXA = ('mus',)
TAXA_GENOMES = {'mus': 'mouse/vM19'}


@click.command(short_help="Create a csv of samples to input to reflow runbatch"
                          " for RNA-seq alignment and gene counting")
@click.argument("experiment_id")
@click.argument("taxon")
@click.argument('s3_output_path')
@click.option("--s3-input-path", default=S3_INPUT_PATH,
              help="Location of input folders")
@click.option('--output', default='.',
              help='Where to output the samples.csv and config.json files to.'
                   ' Default is the current directory.')
@click.option('--reflow-workflows-path', default=REFLOW_WORKFLOWS,
              help='Location of reflow-workflows directory containing .rf '
                   'files')
@click.option('--region', default=REGION,
              help="Either 'east' or 'west', depending on where your fastq "
                   "files are")
@click.option('--workflow', default='star_htseq.rf',
              help="Which workflow to run on these files")
def align(experiment_id, taxon, s3_output_path, s3_input_path=S3_INPUT_PATH,
          output='.', reflow_workflows_path=REFLOW_WORKFLOWS,
          region=REGION, workflow='star_htseq.rf'):
    """Create a samples.csv file

    \b
    Parameters
    ----------
    experiment_id : str
        A string of the form `YYMMDD_EXP_ID`, a folder in the --s3-input-path
        argument. e.g. "20181030_FS10000331_12_BNT40322-1214"
    taxon : str
        Only "mus" (mouse) is valid now, more will be added later
    s3_output_path : str
        Where to output the aligned files to
    s3_input_path : str
        Where the input unaligned fastqs are coming from, default is
        's3://czb-seqbot/fastqs'
    """
    output = sanitize_path(output)
    reflow_workflows_path = sanitize_path(reflow_workflows_path)

    # Make the output directory if it's not already there
    os.makedirs(output, exist_ok=True)

    # Check that the taxa actually has a reference genome, otherwise
    # no alignment :(
    assert taxon in SUPPORTED_TAXA

    # Get dataframe with 1 sample per row, read1 and read2 as columns
    samples = get_fastqs_as_r1_r2_columns(experiment_id, s3_input_path)

    # Set parameters for star_htseq.rf
    samples['name'] = samples.index
    samples['genome'] = TAXA_GENOMES[taxon]
    samples['output'] = s3_output_path
    samples['region'] = region

    # Write filenames
    csv_filename = write_samples(output, samples)
    write_config(csv_filename, output, reflow_workflows_path, workflow)
