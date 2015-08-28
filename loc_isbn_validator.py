__author__ = 'torresal'

""""Note: this script is only intended to retrieve metadata from the Library of Congress database"""

import re, requests,time
from isbnlib import EAN13, clean, canonical
from pprint import pprint

#ERROR file
file = open("LOC-ERRORS.txt", "w")
file2 = open("LOC-DATA.txt", "w")
DATE = ("DATE:" + time.strftime("%m/%d/%Y"))
TIME = ("MILITARY TIME:" + time.strftime("%H:%M:%S"))
file.write(DATE+"\n"+TIME+"\n")
file2.write(DATE+"\n"+TIME+"\n")

#Parses url.json#
def parse(url):
    r = requests.get(url, verify = False)
    JSONdict = r.json()
    return JSONdict
GCIS = 'https://gcis-search-stage.jpl.net:3000/book.json?all=1'
GCISPAR = parse(GCIS)

#Parses xml url
def xmlparse(url):
    r = requests.get(url, verify = False)
    xml = r.text
    return xml

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
        locapi = 'http://lx2.loc.gov:210/lcdb?version=1.1&operation=searchRetrieve&query=bath.isbn={}&maximumRecords=1&recordSchema=mods' .format(V13)
        results = xmlparse(locapi)
        GCISDATA = "GCIS-DEV\n\n\t{}\n\n\tisbn_original:{}\n\n\tisbn_mod:{}\n\n" .format(M, ISBNS, V13)
        APIDATA = "LOC\n\n\t{}\n\n------------\n\n" .format(results)
        print("GCIS-DEV\n\t", M, '\n\n\t', "isbn_original:", ISBNS, '\n\n\t', "isbn_mod:", V13, "\n\n")
        print('LOC\n\t',results)
        file2.write(GCISDATA)
        file2.write(APIDATA)

    except:
        Error = '\n\t######## PROBLEM #######\n\tTitle:{}\n\tGCIS-ISBN:{}\n\tIdentifier:{}\n\n'.format(TITLE, ISBNS, IDEN)
        print(Error)
        file.write(Error)
