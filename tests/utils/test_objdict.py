from sitefab import utils


def test_creation(myobjdict):
    d = {'a': 'test', 'b': {"c": '2nd'}}
    p = utils.dict_to_objdict(d)
    assert d['a'] == p.a
    assert d['b']['c'] == p.b.c


def test_insertion(myobjdict):
    myobjdict.test = 'yes'
    assert myobjdict.test == 'yes'
    assert myobjdict['test'] == 'yes'
    myobjdict['test2'] = 'oui'
    assert myobjdict.test2 == 'oui'


def test_deletion(myobjdict):
    myobjdict.test = 'yes'
    del myobjdict['test']
    assert 'yes' not in myobjdict
