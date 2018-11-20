#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from click.testing import CliRunner


def test_rnaseq(data_folder):
    from aguamenti.rnaseq import align

    experiment_id = '20181030_FS10000331_12_BNT40322-1214'
    taxon = 'mus'
    s3_output = 's3://olgabot-maca/aguamenti-test/'

    csv = os.path.join(data_folder, 'rnaseq_align.csv')
    with open(csv) as f:
        true = f.read()

    runner = CliRunner()
    result = runner.invoke(align, [experiment_id, taxon, s3_output])
    assert result.exit_code == 0
    assert result.output == true
