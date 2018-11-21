# -*- coding: utf-8 -*-

# Set input language USA unicode encoding setting
# Necessary because click assumes ascii input unless otherwise specified
# https://click.palletsprojects.com/en/7.x/python3/
import os
unicode_usa = 'en_US.utf-8'
os.environ['LC_LANG'] = unicode_usa
os.environ["LC_ALL"] = unicode_usa

import click

from aguamenti.rnaseq import align

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
