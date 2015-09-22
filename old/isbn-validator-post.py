__author__ = 'torresal'


import re, sys, requests, argparse,yaml
from isbnlib import EAN13, clean, canonical

#Login process to post onto GCIS-DEV
def main():
#Commnd line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-log', '--login', help="Route path to Gcis.conf YAML file")
    parser.add_argument('-url', '--gcis', help='INSERT EITHER: https://data.globalchange.gov OR https://gcis-search-stage.jpl.net:3000')
    parser.add_argument('-name', '--username', help = "Insert GCIS username")
    parser.add_argument('-pw', '--apikey', help = "Insert GCIS username's api key")
    args = parser.parse_args()
    gcis = 'https://data.globalchange.gov'
    gcisdev = 'https://gcis-search-stage.jpl.net:3000'

#Extracts login info from Gcis.conf
    if args.login:
        a = open(args.login, "r")
        list = (yaml.load(a))
        diction = list[0]
        path = diction['url']
        user = diction['userinfo']
        key = diction['key']
        print(path+'\n'+user+'\n'+key)
    else:
        pass
    if args.gcis == gcis:
        print(args.gcis)
    elif args.gcis == gcisdev:
        print(args.gcis)
    else:
        print('NO MANUAL ENDPOINT (Ignore if using Config file)')
    if args.username:
        print(args.username)
    else:
        print('NO MANUAL USERNAME (Ignore if using Config file)')
    if args.apikey:
        print(args.apikey)
    else:
        print('NO MANUAL API KEY (Ignore if using Config file)')

#Credentials

        path = diction['url']
        if diction['url'] is None:
            path = args.gcis
        else:
            path = gcisdev

        user = diction['userinfo']
        if diction['userinfo'] is None:
            user = args.username

        key = diction['key']
        if diction['key'] is None:
            key = args.apikey


#Parses url.json#
    def parse(url):
        import requests
        r = requests.get(url, verify = False)
        JSONdict = r.json()
        return JSONdict
    GCIS = 'https://gcis-search-stage.jpl.net:3000/book.json?all=1'
    GCISPAR = parse(GCIS)

    for x in range(len(GCISPAR)):
    #Extracts book identifier from GCIS#
            IDEN = GCISPAR[x]["identifier"]
            match =  re.search(r'.*/(.*?)\..*?$', GCIS)
            if match:
                FILETYPE = match.groups()[0]
    #HREF = url that leads to book.json in GCIS-DEV
            HREF = 'https://gcis-search-stage.jpl.net:3000/{}/{}.json' .format(FILETYPE,IDEN)
    #HREF for either GCIS or GCIS-DEV
            #HREF = '{}//{}/{}.json' .format(path, FILETYPE, IDEN)
    #test
            #HREF = 'https://gcis-search-stage.jpl.net:3000/book/305e4144-39d2-4d84-8843-3f502ab890e0.json'
            HREFPAR = parse(HREF)
            print(HREFPAR)
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
    #For possible future implementation of adding original isbn into the JSON dictionary.
            """M["isbn"] = V13
            M["org_isbn"] = ISBNS"""
            print(M, '\n\t', "isbn_original:", ISBNS)
    #Posts updated JSON dictionary back into GCIS-DEV using credentials from command line arguments.
            s = requests.Session()
            s.auth = ( user , key )
            s.headers.update({'Accept': 'application/json'})
            r = s.post(HREF, data = M , verify = False)
            r.raise_for_status()
            sys.exit()

if __name__ == '__main__':
    main()