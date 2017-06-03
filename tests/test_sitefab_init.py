import pytest
import os
from SiteFab.SiteFab import SiteFab

class TestSiteFabInit:

    TEST_ROOT_DIR = os.path.dirname(__file__)
    
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
        fname = os.path.join(TestSiteFabInit.TEST_ROOT_DIR, "data/config/valid_config.yaml")
        print fname
        site = SiteFab(fname)
        assert site.config != None
        #FIXME add more test for the correctness here.

    #FIXME: add test for invalid config