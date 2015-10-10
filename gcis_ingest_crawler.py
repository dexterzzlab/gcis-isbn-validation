__author__ = 'Dexter Tan'
import json
import os,re, subprocess, sys
import datetime
import requests
from gcis_clients import GcisClient

requests.packages.urllib3.disable_warnings()

if len(sys.argv) > 2:
    dump_directory = sys.argv[1]

    gcis_endpoint= sys.argv[2]

    ingest_file = "gcis_es_ingest.py"

#Correct dump_directory
    if not dump_directory.endswith("/"):
        dump_directory = dump_directory + "/"
        #dump_directory = dump_directory[:-1]
    if gcis_endpoint.endswith("/"):
        gcis_endpoint = gcis_endpoint[:-1]
    file_counter = 0

    for (root, dirs, files) in os.walk(dump_directory):
        for f in files:
            #print f
            file_counter = file_counter + 1
            #print file_counter
            fullFilePath = os.path.realpath(os.path.join(root,f))
            with open (fullFilePath) as item:
                json_item = json.load(item)
           
            gcis = GcisClient(gcis_endpoint)
            update_url = gcis_endpoint+"/book/" #+ json_item['uri']
            check_url = "%s%s" % (update_url, json_item['identifier']) 
            if requests.get(check_url, verify=False).status_code == 200:
                update_url = check_url
            
            #print update_url
            r = gcis.s.post(update_url, data=json_item, verify=False)
            r.raise_for_status()
            #print json_item
else:
    print "Argument for directory to ingest and URL endpoint required." 
#log.write("{} crawler finished. time elapsed: {}\n".format(str(datetime.datetime.now()), time_elapsed))
#log.close()
