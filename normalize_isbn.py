import requests
from isbnlib import EAN13, clean, canonical
import os
import json
import datetime
import sys

#top_dir = "output_%s"%datetime.date.today()+"/"

#book_dump_dir = "normalization_output/"

if len(sys.argv) > 1:
    if sys.argv[1] is not None:
        book_top_path = sys.argv[1]
        if not os.path.isdir(book_top_path):
            print "Path parameter for GCIS book dump is not valid"
        
        else:
            #correct top_dir if it doesn't end with /
            if not book_top_path.endswith("/"):
                book_top_path = "%s/"%(book_top_path)
           
            #establish book dump directory
            book_dir = "%sbook/"%(book_top_path)
            
           

            #gcis-TIMESTAMP/book-normalized
            #book_top_path = book_dir + norm_dir
            norm_dir = "book-normalized/"
            norm_top_path = "%s%s"%(book_top_path, norm_dir)

            if not os.path.isdir(norm_top_path):
                os.makedirs(norm_top_path)

            #gcis-TIMESTAMP/book-normalized/isbn-13
            isbn_13_path = "%sisbn-13/"%(norm_top_path)
            if not os.path.isdir(isbn_13_path):
                os.makedirs(isbn_13_path)

            #gcis-TIMESTAMP/book-normalized/isbn-other
            isbn_other_path = "%sisbn-other/"%(norm_top_path)
            if not os.path.isdir(isbn_other_path):
                os.makedirs(isbn_other_path)

            #gcis-TIMESTAMP/book-normalized/isbn-none
            isbn_none_path = "%sisbn-none/"%(norm_top_path)
            if not os.path.isdir(isbn_none_path):
                os.makedirs(isbn_none_path)

            problem_log = open(norm_top_path+"problem_log.txt", "w")
            problem_log.write("Files without ISBN-13 Format: \n")

            problem_json = []

#            book_dir = top_dir+"book/"
#            directory = "gcis-isbn-validation/%s"%book_dir
            
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
                                with open("%s%s"%(isbn_none_path,str(f)),'w') as jsonFile:
                                    jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',',': ')))
                                    problem_log.write(json_item['identifier']+"\n")
                                    problem_count = problem_count + 1
                            else:
                                book_isbn = clean(book_isbn)
                                if EAN13(book_isbn) != None:
                                    book_isbn = EAN13(book_isbn)
                                    json_item['isbn'] = book_isbn
                                    with open("%s%s"%(isbn_13_path,str(f)), 'w') as jsonFile:
                                        jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',', ': ')))
                                        normal_count = normal_count + 1
                                else:
                                    book_isbn = book_isbn.replace("-", "")
                                    json_item['isbn'] = book_isbn
                                    with open("%s%s"%(isbn_other_path,str(f)), 'w') as jsonFile:
                                        jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',', ': ')))
                                        problem_log.write(json_item['identifier']+"\n")
                                        other_count = other_count + 1
                        else:
                            with open("%s%s"%(isbn_none_path,str(f)),'w') as jsonFile:
                                jsonFile.write(json.dumps(json_item, sort_keys=True, indent=4, separators=(',',': ')))
                                problem_log.write(json_item['identifier']+"\n")
                                problem_count = problem_count + 1

            total_count = normal_count+problem_count+other_count
            problem_log.write("\nFiles without any ISBN: %s"%problem_count+"\n")
            problem_log.write("Files that have an ISBN, but are not ISBN-13 format: %s"%other_count+"\n")
            problem_log.write("ISBN13 files: %s"%normal_count+"\n")
            
            problem_log.write("Total files: %s"%total_count+"\n")
    else:
        print "Requires parameter for GCIS book dump"

else:
    print "Requires parameter for GCIS book dump"
