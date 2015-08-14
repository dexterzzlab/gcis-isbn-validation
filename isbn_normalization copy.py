__author__ = 'torresal'

"""# Notes #
- update entries in GCIS by using the GCIS API
- use the book identifier in GCIS API to update ISBN in GCIS
- Cause of 'Problem'
        - Does not have isbn
        - Does not have randomly generated identifier

Requirements

by default, look for the $HOME/etc/Gcis.conf file
if it exists, pull the GCIS endpoint, username, and API key from there
for example:
    ./ISBN_ normalization.py
if it doesn't exist, these values should be specified from the command-line
    takes 3 required arguments:
        GCIS endpoint (e.g. https://data.globalchange.gov or https://gcis-search-stage.jpl.net:3000)
        username
        API key
for example:
    ./ISBN_normalization.py
    Error: cannot resolve GCIS endpoint and auth creds. No Gcis.conf detected. Please specify them on the command line.
    ./ISN_normalization.py --user gmanipon --key a2kdkdu3jdasdf https://gcis-search.stage.jpl.net:3000


import re, sys, requests, argparse, yaml
from isbnlib import EAN13, clean, to_isbn13

def main():
#Commnd line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-log', '--login', help="Route path to Gcis.conf YAML file")
    parser.add_argument('-url', '--gcis', help='INSERT EITHER: https://data.globalchange.gov OR https://gcis-search-stage.jpl.net:3000')
    parser.add_argument('-name', '--username', help = "Insert GCIS username")
    parser.add_argument('-pw', '--apikey', help = "Insert GCIS username's api key")
    parser.add_argument('-spq', '--endpoint', help = "Insert SPARQL endpoint url")
    args = parser.parse_args()
    gcis = 'https://data.globalchange.gov'
    gcisdev = 'https://gcis-search-stage.jpl.net:3000'
#Extracts login info from Gcis.conf
    if args.login:
        a = open(args.login, "r")
        list = (yaml.load(a))
        dict = list[0]
        path = dict['url']
        user = dict['userinfo']
        key = dict['key']
        print(path+'\n'+user+'\n'+key)
    else:
        pass
    if args.gcis == gcis:
        print(args.gcis)
    elif args.gcis == gcisdev:
        print(args.gcis)
    else:
        print('ERROR: NO MANUAL ENDPOINT (Ignore if using Config file)')
    if args.username:
        print(args.username)
    else:
        print('ERROR: NO MANUAL USERNAME (Ignore if using Config file)')
    if args.apikey:
        print(args.apikey)
    else:
        print('ERROR: NO MANUAL API KEY (Ignore if using Config file)')"""

#SPARQL endpoint
import pprint
from SPARQLWrapper import SPARQLWrapper, JSON, XML

sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql.setQuery("""
        select distinct ?book ?prop ?obj
    where {
      ?book a dbo:Book .
      ?book ?prop ?obj .
      ?book dbp:isbn ?isbn .
      FILTER (regex(?isbn, "0-553-05250-0"))
    }
    LIMIT 100
""")
sparql.setReturnFormat(XML)
results = sparql.query().convert()
#pprint.pprint(results)

"""for result in results["results"]["bindings"]:
    print(result["book"]["isbn"])"""



#Parses url.json#
def parse(url):
    import requests
    r = requests.get(url, verify = False)
    JSONdict = r.json()
    return JSONdict

test = parse('https://books.google.com/books?id=EivegccdDY4C&dq=9781847206701&source=gbs_navlinks_s')
print(test)

"""GCIS = '{}/book.json?all=1' .format(url)
GCISPAR = parse(GCIS)

for x in range(len(GCISPAR)):
    try:
#Extracts book identifier from GCIS#
        IDEN = GCISPAR[x]["identifier"]
        match =  re.search(r'.*/(.*?)\..*?$', GCIS)
        if match:
            FILETYPE = match.groups()[0]
#HREF = url that leads to book.json in GCIS-DEV
        HREF = '{}/{}/{}.json' .format(url,FILETYPE,IDEN)
        #HREF = 'https://gcis-search-stage.jpl.net:3000/book/13b8b4fc-3de1-4bd8-82aa-7d3a6aa54ad5.json'
        HREFPAR = parse(HREF)
#Extracts book title and isbn from GCIS-DEV
        d = dict(HREFPAR)
        TITLE = d['title']
        ISBNS = d['isbn']
#Cleans ISBNS to only conatian valid characters
        CISBN = clean(ISBNS)
#Converts all listed ISBNS to a ISBN-13 format
        C13 = to_isbn13(CISBN)
#V13 = validated canonical ISBN-13
        V13 = EAN13(C13)
        M = parse(HREF)
        MV13 = M["isbn"] = V13
        ORGISBN = M["org_isbn"] = ISBNS
        print(M, '\n\t', "isbn_original:", ISBNS)
        s = requests.Session()
        s.auth = (str(user), str(key))
        s.headers.update({'Accept': 'application/json'})
        r = s.post(HREF, data = M , verify = False)
        r.raise_for_status()
        sys.exit()
        #print('Title:', TITLE, '\nIdentifier:', IDEN,'\n',HREF,'\n\tISBN:', V13, '\n')
    except(TypeError, ValueError):
            print('\n\t######## PROBLEM #######\n','\tTitle:', TITLE,'\n\tGCIS-ISBN:', ISBNS,'\n\tIdentifier:', IDEN, '\n\n')

if __name__ =='__main__':
    main()"""












