
Aguamenti
===============================

[![Travis-CI build status](https://travis-ci.org/czbiohub/aguamenti)][travis-ci]
[![Code Coverage](https://codecov.io/gh/czbiohub/aguamenti)][codecov]
[![PyPI Version](https://pypi.python.org/pypi/aguamenti)][pypi]

[travis-ci]: https://img.shields.io/travis/czbiohub/aguamenti.svg
[pypi]: https://img.shields.io/pypi/v/aguamenti.svg
[codecov]: https://codecov.io/gh/czbiohub/aguamenti/branch/master/graph/badge.svg


What is `aguamenti`?
---------------------------------------

Python utility scripts for working with
[reflow-workflows](https://github.com/czbiohub/reflow-workflows). "Aguamenti" is
a spell in Harry Potter that creates water out of nothing.

* Free software: BSD license
* Documentation: https://olgabot.github.io/aguamenti


Installation
------------

To install this code, clone this github repository and use `pip` to install

    git clone https://github.com/olgabot/aguamenti.git
    cd aguamenti

If you have the
[Anaconda Python distribution](anaconda.com/download/)/[Miniconda](https://conda.io/miniconda.html) (suggested):

    make conda_install

If you have non-conda Python:

    make install 


Features
--------

* Create an RNA-seq alignment batch with `samples.csv` and `config.json` files for
  STAR alignment and HTSeq-count with Reflow:
    ```
      aguamenti rnaseq-align  20181030_FS10000331_12_BNT40322-1214 mus s3://olgabot-maca/aguamenti-test/
    Writing /Users/olgabot/code/aguamenti/samples.csv ...
        Done.
    Writing /Users/olgabot/code/aguamenti/config.json ...
        Done.
    ```

* Create a RNA-seq alignment batch with a custom `reflow-workflows` path
  (`--reflow-workflows-path`) and custom output (`--output`) location
    ```
      aguamenti rnaseq-align --reflow-workflows-path ~/code/reflow-workflows/ --output ~/code/reflow-batches/rnaseq/mus/20181030_FS10000331_12_BNT40322-1214/ 20181030_FS10000331_12_BNT40322-1214 mus s3://olgabot-maca/aguamenti-test/
    Writing /Users/olgabot/code/reflow-batches/rnaseq/mus/20181030_FS10000331_12_BNT40322-1214/samples.csv ...
        Done.
    Writing /Users/olgabot/code/reflow-batches/rnaseq/mus/20181030_FS10000331_12_BNT40322-1214/config.json ...
        Done.
    ```
