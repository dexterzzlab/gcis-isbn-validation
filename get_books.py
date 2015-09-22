import requests
import json
import os
import datetime
bookLocation = 'http://data.globalchange.gov/book.json?all=1'
top_dir = "output_%s"%datetime.date.today()+"/"
req = requests.get(bookLocation)
allBookJson = req.json()

bookdir = top_dir + "book/"
if not os.path.isdir(bookdir):
    os.makedirs(bookdir)

for block in allBookJson:
    fileName = block['href']
    fileName = fileName[:-5]
    fileName = fileName.replace("http://data.globalchange.gov/","")
    fileName = "%s%s%s"%(top_dir ,fileName, ".json")

    with open(str(fileName), 'w') as bookJson:
        bookJson.write(json.dumps(block, sort_keys=True, indent=4, separators=(',',': ')))

