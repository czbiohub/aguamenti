
import pytest


def test_rnaseq():
    from aguamenti.rnaseq import align

    experiment_id = '20181030_FS10000331_12_BNT40322-1214'
    taxon = 'mus'
    s3_output = 's3://olgabot-maca/aguamenti-test/'

    align(experiment_id, taxon, s3_output)
