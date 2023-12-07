import pytest
import prepper.cli

class TestIsNovaseq:
    def test_novaseq(self):
        output = prepper.cli.is_novaseq('test/230101_NDX123456_0001_ABCDEFGH/RunInfo.xml')
        assert output is True

    def test_no_novaseq(self):
        output = prepper.cli.is_novaseq('test/230101_NDX123456_0002_ABCDEFGH/RunInfo.xml')
        assert output is False