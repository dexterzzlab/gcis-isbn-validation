__author__ = 'torresal'

"""Notes for Programmer"""
"""Helpful links:
        http://docs.aws.amazon.com/AWSECommerceService/latest/DG/EX_LookupbyISBN.html
        http://docs.aws.amazon.com/AWSECommerceService/latest/GSG/SubmittingYourFirstRequest.html
        http://associates-amazon.s3.amazonaws.com/signed-requests/helper/index.html
   Needed Credentials:
        AWS account Accesskey
        Amazon Associatetag"""

""""Note: this script is only intended to retrieve metadata from the Amazon database"""

import re, requests,time, argparse
from isbnlib import EAN13, clean, canonical

#ERROR file
file = open("AMAZON-ERRORS.txt", "w")
file2 = open("AMAZON-DATA.txt", "w")
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

def main():
#Commnd line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-awsid', '--AWSAccessKeyID', help = "Insert AWS Access Key ID")
    parser.add_argument('-astag', '--AssociateTag', help = "Insert Amazon Associate Tag")
    args = parser.parse_args()

    if args.AWSAccessKeyID:
        print(args.AWSAccessKeyID)
    else:
        print('NO AWS Access Key ID')

    if args.AssociateTag:
        print(args.AssociateTag)
    else:
        print('NO Amazon Associate Tag')


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
    #MV13 = M["isbn"] = V13
    #ORGISBN = M["org_isbn"] = ISBNS
            locapi = 'http://lx2.loc.gov:210/lcdb?version=1.1&operation=searchRetrieve&query=bath.isbn={}&maximumRecords=1&recordSchema=mods' .format(V13)
            results = xmlparse(locapi)
            GCISDATA = "GCIS-DEV\n\n\t{}\n\n\tisbn_original:{}\n\n\tisbn_mod:{}\n\n" .format(M, ISBNS, V13)
            APIDATA = "AMAZON\n\n\t{}\n\n------------\n\n" .format(results)
            print("GCIS-DEV\n\t", M, '\n\n\t', "isbn_original:", ISBNS, '\n\n\t', "isbn_mod:", V13, "\n\n")
            print('AMAZON\n\t',results)
            file2.write(GCISDATA)
            file2.write(APIDATA)

        except:
            Error = '\n\t######## PROBLEM #######\n\tTitle:{}\n\tGCIS-ISBN:{}\n\tIdentifier:{}\n\n'.format(TITLE, ISBNS, IDEN)
            print(Error)
            file.write(Error)