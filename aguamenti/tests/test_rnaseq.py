#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
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


@pytest.fixture
def rnaseq_folder(data_folder):
    return os.path.join(data_folder, 'rnaseq')


@pytest.fixture
def true_config(rnaseq_folder):
    from aguamenti.os_utils import REFLOW_WORKFLOWS

    config = os.path.join(rnaseq_folder, 'config.json')
    with open(config) as f:
        true_config = json.load(f)
    true_config['program'] = os.path.join(REFLOW_WORKFLOWS,
                                          true_config['program'])
    true_config['runs_file'] = os.path.join(os.path.realpath(os.path.curdir),
                                            true_config['runs_file'])
    return true_config


def test_rnaseq(rnaseq_folder, experiment_id, taxon, s3_output, true_config):
    from aguamenti.rnaseq import align

    csv = os.path.join(rnaseq_folder, 'samples.csv')
    true_samples = pd.read_csv(csv)

    runner = CliRunner()
    result = runner.invoke(align, [experiment_id, taxon, s3_output])

    # exit code of '0' means success!
    assert result.exit_code == 0
    assert 'samples.csv' in result.output
    assert 'config.json' in result.output
    assert 0

    # Make sure the files are there
    assert os.path.exists('samples.csv')
    assert os.path.exists('config.json')

    # Ensure file contents are correct
    test = pd.read_csv('samples.csv')
    pdt.assert_frame_equal(test, true_samples)

    with open('config.json') as f:
        test_config = json.load(f)
    assert test_config == true_config


def test_rnaseq_custom_outdir(experiment_id, taxon, s3_output, tmpdir):
    from aguamenti.rnaseq import align

    runner = CliRunner()
    result = runner.invoke(align, ["--output", tmpdir,
                                   experiment_id, taxon, s3_output])
    # exit code of '0' means success!
    assert result.exit_code == 0

    # Make sure the files are there
    assert os.path.exists(os.path.join(tmpdir, 'samples.csv'))
    assert os.path.exists(os.path.join(tmpdir, 'config.json'))
