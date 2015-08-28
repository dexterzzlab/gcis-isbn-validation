__author__ = 'torresal'

"""Notes for Programmer"""
"""Helpful links:
        http://dbpedia.org/sparql
        http://dbpedia.org/sparql?default-graph-uri=http%3A%2F%2Fdbpedia.org&query=select+distinct+%3Fbook+%3Fisbn%0D%0A++++where+%7B%0D%0A++++++%3Fbook+a+dbo%3ABook+.%0D%0A++++++%3Fbook+%3Fprop+%3Fobj+.%0D%0A++++++%3Fbook+dbp%3Aisbn+%3Fisbn+.%0D%0A++++%7D%0D%0A++++LIMIT+1000&format=text%2Fhtml&timeout=30000&debug=on
        https://pypi.python.org/pypi/Distance"""

import re,argparse, time
from isbn_hyphenate import hyphenate
from isbnlib import EAN13, clean, to_isbn13, meta, canonical, to_isbn10
from SPARQLWrapper import SPARQLWrapper, JSON

def RQUERY(r):
    #SPARQL query ISBNs from dbpedia
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    sparql.setQuery(r)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    print(r)
    #print(results)
    if len(results["results"]["bindings"]) != 0:
        print(results)
        pass
    return results["results"]["bindings"]

QUERY = """
                select distinct ?book ?prop ?obj
            where {
              ?book a dbo:Book .
              ?book ?prop ?obj .
              ?book dbp:isbn ?isbn .
              FILTER (regex(?isbn, "%s" ))
            }
            LIMIT 100
        """

#ERROR file
file = open("DBPEDIA-ERRORS.txt", "w")
DATE = ("DATE:" + time.strftime("%m/%d/%Y"))
TIME = ("MILITARY TIME:" + time.strftime("%H:%M:%S"))
file.write(DATE+"\n"+TIME+"\n")


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
        print('NO MANUAL GCIS PATH\n ALL GCIS BOOK JSON FORMATS WILL BE USED AS DEFAULT')

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

            print("GCIS-DEV\n\n\t", M, '\n\n\t', "isbn_original:", ISBNS, '\n\n\t', "isbn_mod:", V13, "\n\n")

        #DBpedia ISBN formats
            a = ISBNS
            b = canonical(CISBN)
            c = to_isbn10(CISBN)
            d = hyphenate(to_isbn10(CISBN))
            e = to_isbn13(CISBN)
            f = hyphenate(to_isbn13(CISBN))
            g = V13
            h = "ISBN {}" .format(CISBN)
            i = "ISBN {}" .format(canonical(CISBN))
            j = "ISBN {}" .format(hyphenate(to_isbn13(CISBN)))
            k = "ISBN {}" .format(V13)
            l = "ISBN {}" .format(to_isbn10(CISBN))
            m = "ISBN {}" .format(hyphenate(to_isbn10(CISBN)))

            tests = [a,b,c,d,e,f,g,h,i,j,k,l,m]

            for indie in tests:
                r = QUERY % indie
                RQUERY(r)
                if len(RQUERY(r)) != 0:
                    print(RQUERY(r))
                    break


        except:
            Error = '\n\t######## PROBLEM #######\n\tTitle:{}\n\tGCIS-ISBN:{}\n\tIdentifier:{}\n\n'.format(TITLE, ISBNS, IDEN)
            print(Error)
            file.write(Error)

if __name__ =='__main__':
    main()



