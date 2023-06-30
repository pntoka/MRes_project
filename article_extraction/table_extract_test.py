from tabledataextractor import Table
# from tabledataextractor.input import from_any
from bs4 import BeautifulSoup
import bs4
import os
import numpy as np
import copy
path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests'
# file = '10.1021-acssuschemeng.9b00027.txt' #ACS
file = '10.1016-j.jphotochem.2019.112201.txt' #Elsevier xml
# file = '10.1016-j.optmat.2019.05.045.txt'
# file = '10.1002-slct.202202223.txt' #Wiley xml
# file = '10.1002-bio.3407.txt' #Wiley html
# file = '10.1039-C8AY00441B.txt' #RSC
# table = Table('https://pubs.acs.org/doi/10.1021/acssuschemeng.9b00027',2)
# table = Table('https://www.nature.com/articles/s41598-020-78070-2/tables/1')
# table = Table(os.path.join(path,file),1)
# print(table)
# table.print_raw_table()
with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
    html_xml_str = f.read()
soup = BeautifulSoup(html_xml_str, features='xml')
table_s = soup.find_all('table')
table = Table(table_s[0])
print(table)