import urllib.request, json
import numpy
from collections import namedtuple


def _json_object_hook(d): return namedtuple('X', d.keys())(*d.values())


def json2obj(data): return json.loads(data, object_hook=_json_object_hook)


def get_data():
    with urllib.request.urlopen("https://test.fanslab.io/blockchain") as url:
        data = json.loads(url.read().decode())

        #print(type(data["KKC"]))

        for k in data["KKC"]:
            print(type(k["validators"]))
        # for b in x["KKC"]:



get_data()