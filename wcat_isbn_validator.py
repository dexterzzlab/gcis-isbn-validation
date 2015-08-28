__author__ = 'torresal'

""""Note: this script is only intended to retrieve metadata from Wolrd Cat database"""

import re,argparse, time
from isbnlib import EAN13, clean, meta, canonical

#ERROR file
file = open("WCAT-ERRORS.txt", "w")
file2 = open("WCAT-DATA.txt", "w")
DATE = ("DATE:" + time.strftime("%m/%d/%Y"))
TIME = ("MILITARY TIME:" + time.strftime("%H:%M:%S"))
file.write(DATE+"\n"+TIME+"\n")
file2.write(DATE+"\n"+TIME+"\n\n")

#Parses url.json#
def parse(url):
    import requests
    r = requests.get(url, verify = False)
    JSONdict = r.json()
    return JSONdict

def main():
#Commnd line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', '--GCIS', help = "Insert url path to GCIS book in JSON format [ex.'https://gcis-search-stage.jpl.net:3000/book.json?all=1'] ")
    args = parser.parse_args()
    GCIS = args.GCIS


    if GCIS is None:
        GCIS = 'https://gcis-search-stage.jpl.net:3000/book.json?all=1'
        print('NO MANUAL GCIS PATH\nALL GCIS BOOK JSON FORMATS WILL BE USED AS DEFAULT')

GCISPAR = parse(GCIS)
HREF =

for x in range(len(GCISPAR)):
#Extracts book identifier from GCIS#
        IDEN = GCISPAR[x]["identifier"]
        match =  re.search(r'.*/(.*?)\..*?$', GCIS)
        if match:
            FILETYPE = match.groups()[0]
    #HREF = url that leads to book.json in GCIS-DEV
        try:
            HREF = 'https://gcis-search-stage.jpl.net:3000/{}/{}.json' .format(FILETYPE,IDEN)
            #HREF = 'https://gcis-search-stage.jpl.net:3000/book/13b8b4fc-3de1-4bd8-82aa-7d3a6aa54ad5.json'
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
            v = meta(V13, service = 'wcat', cache ='default')
            GCISDATA = "GCIS-DEV\n\n\t{}\n\n\tisbn_original:{}\n\n\tisbn_mod:{}\n\n" .format(M, ISBNS, V13)
            APIDATA = "WorldCat\n\n\t{}\n\n------------\n\n" .format(v)
            print("GCIS-DEV\n\n\t", M, '\n\n\t', "isbn_original:", ISBNS, '\n\n\t', "isbn_mod:", V13, "\n\n")
            print ("WorldCat\n\n\t", v, '\n\n')
            file2.write(GCISDATA)
            file2.write(APIDATA)

        except:
            Error = '\n\t######## PROBLEM #######\n\tTitle:{}\n\tGCIS-ISBN:{}\n\tIdentifier:{}\n\n'.format(TITLE, ISBNS, IDEN)
            print(Error)
            file.write(Error)

if __name__ =='__main__':
    main()

