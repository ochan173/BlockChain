import urllib.request, json
import numpy
from collections import namedtuple
with urllib.request.urlopen("https://test.fanslab.io/blockchain") as url:
    data = json.loads(url.read().decode())
    print(data["KKC"][0])
    # for b in data["KKC"]:
    #     print(b["hash"])