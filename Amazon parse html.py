__author__ = 'torresal'
import urllib.request, pprint
"""doc = urllib.request.urlopen("http://associates-amazon.s3.amazonaws.com/signed-requests/helper/index.html")
htmlsource = doc.read()
doc.close()
pprint.pprint(htmlsource)"""

import requests, json
url = "http://associates-amazon.s3.amazonaws.com/signed-requests/helper/index.html"
r = requests.get(url)
#print (r.json())
JSONdict = r.text
print(JSONdict)
