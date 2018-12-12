#!/usr/bin/env python
# -*- coding: utf-8 -*-

from click.testing import CliRunner


def test_traverse_find_reflow_batch_dirs(data_folder):
    from aguamenti.monitor import traverse_find_reflow_batch_dirs

    reflow_dirs = traverse_find_reflow_batch_dirs(data_folder)
    assert sum(1 for x in reflow_dirs) == 1


def test_echo_n_status(capsys):
    from aguamenti.monitor import echo_n_status

    n_statuses = {"waiting": 1, "canceled": 2, "done": 3, "running": 4}
    n_total = 10
    echo_n_status(n_statuses, n_total)
    captured = capsys.readouterr()
    true = '\tcanceled:\t2/10\t(20.000%)\n\tdone:\t3/10\t(30.000%)\n\t' \
           'running:\t4/10\t(40.000%)\n\twaiting:\t1/10\t(10.000%)\n'
    assert captured.out == true


def test_listbatches(data_folder):
    from aguamenti.monitor import listbatches

    runner = CliRunner()
    result = runner.invoke(listbatches, ['--reflow-batches-path', data_folder])

    # exit code of '0' means success!
    assert result.exit_code == 0

    # Correct number of done, waiting, canceled, running jobs
    correct = "canceled:\t21/168\t(12.500%)\n\tdone:\t47/168\t(27.976%)\n\t" \
              "running:\t15/168\t(8.929%)\n\twaiting:\t85/168\t(50.595%)"
    assert correct in result.output
