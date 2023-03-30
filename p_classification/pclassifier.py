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

def get_subsection_names(data):
    '''
    Function to get subsection names from json files
    '''
    subsection_names = []
    sections = data['Sections']
    for element in sections:
        subsections = element['subsections']
        for subelement in subsections:
            subsection_names.append(subelement['name'])
    return subsection_names