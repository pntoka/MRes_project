import os
import json
from bs4 import BeautifulSoup
import re

def get_abstract(doi, save_dir):
    with open(os.path.join(save_dir,doi.replace('/', '-')+'.txt'), 'r', encoding='utf-8') as f:
        html_xml_str = f.read()
    soup = BeautifulSoup(html_xml_str, 'xml')
    abstract = soup.find('abstract')
    return abstract.find('para').get_text()

def abstract_filter(abstract, keywords):
    for keyword in keywords:
        if keyword in abstract:
            return True
    return False

def get_doi_materials(doi, data_entry):
    materials  = list(data_entry['all_materials'].keys())
    return materials

def materials_filter(materials, keywords):
    for material in materials:
        for keyword in keywords:
            if keyword in material:
                return True
    return False

