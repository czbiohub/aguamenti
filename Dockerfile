FROM continuumio/anaconda3
MAINTAINER olga.botvinnik@czbiohub.org

WORKDIR /home

USER root

# Add user "main" because that's what is expected by this image
RUN useradd -ms /bin/bash main


ENV PACKAGES zlib1g git g++ make ca-certificates gcc zlib1g-dev libc6-dev

### don't modify things below here for version updates etc.

WORKDIR /home

RUN apt-get update && \
    apt-get install -y --no-install-recommends ${PACKAGES} && \
    apt-get clean

RUN conda install --yes Cython bz2file pytest numpy matplotlib scipy sphinx alabaster

# Required for multiprocessing of 10x bam file
RUN pip install pathos bamnostic

# Install bam2fastx
RUN cd /home && \
	git clone https://github.com/czbiohub/bam2fastx -b master &&\
	cd bam2fastx && \
	python3 setup.py install
RUN bam2fastx --help

USER main
