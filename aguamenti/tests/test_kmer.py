#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

from click.testing import CliRunner
import pytest
import pandas as pd
import pandas.testing as pdt


@pytest.fixture
def s3_input_path():
    from aguamenti.s3_utils import S3_INPUT_PATH
    return os.path.join(S3_INPUT_PATH, '20181030_FS10000331_12_BNT40322-1214')


@pytest.fixture
def s3_output():
    return 's3://olgabot-maca/aguamenti-test-kmer/'



@pytest.fixture
def ksize():
    return 21



@pytest.fixture
def kmer_folder(data_folder):
    return os.path.join(data_folder, 'kmer')


@pytest.fixture
def true_config(kmer_folder):
    from aguamenti.os_utils import REFLOW_WORKFLOWS

    config = os.path.join(kmer_folder, 'config.json')
    with open(config) as f:
        true_config = json.load(f)
    true_config['program'] = os.path.join(REFLOW_WORKFLOWS,
                                          true_config['program'])
    return true_config


def test_kmer(kmer_folder, s3_input_path, ksize, s3_output):
    from aguamenti.kmer import similarity

    # csv = os.path.join(kmer_folder, 'samples.csv')
    # true_samples = pd.read_csv(csv)

    runner = CliRunner()
    result = runner.invoke(similarity, [s3_input_path, ksize, s3_output])

    # exit code of '0' means success!
    assert result.exit_code == 0
    assert 'samples.csv' in result.output
    assert 'config.json' in result.output

    # # Make sure the files are there
    # assert os.path.exists('samples.csv')
    # assert os.path.exists('config.json')
    #
    # # Ensure file contents are correct
    # test = pd.read_csv('samples.csv')
    # pdt.assert_frame_equal(test, true_samples)
    #
    # with open('config.json') as f:
    #     test_config = json.load(f)
    # assert test_config == true_config
