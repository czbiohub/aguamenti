import os

from click.testing import CliRunner
import pytest
# import pandas as pd
# import pandas.testing as pdt

# def test_wrap():
#     from aguamenti.batchwrapper import wrap
#
#     runner = CliRunner()
#     result = runner.invoke(wrap)
#
#     assert result.exit_code == 0


@pytest.fixture
def batchwrapper_folder(data_folder):
    return os.path.join(data_folder, 'batchwrapper')


@pytest.fixture
def parameters_csv(batchwrapper_folder):
    return os.path.join(batchwrapper_folder, 'test_parameters.csv')


@pytest.fixture
def project_name():
    return '180828_M05295_0162_000000000'


def test_wrap(parameters_csv, project_name):
    from aguamenti.batchwrapper import wrap

    runner = CliRunner()
    result = runner.invoke(wrap, [parameters_csv, project_name])

    assert result.exit_code == 0

    assert False
