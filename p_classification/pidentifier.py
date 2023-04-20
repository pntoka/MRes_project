import re
import os
import json
import pandas as pd
import numpy as np
import unicodedata


def get_data(path):
    '''
    Function to get data from json files
    '''
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def string_cleaner(content):
    '''
    Function to remove non-breaking spaces and unicode characters from strings
    '''
    if type(content[0]) == str:
        clean_str = []
        for element in content:
            clean_str.append(unicodedata.normalize('NFKD', element))
        return clean_str
    elif type(content[0]) == dict:
        clean_dict = []
        for element in content:
            element['name'] = unicodedata.normalize('NFKD', element['name'])
            element['content'] = string_cleaner(element['content'])
            clean_dict.append(element)
        return clean_dict

def get_section_names(data):
    '''
    Function to get section names from json files
    '''
    section_names = []
    sections = data['Sections']
    for element in sections:
        section_names.append(element['name'])
    return section_names


def get_subsection_names(data, section_name):
    '''
    Function to get subsection names from specific section in json files
    '''
    subsection_names = []
    sections = data['Sections']
    for element in sections:
        if element['name'] == section_name:
            for subelement in element['content']:
                subsection_names.append(subelement['name'])
    return subsection_names


def section_selector(section_names):
    '''
    Function to select section containing experimental methods based on keyword matching
    '''
    keywords = ['experimental', 'experimentation', 'experiment','materials and methods', 'methodology', 'methods','procedure','synthesis', 'hydrothermal', 'method']
    for section in section_names:
        if any(keyword.lower() in section.lower() for keyword in keywords):
            section_name = section
            return section_name


def subsection_selector(subsection_names):
    '''
    Function to select subsection containing synthesis methods based on keyword matching
    '''
    keywords = ['synthesis', 'synthes', 'hydrothermal', 'preparation', 'methods', 'experimental']
    for subsection in subsection_names:
        if any(keyword.lower() in subsection.lower() for keyword in keywords):
            subsection_name = subsection
            return subsection_name
        

def get_section_content(data, section_name):
    '''
    Function to get content of selected section
    '''
    sections = data['Sections']
    for element in sections:
        if element['name'] == section_name:
            section_content = element['content']
    return section_content


def get_subsection_content(data, section_name, subsection_name):
    '''
    Function to get content of selected subsection
    '''
    sections = data['Sections']
    for element in sections:
        if element['name'] == section_name:
            for subelement in element['content']:
                if subelement['name'] == subsection_name:
                    subsection_content = subelement['content']
    return subsection_content


def content_checker(data, section_name):
    '''
    Function to check if selected section contains subsections
    '''
    sections = data['Sections']
    for element in sections:
        if element['name'] == section_name:
            if type(element['content'][0]) == dict:
                return True   # section contains subsections
            elif type(element['content'][0]) == str:
                return False   # section does not contain subsections


def synthesis_methods(data):
    '''
    Function to extract synthesis methods from json files
    '''
    section_names = get_section_names(data)
    section_name = section_selector(section_names)    # select section containing experimental information
    if section_name is None:
        return None
    if content_checker(data, section_name) == True:   # check if section contains subsections
        subsection_names = get_subsection_names(data, section_name)
        subsection_name = subsection_selector(subsection_names)   # select subsection containing synthesis methods
        if subsection_name is None:
            return None
        subsection_content = get_subsection_content(data, section_name, subsection_name)
        subsection_content = string_cleaner(subsection_content)
        return subsection_content
    elif content_checker(data, section_name) == False:
        section_content = get_section_content(data, section_name)
        section_content = string_cleaner(section_content)
        return section_content
    

def get_synthesis_methods(path):
    '''
    Function to extract synthesis methods from all json files in a folder and return them as a dataframe
    '''
    p_results = pd.DataFrame(columns=['DOI','paragraphs'])
    for file in os.listdir(path):
        if file.endswith('.json'):
            # print(file)        # uncomment to see which files are being processed
            data = get_data(path + '/' + file)
            paragraphs = synthesis_methods(data)
            doi = data['DOI']
            row = {'DOI': doi, 'paragraphs': paragraphs}
            new_df = pd.DataFrame([row])
            p_results = pd.concat([p_results, new_df], axis=0, ignore_index=True)
    return p_results

def dict_to_str(data):
    '''
    Function to extract paragraphs from dictionary as list of strings
    '''
    paragraphs = []
    for element in data:
        paragraphs.extend(element['content'])
    return paragraphs

def write_paragraph_df_to_txt(df, path, filename):
    '''
    Function to write paragraphs from dataframe to txt file
    '''
    with open (path + '/' +filename, 'w', encoding='utf-8') as f:
        for row in df.itertuples(index=False):
            if row.paragraphs is not None:
                if type(row.paragraphs[0]) == str and len(row.paragraphs) == 1:
                    f.write(row.DOI +': '+ row.paragraphs[0] +'\n')
                elif type(row.paragraphs[0]) == str and len(row.paragraphs) != 1:
                    for paragraph in row.paragraphs:
                        f.write(row.DOI +': '+ paragraph +'\n')
                elif type(row.paragraphs[0]) == dict:
                    paragraphs = dict_to_str(row.paragraphs)
                    for paragraph in paragraphs:
                        f.write(row.DOI +': '+ paragraph +'\n')

