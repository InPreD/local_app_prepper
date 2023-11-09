from bs4 import BeautifulSoup
import click, glob, json, os, re, sys

"""
    Global variables
        - glob to detect fastq files in run folder
        - regex to extract first letters from Instrument field in RunInfo.xml
        - all instrument abbreviations associated with NovaSeq
"""
fastq_file_glob = 'Alignment*/**/*.fastq.gz'
instrument_abbreviation_rex = '^\D+'
novaseq = [
    'A'
]

"""
    read json templates and collect information necessary for input.json files
"""
@click.command()
@click.option('--gather-input-json-template', help='path to template input.json for gather workflow', default=os.path.join(os.path.dirname(sys.argv[0]), 'templates/gather.json'), type=click.Path(exists=True))
@click.option('--input', '-i', help='sequencing run output folder path', required=True, type=click.Path(exists=True))
@click.option('--run-info-xml', help='RunInfo.xml file name', default='RunInfo.xml', type=str)
@click.option('--tso500-input-json-template', help='path to template input.json for TSO500 workflow', default=os.path.join(os.path.dirname(sys.argv[0]), 'templates/tso500.json'), type=click.Path(exists=True))
def cli(gather_input_json_template, input, run_info_xml, tso500_input_json_template):
    # read json templates
    tso500 = get_json(tso500_input_json_template)
    gather = get_json(gather_input_json_template)

    # get values
    isNovaSeq = is_novaseq(os.path.join(input, run_info_xml))
    startFromFastq, fastqFolder = detect_fastq(input)

    # generate input.json for TSO500
    tso500['TSO500.isNovaSeq'] = isNovaSeq
    tso500['TSO500.startFromFastq'] = startFromFastq
    tso500['TSO500.fastqFolder'] = fastqFolder
    write_json(tso500, 'tso500.json')

    # generate input.json for gather
    gather['GatherResultsWorkflow.isNovaSeq'] = isNovaSeq
    gather['GatherResultsWorkflow.startFromFastq'] = startFromFastq
    write_json(gather, 'gather.json')

"""
    use glob to find fastq and return folder containing them or empty string if not
"""
def detect_fastq(path):
    fastq_files = glob.glob(os.path.join(path, fastq_file_glob), recursive=True)
    if len(fastq_files) > 0:
        return True, os.path.normpath(os.path.dirname(fastq_files[0]).replace(path, 'RUNFOLDER/'))
    else:
        return False, ''

"""
    read json template
"""
def get_json(path):
    f = open(path)
    data = json.load(f)
    f.close()
    return data

"""
    Use Instrument field in RunInfo.xml to check if the sequencing was performed on a NovaSeq
"""
def is_novaseq(path):
    with open(path, 'r') as f:
        content = f.read()

    xml = BeautifulSoup(content, 'xml')

    instrument = xml.Instrument.get_text()
    tokens = re.findall(instrument_abbreviation_rex, instrument)
    try:
        if tokens[0] in novaseq:
            return True
        else:
            return False
    except:
        print('the Instrument field in %s is not parseable: %s' % (path, instrument))
        raise IndexError

"""
    write input.json
"""
def write_json(obj, path):
    with open(path, 'w') as f:
        f.write(json.dumps(obj, indent=4))

"""
    entry point
"""
def main():
    cli()