#!/bin/bash


python get_books.py
source ../facetview-gcis/env/bin/activate
python normalize_isbn.py
python get_loc_xml.py
