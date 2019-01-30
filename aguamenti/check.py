# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os, sanitize_path, get_stdout_stderr_from_command

from itertools import chain
import subprocess

import click

from .reflow_utils import SAMPLES_CSV, CONFIG_JSON, read_config, read_samples


REGION = 'west'
WORKFLOW = 'rnaseq.rf'

# Taxons (species) with available references
SUPPORTED_TAXA = ('mus',)
TAXA_GENOMES = {'mus': 'mouse/vM19'}


def get_parameter_order(reflow_program):
    """Get the expected order of command line flags for a reflow program"""
    stdout, stderr = get_stdout_stderr_from_command(
        ["reflow", "doc", reflow_program])

    stderr = '\n'.join(stderr)
    if 'syntax error' in stderr:
        raise ValueError("Syntax errors in Reflow program:\n"
                         "{stderr}")

    # Save the parameters from the command
    parameter_order = []
    for line in stdout:
        # First section is always parameters, then function definitions.
        if line.startswith('val'):
            val, parameter, *rest = line.split()
            parameter_order.append(parameter)

        # Ignore all function definitions since they're not parameters
        if line.startswith('Declarations'):
            break
    return parameter_order


@click.command(short_help="Submit the first line of a reflow runbatch "
                          "samples.csv to check for errors")
@click.option("--path", default='.',
              help="Where to look for samples.csv and config.json files. "
                   "Default is the current directory")
@click.option("--debug/--no-debug", default=False)
def check_batch(path, debug):
    """Reflow run the first line of a samples.csv"""
    path = sanitize_path(path)

    samples = read_samples(os.path.join(path, SAMPLES_CSV))
    config = read_config(os.path.join(path, CONFIG_JSON))

    program = os.path.join(path, config['program'])

    parameter_order = get_parameter_order(program)

    sample_id = samples.index[0]

    first_row = samples.iloc[0]
    arguments = {}
    for key, value in first_row.items():
        arguments[key] = str(value)

    arguments_ordered = list(chain(*[
        # Add '-' before parameter name to show it's a flag
        (f"-{param}", arguments[param]) for param in parameter_order
    ]))

    if debug:
        base_command = ["reflow", " -log=debug", "run", "-trace", program]
    else:
        base_command = ["reflow", "run", program]

    command = base_command + arguments_ordered

    click.echo("---")
    click.echo(f'Found sample with id "{sample_id}"!')
    click.echo(f"Running '{' '.join(command)}'")
    click.echo("---")
    subprocess.run(command)
