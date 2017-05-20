import pytest

from SiteFab.SiteFab import SiteFab

class TestSiteFabInit:

    def test_empty_config(self):
        # is SiteFab raise the correct exception
        with pytest.raises(Exception) as excinfo:
            site = SiteFab(None)
            assert excinfo.value.message == 'Supply a configuration filename' 
    
    def test_non_existing_config(self):
        # is SiteFab raise the correct exception
        with pytest.raises(Exception) as excinfo:
            site = SiteFab(None)
            assert 'Configuration file not found:' in excinfo.value.message
    
    def test_valid_config(self):
        # is SiteFab raise the correct exception
        valid_file = "data/config/valid_config.yaml"
        site = SiteFab(valid_file)
        assert site.config != None
        #FIXME add more test for the correctness here.

    #FIXME: add test for invalid config