Basic test case
* python test_hash.py

Assets:
1. srepy.py: full test case
1. png and pdf files: test prints
1. requirements.txt: modules in test environment
1. data_template.xlsx: excel file to generate csvs from
1. input/ : location of csv files to intake into srepy
1. output/ : location where output files should be written

Dev log
1. chart s&d
1. chart building breakdown
1. chart pds table
1. print assembly
1. class printer. iterates over geo,region, group
1. have run specific temp folder for individual pngs to stage before consolidating into each site's pdf pages (allows parallel runs of each geo if output pdfs are different)


Refining
1. Args
1. generate pattern list based on status
1. x axis is combi of building and status. Hatch only the non-existing statuses
1. config file

