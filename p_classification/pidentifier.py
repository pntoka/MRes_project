import re
import os
import json
import pandas as pd
import numpy as np


def get_data(path):
    '''
    Function to get data from json files
    '''
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


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
    keywords = ['experimental', 'experimentation', 'materials and methods', 'methodology', 'methods','procedure','synthesis', 'hydrothermal', 'method']
    for section in section_names:
        if any(keyword.lower() in section.lower() for keyword in keywords):
            section_name = section
            return section_name


def subsection_selector(subsection_names):
    '''
    Function to select subsection containing synthesis methods based on keyword matching
    '''
    keywords = ['synthesis', 'hydrothermal', 'preparation', 'methods', 'experimental']
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
        return subsection_content
    elif content_checker(data, section_name) == False:
        section_content = get_section_content(data, section_name)
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
