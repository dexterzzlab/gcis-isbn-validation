GCIS ISBN Validation

Purpose
This set of scripts is designed to validate the isbn information we have for all the books in GCIS

Process
(should be wrapped up in isbn_script.sh)
1. Use python get_books.py to retrieve JSON dumps from all books on data.globalchange.gov
2. Use python normalize_isbn.py to convert book isbn to isbn13 format, if it exists
3. Use python get_loc_xml.py to check if isbns exist on Library of Congress database

This process generates folders with the following:
Original JSON files from data.globalchange.gov
Normalized JSON files (Separated to ISBN13, non-ISBN13, and no ISBN subfolders)
XML files for matched ISBNs from Library of Congress (Separated to ISBN13, non-ISBN13, and problem file subfolders)


Notes:
Looks like there are only 3 isbn files missing
