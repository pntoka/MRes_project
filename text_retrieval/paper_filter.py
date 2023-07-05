import os
import json
from bs4 import BeautifulSoup
import re
from tqdm import tqdm

def get_abstract(doi, save_dir):
    with open(os.path.join(save_dir,doi.replace('/', '-')+'.txt'), 'r', encoding='utf-8') as f:
        html_xml_str = f.read()
    soup = BeautifulSoup(html_xml_str, 'xml')
    abstract = soup.find('abstract')
    if abstract is None:
        return None
    return abstract.find('para').get_text()

def abstract_filter(abstract, keywords):
    if abstract is None:
        return False
    for keyword in keywords:
        if keyword in abstract:
            return True
    return False

def get_doi_materials(data_entry):
    materials  = list(data_entry['all_materials'].keys())
    return materials

def materials_filter(materials, keywords):
    for material in materials:
        for keyword in keywords:
            if keyword in material:
                return True
    return False

def filter_dois(data, exclude_list, abs_keywords, mat_keywords, save_dir):
    pattern = r"_no_\d+$"
    doi_results = []
    for entry in tqdm(data, desc='Filtering DOIs'):
        abstract_hit = 0
        material_hit = 0
        if re.search(pattern, entry['doi']):
            doi = entry['doi'].replace(re.search(pattern, entry['doi']).group(), '')
            if doi not in exclude_list:
                abstract = get_abstract(doi, save_dir)
                if abstract_filter(abstract, abs_keywords):
                    abstract_hit = 1
            materials = get_doi_materials(entry)
            if materials_filter(materials, mat_keywords):
                material_hit = 1
        else:
            doi = entry['doi']
            if doi not in exclude_list:
                abstract = get_abstract(doi, save_dir)
                if abstract_filter(abstract, abs_keywords):
                    abstract_hit = 1
            materials = get_doi_materials(entry)
            if materials_filter(materials, mat_keywords):
                material_hit = 1
        doi_results.append((entry['doi'], abstract_hit, material_hit))
    return doi_results

def get_data(dir):
    with open(dir, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data
