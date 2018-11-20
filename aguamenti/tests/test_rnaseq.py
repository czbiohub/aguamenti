import sys

sys.path.append('..')

import pytest


def test_make_star_htseq_batch():
    from ..make_star_htseq_batch import cli

    experiment_id = '20181030_FS10000331_12_BNT40322-1214'
    taxon = 'mus'

    cli(experiment_id, taxon)