import re
import yaml
import datetime
import time
from sitefab import utils

date_matcher = re.compile('(\d+) +(\w{3}) +(\d+) +(\d+):(\d+)')  # noqa
frontmatter_matcher = re.compile(r'(^\s*---.*?---\s*$)',
                                 re.DOTALL | re.MULTILINE)


def parse_fields(fields=None):
    """ Recursively parse a given dict of fields to add extra information
    (e.g timestamp) if needed

    Args:
        fields (dict): the fields to parse

    Returns:
        objdict: the fields with the additional properties
    """
    new_fields = {}
    if fields:
        for name, value in fields.items():
            if isinstance(value, dict):
                new_fields[name] = parse_fields(value)
            else:
                new_fields[name] = value
                # adding timestamp
                if value and "_date" in name:
                    ts = parse_date_to_ts(value)
                    if ts:
                        fts = name + "_ts"
                        new_fields[fts] = ts

    return new_fields


def parse_date_to_ts(date_str):
    """ create the timestamp coresponding to a given date string"""
    if not date_str:
        return None
    m = date_matcher.search(date_str)

    if not m:
        return None
    day = m.group(1)
    month = m.group(2).capitalize()
    year = m.group(3)
    hour = m.group(4)
    minutes = m.group(5)

    if len(day) == 1:
        day = "0" + day

    if len(hour) == 1:
        hour = "0" + hour

    if len(minutes) == 1:
        minutes = "0" + minutes
    date_str = "%s-%s-%s %s:%s" % (day, month, year, hour, minutes)
    try:
        d = datetime.datetime.strptime(date_str, "%d-%b-%Y %H:%M")
    except:  # noqa
        return None
    dtt = d.timetuple()  # time.struct_time
    ts = int(time.mktime(dtt))
    ts -= (3600 * 8)
    return ts


def parse(post):
    """ Get a post content and extract frontmatter data if exist

    Args:
        post (str): post to parse

    Returns
        list: [meta data, md]

    note: all sanity check must be done via the linter and
    used in linter.validate()
    """
    md = post
    d = frontmatter_matcher.search(post)
    if d:
        frontmatter = d.group(1)
        md = md.replace(frontmatter, "")
        frontmatter = frontmatter.replace("---", '')
        try:
            m = yaml.load(frontmatter, Loader=yaml.SafeLoader)  # using YAML :)
        except yaml.YAMLError as ye:
            print(ye)
            m = None

        if type(m) != dict:
            meta_data = None
        else:
            meta_data = parse_fields(m)
            meta = utils.dict_to_objdict(meta_data)

    return [meta, md]
