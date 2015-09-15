import requests
import json
import os

bookLocation = 'http://data.globalchange.gov/book.json?all=1'

req = requests.get(bookLocation)
allBookJson = req.json()

os.makedirs('book')

for block in allBookJson:
    fileName = block['href']
    fileName = fileName[:-5]
    fileName = fileName.replace("http://data.globalchange.gov/","")
    fileName = "%s%s"%(fileName, ".json")

    with open(str(fileName), 'w') as bookJson:
        bookJson.write(json.dumps(block, sort_keys=True, indent=4, separators=(',',': ')))

