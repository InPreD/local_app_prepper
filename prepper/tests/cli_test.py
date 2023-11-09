import pytest
import prepper.cli

class TestDetectFastq:
    def test_fastq_exists(self):
        output_1, output_2 = prepper.cli.detect_fastq('test/230101_NDX123456_0001_ABCDEFGH')
        assert output_1 is True
        assert output_2 == 'RUNFOLDER/Alignment_1/230101_101010/Fastq'

    def test_fastq_absent(self):
        output_1, output_2 = prepper.cli.detect_fastq('test/230101_NDX123456_0002_ABCDEFGH')
        assert output_1 is False
        assert output_2 == ''

class TestIsNovaseq:
    def test_novaseq(self):
        output = prepper.cli.is_novaseq('test/230101_NDX123456_0001_ABCDEFGH/RunInfo.xml')
        assert output is True

    def test_no_novaseq(self):
        output = prepper.cli.is_novaseq('test/230101_NDX123456_0002_ABCDEFGH/RunInfo.xml')
        assert output is False