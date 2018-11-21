#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from click.testing import CliRunner
import pytest
import pandas as pd
import pandas.testing as pdt


@pytest.fixture
def experiment_id():
    return '20181030_FS10000331_12_BNT40322-1214'


@pytest.fixture
def taxon():
    return 'mus'


@pytest.fixture
def s3_output():
    return 's3://olgabot-maca/aguamenti-test/'


def test_rnaseq(data_folder, experiment_id, taxon, s3_output):
    from aguamenti.rnaseq import align

    csv = os.path.join(data_folder, 'rnaseq_align.csv')
    true = pd.read_csv(csv)

    runner = CliRunner()
    result = runner.invoke(align, [experiment_id, taxon, s3_output])

    # exit code of '0' means success!
    assert result.exit_code == 0
    assert 'samples.csv' in result.output
    assert 'config.json' in result.output

    # Make sure the files are there
    assert os.path.exists('samples.csv')
    assert os.path.exists('config.json')

    # Ensure file contents are correct
    test = pd.read_csv('samples.csv')
    pdt.assert_frame_equal(test, true)



def test_rnaseq_custom_output(data_folder, experiment_id, taxon, s3_output,
                              tmpdir):
    from aguamenti.rnaseq import align

    runner = CliRunner()
    result = runner.invoke(align, ["--output", tmpdir,
                                   experiment_id, taxon, s3_output])
    # exit code of '0' means success!
    assert result.exit_code == 0

    # Make sure the files are there
    assert os.path.exists(os.path.join(tmpdir, 'samples.csv'))
    assert os.path.exists(os.path.join(tmpdir, 'config.json'))
