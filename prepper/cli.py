from bs4 import BeautifulSoup
import click, copy, glob, json, os, re, sys

"""
    Global variables
        - regex to extract first letters from Instrument field in RunInfo.xml
        - all instrument abbreviations associated with NovaSeq
"""
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
@click.option('--samples', '-s', help='comma-separated list of sample ids', required=True, type=str)
@click.option('--tso500-input-json-template', help='path to template input.json for TSO500 workflow', default=os.path.join(os.path.dirname(sys.argv[0]), 'templates/tso500.json'), type=click.Path(exists=True))
def cli(gather_input_json_template, input, run_info_xml, samples, tso500_input_json_template):
    # read json templates
    tso500 = get_json(tso500_input_json_template)
    gather = get_json(gather_input_json_template)

    # determine if sequencing was performed on a NovaSeq
    isNovaSeq = is_novaseq(os.path.join(input, run_info_xml))

    # generate inputs.json for TSO500 demultiplexing
    demultiplex = copy.deepcopy(tso500)
    demultiplex['TSO500.demultiplex'] = True
    demultiplex['TSO500.isNovaSeq'] = isNovaSeq
    write_json(demultiplex, 'demultiplex.json')

    # generate inputs.json files for each sample for TSO500 DNA and RNA analysis
    for sample in samples.split(','):
        tso500['TSO500.isNovaSeq'] = isNovaSeq
        tso500['TSO500.sampleOrPairIDs'] = sample
        tso500['TSO500.startFromFastq'] = True
        tso500['TSO500.fastqFolder'] = 'FASTQFOLDER'
        write_json(tso500, ('tso500_%s.json' % sample))

    # generate input.json for gather
    gather['GatherResultsWorkflow.isNovaSeq'] = isNovaSeq
    write_json(gather, 'gather.json')

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