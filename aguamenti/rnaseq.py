import os

import click
import pandas as pd
import utilities.s3_util as s3u


# USA unicode encoding setting
# Necessary because click assumes ascii input unless otherwise specified
# https://click.palletsprojects.com/en/7.x/python3/
unicode_usa = 'en_US.utf-8'
os.environ['LC_LANG'] = unicode_usa
os.environ["LC_ALL"] = unicode_usa

S3_REFERENCE = {"east": "czi-hca", "west": "czbiohub-reference"}
SAMPLE_REGEX = r'(?P<id>[^/]+)_(?P<read_number>R\d)_\d+.fastq.gz$'
S3_INPUT_PATH = "s3://czb-seqbot/fastqs"
S3_REFERENCE = "s3://czbiohub-reference"
REGION = 'west'

# Taxons (species) with available references
SUPPORTED_TAXA = ('mus',)
TAXA_GENOMES = {'mus': 'mouse/vM19'}


def maybe_add_slash(path):
    """Add a final trailing slash if it wasn't there already"""
    with_trailing_slash = path if path.endswith('/') else path + '/'
    return with_trailing_slash


def get_fastqs_as_r1_r2_columns(experiment_id, s3_input_path=S3_INPUT_PATH):
    """Create a dataframe with a sample per row, and R1 and R2 fastqs in cols

    Parameters
    ----------
    experiment_id : str
        Experiment id from Illumina sequencing run, as a folder in
        s3_input_path
    s3_input_path : str


    Returns
    -------
    samples : pandas.DataFrame
        A (n_samples, 2) dataframe containing the full path to the fastq.gz
        for each sample. Each row is a single sample, and the columns are
        'read1' and 'read2'.

    """
    s3_input_bucket, s3_input_prefix = s3u.s3_bucket_and_key(
        s3_input_path)

    data = [
        (filename, size)
        for filename, size in s3u.get_size(
            s3_input_bucket, os.path.join(s3_input_prefix, experiment_id)
        )
        if filename.endswith("fastq.gz")
    ]

    s3_input_bucket = maybe_add_slash(s3_input_bucket)

    fastqs = pd.DataFrame(data, columns=['filename', 'size'])
    fastqs['full_path'] = s3_input_bucket + fastqs['filename']
    fastqs['basename'] = fastqs.filename.map(os.path.basename)
    read_data = fastqs.basename.str.extractall(SAMPLE_REGEX)
    read_data.index = read_data.index.droplevel(-1)
    fastqs_with_data = pd.concat([fastqs, read_data], axis=1)

    # Transform so R1 and R2 are column names, and the values are the paths
    # Each row is a single sample
    samples = fastqs_with_data.pivot(index='id', columns='read_number',
                                     values='full_path')
    samples = samples.rename(columns={'R1': 'read1', "R2": "read2"})
    return samples


@click.command(short_help="Create a csv of samples to input to reflow runbatch"
                          " for RNA-seq alignment and gene counting")
@click.argument("experiment_id")
@click.argument("taxon")
@click.argument('s3_output_path')
@click.option("--s3-input-path", default=S3_INPUT_PATH,
              help="Location of input folders")
@click.option('--region', default='west')
def align(experiment_id, taxon, s3_output_path, s3_input_path=S3_INPUT_PATH,
          region=REGION):
    """

    Parameters
    ----------
    experiment_id : str
        A string of the form `YYMMDD_EXP_ID`, a folder in the --s3-input-path
        argument. e.g. "20181030_FS10000331_12_BNT40322-1214"
    taxon : str
        Only "mus" (mouse) is valid now, more will be added later
    s3_output_path : str
        Where to output the aligned files to

    Returns
    -------

    """
    assert taxon in SUPPORTED_TAXA
    samples = get_fastqs_as_r1_r2_columns(experiment_id, s3_input_path)
    samples['name'] = samples.index
    samples['genome'] = TAXA_GENOMES[taxon]
    samples['output'] = s3_output_path
    click.echo(samples.to_csv())


if __name__ == "__main__":
    align()
