===============================
Aguamenti
===============================

.. image:: https://img.shields.io/travis/olgabot/aguamenti.svg
        :target: https://travis-ci.org/olgabot/aguamenti

.. image:: https://img.shields.io/pypi/v/aguamenti.svg
        :target: https://pypi.python.org/pypi/aguamenti


What is `aguamenti`?
---------------------------------------

Python utility scripts for working with reflow workflows. "Aguamenti" is a spell in Harry Potter that creates water out of nothing.

* Free software: BSD license
* Documentation: https://olgabot.github.io/aguamenti


Installation
------------

To install this code, clone this github repository and use `pip` to install

    git clone https://github.com/olgabot/aguamenti.git
    cd aguamenti
    pip install .  # The "." means "install *this*, the folder where I am now"



Features
--------

* TODO

* Create a RNA-seq alignment batch with a custom `reflow-workflows` path
  (`--reflow-workflows-path`) and custom output (`--output`) location
```
  aguamenti rnaseq-align --reflow-workflows-path ~/code/reflow-workflows/ --output ~/code/reflow-batches/rnaseq/mus/20181030_FS10000331_12_BNT40322-1214/ 20181030_FS10000331_12_BNT40322-1214 mus s3://olgabot-maca/aguamenti-test/
Writing /Users/olgabot/code/reflow-batches/rnaseq/mus/20181030_FS10000331_12_BNT40322-1214/samples.csv ...
	Done.
Writing /Users/olgabot/code/reflow-batches/rnaseq/mus/20181030_FS10000331_12_BNT40322-1214/config.json ...
	Done.
```
