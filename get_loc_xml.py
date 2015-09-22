import re, requests
from isbnlib import EAN13, clean, canonical
import os
import json
import datetime
import xml.etree.cElementTree as ET
#import logging

#log = 
top_dir = "output_%s"%datetime.date.today()+"/"

#error_log = open("book_error_log", "w")
problem_json = []
config = open("isbn.conf", "r")


non13_dir = top_dir+"normalization_output/non13_book/"

valid13_dir = top_dir+"normalization_output/isbn13_book/"



loc_xml_dir = top_dir+"get_loc_xml_result/"

match_dir_13 = loc_xml_dir + "match_13/"

problem_dir = loc_xml_dir + "problem_13/"

match_dir_other = loc_xml_dir + "match_other/"

problem_dir_other = loc_xml_dir +  "problem_other/"



log = open(top_dir+"get_loc_xml_log.txt", 'w')



if not os.path.isdir(loc_xml_dir):
    os.makedirs(loc_xml_dir)
if not os.path.isdir(match_dir_13):
    os.makedirs(match_dir_13)
if not os.path.isdir(problem_dir):
    os.makedirs(problem_dir)
if not os.path.isdir(match_dir_other):
    os.makedirs(match_dir_other)
if not os.path.isdir(problem_dir_other):
    os.makedirs(problem_dir_other)

problem_isbn_counter = 0
isbn13_file_counter = 0
for (root, dirs, files) in os.walk(valid13_dir):
    for f in files:
        fname = f[:-5]+".xml"
        with open(valid13_dir+f) as item:
            json_item = json.load(item)
            book_isbn = json_item['isbn']
            loc_xml = requests.get('http://lx2.loc.gov:210/lcdb?version=1.1&operation=searchRetrieve&query=bath.isbn={}&maximumRecords=1&recordSchema=mods'.format(book_isbn))
            loc_xml = loc_xml.text
            if loc_xml != None:
               with open(match_dir_13+str(fname), 'w') as item:
                    item.write(loc_xml)
                    isbn13_file_counter += 1
            else:
                with open(problem_dir+str(fname), 'w') as item:
                    problem_isbn_counter+=1
                    log.write(json_item['isbn']+"\n")
                    item.write(json_item)

non_isbn13_counter = 0
for (root, dirs, files) in os.walk(non13_dir):
    for f in files:
        fname = f[:-5]+".xml"
        with open(non13_dir+f) as item:
            json_item = json.load(item)
            book_isbn = json_item['isbn']
            loc_xml = requests.get('http://lx2.loc.gov:210/lcdb?version=1.1&operation=searchRetrieve&query=bath.isbn={}&maximumRecords=1&recordSchema=mods'.format(book_isbn))
            loc_xml = loc_xml.text
            if loc_xml != None:
               with open(match_dir_other+str(fname), 'w') as item:
                    item.write(loc_xml)
                    non_isbn13_counter += 1
            else:
                with open(problem_dir_other+str(fname), 'w') as item:
                    item.write(json_item)
                    problem_isbn_counter+=1
                    log.write(json_item['isbn']+"\n")

 
log.write("isbn 13 match: %s" % isbn13_file_counter + "\n")
log.write("non isbn13 match: %s" % non_isbn13_counter + "\n")
log.write("problem files: %s" %problem_isbn_counter)
