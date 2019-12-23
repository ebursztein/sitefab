import pytest
from pathlib import Path
from sitefab.SiteFab import SiteFab

TEST_ROOT_DIR = Path(__file__).parent


def test_empty_config():
    # is SiteFab raise the correct exception
    with pytest.raises(Exception) as excinfo:
        SiteFab(None)
        assert excinfo.value.message == 'Supply a configuration filename'


def test_non_existing_config():
    # is SiteFab raise the correct exception
    with pytest.raises(Exception) as excinfo:
        SiteFab(None)
        assert 'Configuration file not found:' in excinfo.value.message


def test_valid_config():
    # is SiteFab raise the correct exception
    fname = TEST_ROOT_DIR / "data" / "config" / "valid_config.yaml"
    site = SiteFab(fname)
    assert site.config
    # FIXME add more test for the correctness here.
