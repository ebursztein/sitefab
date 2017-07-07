# encoding: utf-8
import pytest
from SiteFab import utils
from SiteFab.utils.objdict import objdict 

class TestUtils:

    def test_dict_to_objdict(self):
        dic = {
            "str": "str",
            "int": 1,
            "array": [1,2,3]
        }
        objdict = utils.dict_to_objdict(dic)
        assert objdict.str == "str"
        assert objdict.int == 1
        assert type(objdict.array) == type([])

    def test_create_objdict(self):
        od = utils.create_objdict()
        od2 = objdict()
        assert type(od) == type(od2)

    def test_objdict_to_dict(self):
        od = utils.create_objdict()
        od.str = "str"
        od.int = 1
        od.array = [1,2,3]
        od.arrayofarray = [[1,2], [3,4]]
        d = utils.objdict_to_dict(od)
        assert d['str'] == "str"
        assert d['int'] == 1
        assert d['array'][2] == 3
        assert d['arrayofarray'][0][0] == 1   # testing nested array
        assert d['arrayofarray'][1][1] == 4   # testing nested array
    
    def test_img_extensions(self):
        values = [ 
                [".png", "PNG", "image/png"], 
                [".webp", "WEBP", "image/webp"], 
                [".jpeg", "JPEG", "image/jpeg"],
                [".jpg", "JPEG", "image/jpeg"], 
                ["unkn", None, None]
            ]
        for value in values:
            codename, extension = utils.get_img_extension_alternative_naming(value[0])
            assert codename == value[1]
            assert extension == value[2]