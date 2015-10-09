import requests
import json
import os
import datetime
import sys

#bookLocation = 'http://data.globalchange.gov/book.json?all=1'
if len(sys.argv) > 1:
    if sys.argv[1] is not None:
	bookLocation = sys.argv[1]


	top_dir_prefix = "gcis-"
	top_dir_suffix = str(datetime.datetime.now())#date.now().isoformat()+"/)"
        top_dir_suffix = top_dir_suffix.replace("-", "")	
	top_dir_suffix = top_dir_suffix.replace(" ", "T")
	top_dir_suffix = top_dir_suffix.replace(":", "")
	top_dir_suffix = top_dir_suffix.split(".")[0]
	#top_dir = "output_%s"%datetime.date.isoformat()+"/"
	top_dir = "%s%s/"%(top_dir_prefix, top_dir_suffix)
	
	req = requests.get(str(bookLocation))
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
        print "Wrote book JSONs to directory %s"%(bookdir)
else:
	print "Requires parameter for GCIS endpont"
