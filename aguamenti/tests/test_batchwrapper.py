import json
import os

from click.testing import CliRunner
import pytest
import pandas as pd
import pandas.testing as pdt

@pytest.fixture
def batchwrapper_folder(data_folder):
    return os.path.join(data_folder, 'batchwrapper')


@pytest.fixture
def parameters_csv(batchwrapper_folder):
    return os.path.join(batchwrapper_folder, 'test_parameters.csv')


@pytest.fixture
def project_name():
    return '180828_M05295_0162_000000000'


@pytest.fixture
def true_config(batchwrapper_folder):
    from aguamenti.os_utils import REFLOW_WORKFLOWS

    config = os.path.join(batchwrapper_folder, 'config.json')
    with open(config) as f:
        true_config = json.load(f)

    true_config['program'] = os.path.join(REFLOW_WORKFLOWS,
                                          true_config['program'])
    # true_config['runs_file'] = os.path.join(os.path.realpath(os.path.curdir),
    #                                         true_config['runs_file'])
    return true_config


def test_wrap(parameters_csv, project_name, tmpdir, true_config,
              batchwrapper_folder):
    from aguamenti.batchwrapper import wrap

    # os.chdir(tmpdir)
    csv = os.path.join(batchwrapper_folder, 'samples.csv')
    true_samples = pd.read_csv(csv)

    runner = CliRunner()
    result = runner.invoke(wrap, ["--output", tmpdir, parameters_csv,
                                  project_name])

    assert result.exit_code == 0

    folder = os.path.join(tmpdir, 'rnaseq', project_name)

    samples_csv = os.path.join(folder, 'samples.csv')
    config_json = os.path.join(folder, 'config.json')

    # Test that expected outputs are there
    assert os.path.exists(samples_csv)
    assert os.path.exists(config_json)

    test = pd.read_csv(samples_csv)
    pdt.assert_frame_equal(test, true_samples)

    with open(config_json) as f:
        test_config = json.load(f)

    true_config['runs_file'] = os.path.join(tmpdir, true_config['runs_file'])
    assert test_config == true_config

    assert False
