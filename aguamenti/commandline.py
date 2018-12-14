# -*- coding: utf-8 -*-

# Import modified 'os' module with LC_LANG set so click doesn't complain
from aguamenti.os_utils import os  # noqa: F401
import sys

import click

from aguamenti.rnaseq import align
from aguamenti.batchwrapper import wrap

settings = dict(help_option_names=['-h', '--help'])


@click.group(options_metavar='', subcommand_metavar='<command>',
             context_settings=settings)
def cli():
    """
    Aguamenti creates reflow batches for AWS jobs from experiment IDs
    """
    pass


cli.add_command(align, name='rnaseq-align')
cli.add_command(wrap, name='wrap')


if __name__ == "__main__":
    cli(sys.argv[1:])
