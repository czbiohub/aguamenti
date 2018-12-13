#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner


def test_traverse_find_reflow_batch_dirs(data_folder):
    from aguamenti.status import traverse_find_reflow_batch_dirs

    reflow_dirs = traverse_find_reflow_batch_dirs(data_folder)
    assert sum(1 for x in reflow_dirs) == 1


def test_echo_n_status(capsys):
    from aguamenti.status import echo_n_status

    n_statuses = {"waiting": 1, "canceled": 2, "done": 3, "running": 4}
    n_total = 10
    echo_n_status(n_statuses, n_total)
    captured = capsys.readouterr().out
    assert 'canceled' in captured
    assert 'done' in captured
    assert 'waiting' in captured
    assert 'running' in captured


def test_listbatches(data_folder):
    from aguamenti.status import listbatches

    runner = CliRunner()
    result = runner.invoke(listbatches, ['--path', data_folder])

    # exit code of '0' means success!
    assert result.exit_code == 0

    # Correct number of done, waiting, canceled, running jobs
    correct = "canceled:\t21/168\t(12.500%)\n\tdone:\t47/168\t(27.976%)\n\t" \
              "running:\t15/168\t(8.929%)\n\twaiting:\t85/168\t(50.595%)"
    assert correct in result.output
