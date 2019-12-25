import pytest
from sitefab.SiteFab import SiteFab
from.conftest import TEMPLATE_DATA_CONFIG_FILE_PATH


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
    fname = TEMPLATE_DATA_CONFIG_FILE_PATH
    site = SiteFab(fname)
    assert site.config
    # FIXME add more test for the correctness here.


def test_template_filters(sitefab):
    "ensure custom filters from plugins/template/filters are correctly loaded"
    assert 'str_to_list' in sitefab.jinja2.filters


def test_get_config(sitefab):
    assert sitefab.get_config() == sitefab.config
