__author__ = 'torresal'

""""Note: this script is only intended to retrieve metadata from ISBNDB database"""

import re, argparse, time
from isbnlib import EAN13, clean, canonical

#ERROR file
file = open("ISBNDB-ERRORS.txt", "w")
file2 = open("ISBNDB-DATA.txt", "w")
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


def main():
#Commnd line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-apikey', '--isbndbkey', help = "Insert ISBNDB apikey")
    args = parser.parse_args()

    if args.isbndbkey:
        print(args.isbndbkey)
    else:
        print('NO MANUAL API KEY')

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
            apikey = args.isbndbkey
            if args.isbndbkey is None:
                apikey = 'XOATAY1G'
            data = 'http://isbndb.com/api/v2/json/{}/book/{}'.format(apikey, V13)
            v = parse(data)
            GCISDATA = "GCIS-DEV\n\n\t{}\n\n\tisbn_original:{}\n\n\tisbn_mod:{}\n\n" .format(M, ISBNS, V13)
            APIDATA = "ISBNDB\n\n\t{}\n\n------------\n\n" .format(v)
            print("GCIS-DEV\n\n\t", M, '\n\n\t', "isbn_original:", ISBNS, '\n\n\t', "isbn_mod:", V13, "\n\n")
            print ("ISBNDB\n\n\t", v, '\n\n')
            if v['error']:
                file.write(v['error']+"\n")
            else:
                pass
#Writing Metadata onto file2
            file2.write(GCISDATA)
            file2.write(APIDATA)

        except:
            Error = '\n\t######## PROBLEM #######\n\tTitle:{}\n\tGCIS-ISBN:{}\n\tIdentifier:{}\n\n'.format(TITLE, ISBNS, IDEN)
            print(Error)
            file.write(Error)

if __name__ =='__main__':
    main()