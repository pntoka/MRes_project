import os
import json
from bs4 import BeautifulSoup

def get_abstract(doi, save_dir):
    with open(os.path.join(save_dir,doi.replace('/', '-')+'.txt'), 'r', encoding='utf-8') as f:
        html_xml_str = f.read()
    soup = BeautifulSoup(html_xml_str, 'xml')
    abstract = soup.find('abstract')
    return abstract.find('para').get_text()
