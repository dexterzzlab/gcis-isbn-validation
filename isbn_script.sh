#!/bin/bash


python get_books.py
source ../facetview-gcis/env/bin/activate
python loc_isbn_validator.py

