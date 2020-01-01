from sitefab import utils
from sitefab.utils.objdict import objdict


def test_dict_to_objdict():
    dic = {
        "str": "str",
        "int": 1,
        "array": [1, 2, 3]
    }
    objdict = utils.dict_to_objdict(dic)
    assert objdict.str == "str"
    assert objdict.int == 1
    assert isinstance(objdict.array, type([]))


def test_create_objdict():
    od = utils.create_objdict()
    od2 = objdict()
    assert type(od) == type(od2)


def test_objdict_to_dict():
    od = utils.create_objdict()
    od.str = "str"
    od.int = 1
    od.array = [1, 2, 3]
    od.arrayofarray = [[1, 2], [3, 4]]
    d = utils.objdict_to_dict(od)
    assert d['str'] == "str"
    assert d['int'] == 1
    assert d['array'][2] == 3
    assert d['arrayofarray'][0][0] == 1   # testing nested array
    assert d['arrayofarray'][1][1] == 4   # testing nested array

