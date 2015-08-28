__author__ = 'torresal'

""""Note: this script is only intended to retrieve metadata from Google database"""

import re, time
from isbnlib import EAN13, clean, meta, canonical

#ERROR file
file = open("GOOGLE-ERRORS.txt", "w")
file2 = open("GOOGLE-DATA.txt", "w")
DATE = ("DATE:" + time.strftime("%m/%d/%Y"))
TIME = ("MILITARY TIME:" + time.strftime("%H:%M:%S"))
file.write(DATE+"\n"+TIME+"\n")
file2.write(DATE+"\n"+TIME+"\n")

#Parses url.json#
def parse(url):
    import requests
    r = requests.get(url, verify = False)
    JSONdict = r.json()
    return JSONdict
GCIS = 'https://gcis-search-stage.jpl.net:3000/book.json?all=1'
GCISPAR = parse(GCIS)

for x in range(len(GCISPAR)):
    try:
#Extracts book identifier from GCIS#
        IDEN = GCISPAR[x]["identifier"]
        match =  re.search(r'.*/(.*?)\..*?$', GCIS)
        if match:
            FILETYPE = match.groups()[0]
#HREF = url that leads to book.json in GCIS-DEV
        HREF = 'https://gcis-search-stage.jpl.net:3000/{}/{}.json' .format(FILETYPE,IDEN)
        HREFPAR = parse(HREF)
#Extracts book title and isbn from GCIS-DEV
        d = dict(HREFPAR)
        TITLE = d['title']
        ISBNS = d['isbn']
#Cleans ISBNS to only conatian valid characters
        CISBN = clean(ISBNS)
#V13 = validated canonical ISBN-13
        V13 = EAN13(CISBN)
        if V13 is None:
            V13 = canonical(CISBN)
        M = parse(HREF)
        v = meta(V13, service = 'goob', cache ='default')
        GCISDATA = "GCIS-DEV\n\n\t{}\n\n\tisbn_original:{}\n\n\tisbn_mod:{}\n\n" .format(M, ISBNS, V13)
        APIDATA = "GOOB\n\n\t{}\n\n------------\n\n" .format(v)
        print("GCIS-DEV\n\n\t", M, '\n\n\t', "isbn_original:", ISBNS, '\n\n\t', "isbn_mod:", V13, "\n\n")
        print ("GOOB\n\t","\n\t", v, '\n')
        file2.write(GCISDATA)
        file2.write(APIDATA)


    except:
        Error = '\n\t######## PROBLEM #######\n\tTitle:{}\n\tGCIS-ISBN:{}\n\tIdentifier:{}\n\n'.format(TITLE, ISBNS, IDEN)
        print(Error)
        file.write(Error)

