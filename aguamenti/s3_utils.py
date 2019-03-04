from .os_utils import os, maybe_add_slash


import warnings

from tqdm import tqdm
from utilities import s3_util as s3u

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    import pandas as pd


S3_REFERENCE = {"east": "czbiohub-reference-east",
                "west": "czbiohub-reference"}
SAMPLE_REGEX = r'(?P<id>[^/]+)_(?P<read_number>R\d)_\d+.fastq.gz$'
SRA_SAMPLE_REGEX = r'(?P<id>[\w]+)_(?P<read_number>[12]).fastq.gz$'

REGEX_TO_READ_ID = {SAMPLE_REGEX: ("R1", "R2"),
                   SRA_SAMPLE_REGEX: ("1", "2")}
S3_INPUT_PATH = "s3://czb-seqbot/fastqs"

def _extract_r1_r2(data, s3_input_bucket):
    fastqs = pd.DataFrame(data, columns=['filename', 'size'])
    fastqs['full_path'] = 's3://' + s3_input_bucket + fastqs['filename']
    fastqs['basename'] = fastqs.filename.map(os.path.basename)

    for REGEX, (read1, read2) in REGEX_TO_READ_ID.items():
        read_data = fastqs.basename.str.extractall(REGEX)

        # If this regex didn't extract anything, try the other one
        if read_data.empty:
            continue
        read_data.index = read_data.index.droplevel(-1)
        fastqs_with_data = pd.concat([fastqs, read_data], axis=1)
        # Transform so R1 and R2 are column names, and the values are the paths
        # Each row is a single sample
        samples = fastqs_with_data.pivot(index='id', columns='read_number',
                                         values='full_path')
        samples = samples.rename(columns={read1: 'read1', read2: "read2"})

    return samples


def get_fastqs_as_r1_r2_columns(subfolder="", s3_input_path=S3_INPUT_PATH):
    """Create a dataframe with a sample per row, and R1 and R2 fastqs in cols

    Parameters
    ----------
    subfolder : str
        Subfolder of s3_input_path, e.g. an experiment ID from an Illumina
        sequencing run
    s3_input_path : str
        Prefix of the S3 folder/bucket, including "s3://"

    Returns
    -------
    samples : pandas.DataFrame
        A (n_samples, 2) dataframe containing the full path to the fastq.gz
        for each sample. Each row is a single sample, and the columns are
        'read1' and 'read2'.

    """
    # Add a final slash if it's not already there to ensure we're searching
    # subfolders
    s3_input_path = maybe_add_slash(s3_input_path)

    s3_input_bucket, s3_input_prefix = s3u.s3_bucket_and_key(
        s3_input_path)

    path_to_search = os.path.join(s3_input_prefix, subfolder)

    print(f"Recursively searching s3://{s3_input_bucket}/{path_to_search}"
          " for fastq.gz files ...")

    data = [
        (filename, size)
        for filename, size in tqdm(s3u.get_size(
            s3_input_bucket, os.path.join(s3_input_prefix, subfolder)
        ))
        if filename.endswith("fastq.gz")
    ]
    print(f"\tDone. Found {len(data)} fastq.gz files")

    s3_input_bucket = maybe_add_slash(s3_input_bucket)

    samples = _extract_r1_r2(data, s3_input_bucket)
    print(f"\tDone. Found {len(samples)} samples' reads (single or paired)")


    return samples
