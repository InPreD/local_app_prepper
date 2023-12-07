# local_app_prepper

creates `inputs.json` files to be used with the LocalApp

## Introduction :speech_balloon:

Running the LocalApp requires the specification of a least one `inputs.json` file containing the configuration as well as input and output options. To make running the LocalApp more efficient, the `local_app_prepper` will generate several `inputs.json` files:

`inputs.json` | description
--- | ---
`demultiplex.json` | running the initial steps to demultiplex the sequencing data
`tso500_<sample id>.json` | running the DNA/RNA workflow of the TSO500 pipeline from `.fastq` files
`gather.json` | running the Gather workflow to combine all results into a single directory

## Dependencies :briefcase:

[![beautifulsoup4](https://img.shields.io/badge/beautifulsoup4-4.12.2-blue?color=417fb1)](https://pypi.org/project/beautifulsoup4/)

[![click](https://img.shields.io/badge/click-8.1.7-blue?color=417fb1)](https://pypi.org/project/click/)

[![lxml](https://img.shields.io/badge/lxml-4.9.3-blue?color=417fb1)](https://pypi.org/project/lxml/)

[![python](https://img.shields.io/badge/python-3.11.4-blue?color=417fb1)](https://www.python.org/)

## Usage :rocket:

There is a docker image available at `inpred/local_app_prepper:latest` which is the recommended way of running this tool. Help text is printed like so:

```bash
$ local_app_prepper.py --help
```

And to produce `inputs.json` files, simply run:

```bash
$ local_app_prepper.py -i <run id> -s <sample 1 id>,<sample 2 id>,...
```
