# gcis-isbn-validator
Scripts used to validate and clean up ISBN formats in GCIS-DEV.

What this script does?
=====================
*"isbn-validator-post"* is used to **ONLY** extract, clean, and repost onto GCIS-DEV

Details:

    1. Accepts Gcis.conf credentials as command line argument [example: https://metacpan.org/pod/Gcis::Client#CONFIGURATION]
    2. Parses metadata from GCIS-DEV into a JSON dictionary 
    3. Extracts the "isbn" key from the dictionary and updates the isbn to a cannonical ISBN 13 character format
    4. Posts updated JSON dictionary back into GCIS-DEV using credentials from command line arguments.

Other scripts are used to compare metadata. If the metadata from GCIS-DEV matches the metadata from other database, then the cleaned ISBN is considered valid. Each script is dedicated to a specfic database (World Cat, Google, Library of Congress, etc.).

Each of the following scripts:

    1. *Extracts all ISBN formats from GCIS-DEV 
    2. Converts ISBN to a validated ISBN-13 format 
    3. Writes metadata from GCIS-DEV and other Database onto text file [example: "{database}-DATA.txt"].
    4. Writes errors from GCIS-DEV and other Database onto text file [example: "{database}-ERROR.txt"].

Requirements
============
1. Python:

  - Python 3.4 
  
2. API access: (isbn-validator-post use only)

    Positional arg:
    
      Gcis.conf (YAML format) file containing:
      
        - url
        - userinfo
        - key
        
    Optional arg: (*use only if Gcis.conf file is not avaliable)
    
        -username and api key

Installation
============
Clone git repo "gcis-isbn-validator".


Usage
=====
To execute script, open command line and change directory to location of git repo. 

Enter into command line:

    ~python [SCRIPT.py]

*Some scripts may require extra arguments. To view them, insert a "--help" flag at the end of script 

    ~python [SCRIPT.py] --help
    
Notes/References
================
*Scripts that require command line arguments:

        - isbn-validator-post.py
        - isbndb_isbn_validator.py
        
Incomplete Scripts:

        - amazon_isbn_validator.py
        
                Issue: Implementing Amazon Request into script and parsing the Amazon metadata
                        
        - dbpedia_isbn_valdator.py 
        
                Issue: No ISBN results when running ISBN SPARQL query
        


