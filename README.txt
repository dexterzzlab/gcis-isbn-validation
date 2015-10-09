GCIS ISBN Validation

Purpose
This set of scripts is designed to validate the isbn information we have for all the books in GCIS

Process
1. Use 'python get_books.py [GCIS book JSON endpoint]' to retrieve json dumps for all books from the GCIS book JSON endpoint
2. Use 'python normalize_isbn.py [top level GCIS script-created directory]' to normalize all the JSON files to ISBN13 if an ISBN13 version exists
3. Use 'python get_loc_xml.py [top level GCIS script-created directory]' to check existing isbn entries in json files against Library of Congress Database

At this point, the following directories will be created:

/gcis-[DATE]T[TIME] (This is in ISO8601 spec)
--> book
--> book-loc
--> book-normalized
--> book-to-fix
--> book-to-ingest


These folders contain the following:
[ book ] : Original JSON files from data.globalchange.gov
[ book-loc ] : XML files for matched ISBNs from Library of Congress (Separated into isbn-13-match, isbn-other-match, and isbn-problem subfolders)
[ book-normalized ] : Normalized JSON files (Separated into isbn-13, isbn-none, and isbn-other subfolders)
[ book-to-fix ] : Books where ISBNs did not match Library of Congress database. These need to be manually handled.
[ book-to-ingest ] : JSON files of the cleaned/normalized and verified books that are ready to ingest into GCIS

To ingest this data into GCIS elastic search, you simply run the following:
'python gcis_es_crawler.py gcis-[DATE]T[TIME]/book-to-ingest'

Notes:
Looks like there are only 3 isbn files missing
