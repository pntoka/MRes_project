from tabledataextractor import Table
import os
from bs4 import BeautifulSoup
path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests'
file = '10.1021-acssuschemeng.9b00027.txt'
# file = '10.1016-j.jphotochem.2019.112201.txt'
# table = Table('https://pubs.acs.org/doi/10.1021/acssuschemeng.9b00027',2)
# table = Table('https://link.springer.com/article/10.1007/s10853-012-6439-6/tables/1')
table = Table(os.path.join(path, file),2)
# table = Table(os.path.join(path,'10.1016-j.jphotochem.2019.112201.txt'),1)
print(table)
table.print_raw_table()
# with open(os.path.join(path, file), 'r', encoding='utf-8') as f:
#     html_xml_str = f.read()
# soup = BeautifulSoup(html_xml_str, features='xml')
# table = soup.find_all('table')
# print(len(table))
# simple = table[0].prettify()
# simple = str(table[0])
# print(type(simple))