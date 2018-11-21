# -*- coding: utf-8 -*-

# Import modified 'os' module with LC_LANG set so click doesn't complain
from .os_utils import os

import click

from .rnaseq import align

settings = dict(help_option_names=['-h', '--help'])


@click.group(options_metavar='', subcommand_metavar='<command>',
             context_settings=settings)
def cli():
    """
    Aguamenti creates reflow batches for AWS jobs from experiment IDs
    """
    pass


cli.add_command(align, name='rnaseq-align')


if __name__ == "__main__":
    cli()
