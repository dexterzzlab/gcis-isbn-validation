import requests
from isbnlib import EAN13, clean, canonical
import os
import json
import datetime

top_dir = "output_%s"%datetime.date.today()+"/"

book_dump_dir = "normalization_output/"

if not os.path.isdir(top_dir):
    os.makedirs(top_dir)
if not os.path.isdir(top_dir+book_dump_dir):
    os.makedirs(top_dir+book_dump_dir)
if not os.path.isdir(top_dir+book_dump_dir+"isbn13_book/"):
    os.makedirs(top_dir+book_dump_dir+"isbn13_book/")
if not os.path.isdir(top_dir+book_dump_dir+"problem_book/"):
    os.makedirs(top_dir+book_dump_dir+"problem_book/")
if not os.path.isdir(top_dir+book_dump_dir + "non13_book"):
    os.makedirs(top_dir+book_dump_dir+"non13_book")

problem_log = open(top_dir+"problem_log.txt", "w")
problem_log.write("Normalization Problem Files: \n")

problem_json = []
config = open("isbn.conf", "r")


def get_book_dir():
    for line in config:
        if line.startswith("book_json_loc"):
            temp = line.split(":")[1].rstrip("\n")
            temp = temp.replace(" ", "")
            return temp

#book_dir = get_book_dir()
book_dir = top_dir+"book/"
directory = "gcis-isbn-validation/%s"%book_dir

problem_count = 0
normal_count = 0
other_count = 0
total_count = 0

for (root, dirs, files) in os.walk(book_dir):
    for f in files:
        with open(book_dir+f) as item:
            json_item = json.load(item)
            book_isbn = json_item['isbn']
            if book_isbn is not None:
                if book_isbn == "None": 
                    with open(top_dir+"normalization_output/problem_book/"+str(f),'w') as jsonFile:
                        jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',',': ')))
                        problem_log.write(json_item['identifier']+"\n")
                        problem_count = problem_count + 1
                else:
                    book_isbn = clean(book_isbn)
                    if EAN13(book_isbn) != None:
                        book_isbn = EAN13(book_isbn)
                        json_item['isbn'] = book_isbn
                        with open(top_dir+"normalization_output/isbn13_book/"+str(f), 'w') as jsonFile:
                            jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',', ': ')))
                            normal_count = normal_count + 1
                    else:
                        with open(top_dir+"normalization_output/non13_book/"+str(f), 'w') as jsonFile:
                            jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',', ': ')))
                            problem_log.write(json_item['identifier']+"\n")
                            other_count = other_count + 1
            else:
                with open(top_dir+"normalization_output/problem_book/"+str(f),'w') as jsonFile:
                    jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',',': ')))
                    problem_log.write(json_item['identifier']+"\n")
                    problem_count = problem_count + 1

total_count = normal_count+problem_count+other_count
problem_log.write("Problem files: %s"%problem_count+"\n")
problem_log.write("ISBN13 files: %s"%normal_count+"\n")
problem_log.write("Non ISBN 13 files: %s"%other_count+"\n")
problem_log.write("Total files: %s"%total_count+"\n")

