import json

def parse_string(d):
    s = d.split('-')
    f = "%s/%s/%s" % (s[2], s[1], s[0])
    return f

def toJson(dict):
    jd = json.dumps(dict)
    return jd

