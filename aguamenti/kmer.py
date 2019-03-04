# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, REFLOW_WORKFLOWS, sanitize_path

from itertools import product

import click
import pandas as pd


from .reflow_utils import write_config, write_samples
from .s3_utils import get_fastqs_as_r1_r2_columns, maybe_add_slash


WORKFLOW = "kmer_similarity.rf"
KSIZES = "21,27,33,51"
LOG2_SKETCH_SIZES = "8,9,10,11,12,13,14,15,16"


def intify(s):
    """Given string containing comma-separated integers, return the integers

    >>> intify("1,2,3")
    [1, 2, 3]
    """
    return sorted(list(set([int(x.strip()) for x in s.split(",")])))


def get_reads_per_comparison(s3_input_paths, name):
    dfs = []
    for s3_input_path in s3_input_paths.split(","):
        df = get_fastqs_as_r1_r2_columns(s3_input_path=s3_input_path)
        dfs.append(df)
    fastqs = pd.concat(dfs)

    print(f"Combining all {len(fastqs)} samples for comparison ...")
    # Glue together read1 and read2 into single line
    read1s = ';'.join(fastqs['read1'])
    read2s = ';'.join(fastqs['read2'])
    sample_names = ";".join(fastqs.index)
    samples = pd.DataFrame(dict(read1s=read1s, read2s=read2s,
                                names=sample_names), index=[name])
    print("\tDone.")
    return samples

@click.command(short_help="Calculate kmer distance of all samples in a "
                          "directory. Combines R1 and R2 reads into one "
                          "sample")
@click.argument("s3_input_paths")
@click.argument('s3_output_path')
@click.option("--name", "-n",
              default="kmer_similarity",
              help=f"If provided, prefixes the csvs with this name. If not "
                   "provided, uses the last folder in s3_input_path")
@click.option("--ksizes", "-k",
              default=KSIZES,
              help=f"Which kmer size to compare. Default: '{KSIZES}'")
@click.option("--log2-sketch-sizes", "-s",
              default=LOG2_SKETCH_SIZES,
              help=f"Use 2**log2_sketch_size hashes. Default: "
                   "'{LOG2_SKETCH_SIZES}'")
@click.option('--output', default='.',
              help='Where to output the samples.csv and config.json files to.'
                   ' Default is the current directory.')
@click.option('--reflow-workflows-path', default=REFLOW_WORKFLOWS,
              help='Location of reflow-workflows directory containing .rf '
                   'files where you will run the workflow. '
                   f'Default: {REFLOW_WORKFLOWS}')
@click.option('--workflow', default=WORKFLOW,
              help="Which workflow to run on these files. "
                   f"Default: {WORKFLOW}")
@click.option('--method', default="minhash",
              type=click.Choice(["minhash", "hyperloglog", "truejaccard"]),
              help='Which method to use for estimating a jaccard similarity '
                   'of k-mer overlap')
@click.option('--molecule', default="dna",
              type=click.Choice(["dna", "protein"]),
              help='Which molecule to compare on. Default is "dna". Only '
                   'minhash can use "protein"')
def similarity(s3_input_paths, s3_output_path, name=None,
               ksizes=KSIZES,
               log2_sketch_sizes=LOG2_SKETCH_SIZES,
               output='.', reflow_workflows_path=REFLOW_WORKFLOWS,
               workflow=WORKFLOW, method='minhash', molecule='DNA'):
    """Create a samples.csv file

    \b
    Parameters
    ----------
    s3_input_path : str
        Full path to a s3 folder containing fastq files. Multiple paths can be
        specified as a comma-separated list, e.g.:
        s3://bucket1/path1,s3://bucket2/path2
    s3_output_path : str
        Where to output the csvs of comparison to

    """
    s3_output_path = maybe_add_slash(s3_output_path)

    output = sanitize_path(output)
    reflow_workflows_path = sanitize_path(reflow_workflows_path)

    # Make the output directory if it's not already there
    os.makedirs(output, exist_ok=True)

    # Get dataframe with 1 sample per row, read1 and read2 as columns
    samples = get_reads_per_comparison(s3_input_paths, name)

    # Add all parameters and make full samples
    ksizes = intify(ksizes)
    log2_sketch_sizes = intify(log2_sketch_sizes)

    click.echo(f"Preparing Reflow runbatch to compare {len(samples)} samples "
               "with ..."
               f"\n\tmethod: {method}, "
               f"\n\tksizes: {ksizes}, "
               f"\n\tlog2_sketch_sizes: {log2_sketch_sizes}"
               f"\n\tmolecule: {molecule}")
    parameters = pd.DataFrame(list(product([name], ksizes, log2_sketch_sizes)),
                              columns=['name', 'ksize', 'log2_sketch_size'])
    parameters = parameters.set_index('name')
    samples = samples.join(parameters)
    template = "_ksize-{ksize}_log2sketchsize-{log2_sketch_size}"

    samples['id'] = samples.apply(lambda x: x.name + template.format(**x),
                                  axis=1)
    samples['output'] = samples.apply(
        lambda x: s3_output_path + x['id'] + '.csv', axis=1)
    samples = samples.set_index('id')

    # Write filenames
    csv_filename = write_samples(output, samples)
    write_config(csv_filename, output, reflow_workflows_path, workflow)
