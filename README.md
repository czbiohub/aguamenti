
Aguamenti
===============================

[![Travis-CI build status](https://travis-ci.org/czbiohub/aguamenti)][travis-ci]
[![PyPI Version](https://pypi.python.org/pypi/aguamenti)][pypi]

[travis-ci]: https://img.shields.io/travis/czbiohub/aguamenti.svg
[pypi]: https://img.shields.io/pypi/v/aguamenti.svg


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

* Make a `samples.csv` file of all your samples for an RNA-seq alignment and
  counting with Reflow:
    ```
    python aguamenti/rnaseq.py 20181030_FS10000331_12_BNT40322-1214 mus s3://olgabot-maca/aguamenti-test/ > ~/samples.csv
    ```
