import json
from datetime import datetime

def parse_string(d):
    s = d.split('-')
    f = "%s/%s/%s" % (s[2], s[1], s[0])
    return f

def toJson(dict):
    jd = json.dumps(dict)
    return jd

def get_first_day():
    today = datetime.today()
    today = today.strftime('%d/%m/%Y')
    today = today[2:]
    first_day_s = "01" + today
    first_day = datetime.strptime(first_day_s, "%d/%m/%Y")
    return first_day