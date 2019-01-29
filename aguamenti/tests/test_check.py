#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from click.testing import CliRunner
import pytest


@pytest.fixture
def check_folder(data_folder):
    return os.path.join(data_folder, 'check')


@pytest.fixture
def reflow_program():
    return "greet.rf"


@pytest.fixture
def reflow_program_syntax_error():
    return "greet_syntax_error.rf"


def test_get_parameter_order(check_folder, reflow_program):
    from aguamenti.check import get_parameter_order

    program_full_path = os.path.join(check_folder, reflow_program)

    test = get_parameter_order(program_full_path)
    true = ['whom', 'greeting']
    assert test == true


def test_get_parameter_order_syntax_error(check_folder,
                                          reflow_program_syntax_error):
    from aguamenti.check import get_parameter_order

    program_full_path = os.path.join(check_folder, reflow_program_syntax_error)

    with pytest.raises(ValueError):
        get_parameter_order(program_full_path)


def test_check_batch(check_folder):
    from aguamenti.check import check_batch

    runner = CliRunner()
    result = runner.invoke(check_batch, ['--path', check_folder])

    # exit code of '0' means success!
    assert result.exit_code == 0

    captured = result.output

    found_sample = '---\nFound sample with id "english"'
    running = 'greet.rf -whom world -greeting hello\'\n---\n'

    assert isinstance(captured, object)
    assert found_sample in captured
    assert running in captured


def test_check_batch_debug(check_folder):
    from aguamenti.check import check_batch

    runner = CliRunner()
    result = runner.invoke(check_batch, ['--debug', '--path', check_folder])

    # exit code of '0' means success!
    assert result.exit_code == 0

    captured = result.output

    found_sample = '---\nFound sample with id "english"'
    running = 'greet.rf -whom world -greeting hello\'\n---\n'

    assert isinstance(captured, object)
    assert found_sample in captured
    assert running in captured
    assert 'reflow run -trace' in captured
