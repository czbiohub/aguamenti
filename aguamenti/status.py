# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, REFLOW_BATCHES, sanitize_path, \
    get_stdout_from_command

from collections import defaultdict


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
    for status, n in sorted(n_statuses.items()):
        # "done" is short relative to other statuses, so pad with one extra
        # tab so it looks nice
        sep = '\t' if status != 'done' else '\t\t'
        click.echo(f"\t{status}:{sep}{n}/{n_total}\t({100*n/n_total:.3f}%)")


@click.command(short_help="Summarize done/running/waiting/canceled reflow "
                          "batch jobs")
@click.option('--path', default=REFLOW_BATCHES,
              help='Parent directory of subfolders containing reflow batch '
                   'files "samples.csv" and "config.json", '
                   f'default: {REFLOW_BATCHES}')
def listbatches(path, n_last_words=4):
    """Summarize done, running, waiting, canceled reflow batch jobs"""
    path = sanitize_path(path)

    reflow_batch_dirs = traverse_find_reflow_batch_dirs(path)
    for reflow_batch_dir in reflow_batch_dirs:
        os.chdir(reflow_batch_dir)

        lines = get_stdout_from_command(["reflow", "listbatch"])

        n_known_statuses = dict.fromkeys(KNOWN_STATUSES, 0)
        n_other_statuses = defaultdict(int)
        for line in lines:
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
