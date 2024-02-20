import pytest
import prepper.cli

from contextlib import nullcontext as does_not_raise
from json import decoder

@pytest.mark.parametrize(
    "input, exception, want",
    [
        ('test/test.json', does_not_raise(), {'key': 'value'}),
        ('test/test.yaml', pytest.raises(decoder.JSONDecodeError), {}),
        ('test/non-existent.json', pytest.raises(FileNotFoundError), {}),
    ]
)
def test_get_json(input, exception, want):
    with exception:
        assert prepper.cli.get_json(input) == want

@pytest.mark.parametrize(
    "input, exception, want",
    [
        ('test/230101_NDX123456_0001_ABCDEFGH/RunInfo.xml', does_not_raise(), True),
        ('test/230101_NDX123456_0002_ABCDEFGH/RunInfo.xml', does_not_raise(), False),
        ('test/230101_NDX123456_0003_ABCDEFGH/RunInfo.xml', pytest.raises(IndexError), False),
    ]
)
def test_is_novaseq(input, exception, want):
    with exception:
        assert prepper.cli.is_novaseq(input) == want