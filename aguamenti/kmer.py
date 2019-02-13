# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, REFLOW_WORKFLOWS, sanitize_path


import click

from .reflow_utils import write_config, write_samples
from .s3_utils import S3_INPUT_PATH, get_fastqs_as_r1_r2_columns


WORKFLOW = "kmer_similarity.rf"
LOG2_SKETCH_SIZE = 10

@click.command(short_help="Calculate kmer distance of all samples in a "
                          "directory. Combines R1 and R2 reads")
@click.argument("s3_input_path")
@click.argument("ksize")
@click.argument('s3_output_path')
@click.option("--log2-sketch-size", default=LOG2_SKETCH_SIZE,
              help="Use 2**log2_sketch_size hashes")
@click.option('--output', default='.',
              help='Where to output the samples.csv and config.json files to.'
                   ' Default is the current directory.')
@click.option('--reflow-workflows-path', default=REFLOW_WORKFLOWS,
              help='Location of reflow-workflows directory containing .rf '
                   f'files where you will run the workflow. ' \
                    'Default: {REFLOW_WORKFLOWS}')
@click.option('--workflow', default=WORKFLOW,
              help="Which workflow to run on these files. "
                   f"Default: {WORKFLOW}")
def similarity(s3_input_path, ksize, s3_output_path,
          log2_sketch_size=LOG2_SKETCH_SIZE,
          output='.', reflow_workflows_path=REFLOW_WORKFLOWS,
          workflow=WORKFLOW):
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

    """
    output = sanitize_path(output)
    reflow_workflows_path = sanitize_path(reflow_workflows_path)

    # Make the output directory if it's not already there
    os.makedirs(output, exist_ok=True)

    # Get dataframe with 1 sample per row, read1 and read2 as columns
    samples = get_fastqs_as_r1_r2_columns(s3_input_path=s3_input_path)

    # Set parameters for star_htseq.rf
    samples['name'] = samples.index
    samples['output'] = s3_output_path
    samples['ksize'] = ksize
    samples['log2_sketch_size'] = log2_sketch_size

    # Write filenames
    csv_filename = write_samples(output, samples)
    write_config(csv_filename, output, reflow_workflows_path, workflow)
