# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, REFLOW_BATCHES, sanitize_path

from collections import defaultdict
import subprocess


import click

from .reflow_utils import SAMPLES_CSV, CONFIG_JSON


STATE_JSON = 'state.json'
STATE_LOCK = 'state.lock'

STATUS_FILES = STATE_JSON, STATE_LOCK, CONFIG_JSON, SAMPLES_CSV


LISTBATCH_COLS = ["id", "run", "status"]
KNOWN_STATUSES = 'done', 'running', 'waiting', 'canceled'


def traverse_find_reflow_batch_dirs(dirname):
    for root, dirs, files in os.walk(dirname):
        if all(x in files for x in STATUS_FILES):
            yield root


def echo_n_status(n_statuses, n_total):
    for status, n in n_statuses.items():
        # print(f"\t{status}: n: {n}")
        # print(f"\t{status}: n_total: {n_total}")
        click.echo(f"\t{status}:\t{n}/{n_total}\t({100*n/n_total:.3f}%)")


@click.command(short_help="Summarize currently running")
@click.option('--reflow-batches-path', default=REFLOW_BATCHES,
              help='Parent directory of subfolders containing reflow batch '
                   'files "samples.csv" and "config.json"')
def listbatches(reflow_batches_path, n_last_words=4):
    """Summarize done, running, waiting, canceled reflow batch jobs"""
    reflow_batches_path = sanitize_path(reflow_batches_path)

    reflow_batch_dirs = traverse_find_reflow_batch_dirs(reflow_batches_path)
    for reflow_batch_dir in reflow_batch_dirs:
        os.chdir(reflow_batch_dir)

        listbatch = subprocess.run(["reflow", "listbatch"],
                                   stdout=subprocess.PIPE)
        lines = listbatch.stdout.decode("utf-8").splitlines()

        n_known_statuses = dict.fromkeys(KNOWN_STATUSES, 0)
        n_other_statuses = defaultdict(int)
        for line in lines:
            line = line.strip()
            matched_status = False
            for status in KNOWN_STATUSES:
                if line.endswith(status):
                    n_known_statuses[status] += 1
                    matched_status = True
            if not matched_status:
                last_words = ' '.join(line.split()[-n_last_words:])
                n_other_statuses[last_words] += 1

        n_total = len(lines)

        click.echo(reflow_batch_dir)
        echo_n_status(n_known_statuses, n_total)

        if len(n_other_statuses) > 0:
            click.echo("\tOther statuses:")
            echo_n_status(n_other_statuses, n_total)
