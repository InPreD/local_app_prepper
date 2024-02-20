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

The docker image `inpred/local_app_prepper:latest` is available at dockerhub. The recommended way of running the tool is as a container (docker, singularity/apptainer).

Start your **docker** container like so:

```bash
$ docker run --rm -it -v /path/to/runfolder:/containerpath/to/runfolder:ro inpred/local_app_prepper:latest bash
```

or if you are more a **apptainer/singularity** kind of person:

```bash
$ apptainer run -B /path/to/runfolder:/containerpath/to/runfolder:ro docker://inpred/local_app_prepper:latest bash
# OR
$ singularity run -B /path/to/runfolder:/containerpath/to/runfolder:ro docker://inpred/local_app_prepper:latest bash
```

Both `/path/to/runfolder` and `/containerpath/to/runfolder` should be replaced with the actual path to the run folder and the path you chose for mounting the folder inside the container, respectively.

Once you are inside the container, you can execute the following to get some help text:

```bash
$ local_app_prepper.py --help
```

And to produce `.json` files, simply run:

```bash
$ local_app_prepper.py -i /containerpath/to/runfolder -s <sample 1 id>,<sample 2 id>,...
```

`/containerpath/to/runfolder` should be replaced with the actual path you mounted the run folder at inside the container and `<sample 1 id>` etc. should be a comma-separated list of your sample ids.
