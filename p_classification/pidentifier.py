import re
import os
import json
import pandas as pd
import numpy as np
import unicodedata
import shutil
from tqdm import tqdm


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

def section_selector_2(section_names):
    '''
    Function to select section containing results and discussion based on keyword matching
    '''
    keywords = ['results', 'results and discussion', 'results & discussion', 'results and discussions', 'results & discussions', 'result']
    for section in section_names:
        if any(keyword.lower() in section.lower() for keyword in keywords):
            section_name = section
            return section_name

def subsection_selector(subsection_names):
    '''
    Function to select subsection containing synthesis methods based on keyword matching
    '''
    keywords = ['synthesis', 'synthes', 'hydrothermal', 'preparation', 'methods', 'experimental']
    names = []
    for subsection in subsection_names:
        if any(keyword.lower() in subsection.lower() for keyword in keywords):
            names.append(subsection)
    if len(names) == 1:
        subsection_name = names[0]
        return subsection_name
    elif len(names) > 1:
        keywords_2 = ['synthesis', 'synthes', 'hydrothermal', 'preparation']
        for name in names:
            if any(keyword.lower() in name.lower() for keyword in keywords_2):
                subsection_name = name
                return subsection_name
            
def subsection_selector_2(subsection_names):
    '''
    Function to select subsection of results containing QY info based on keyword matching
    '''
    keywords = ['QY', 'quantum yield', 'quantum yields', 'quantum efficiency']
    names = []
    for subsection in subsection_names:
        if any(keyword.lower() in subsection.lower() for keyword in keywords):
            names.append(subsection)
    if len(names) == 1:
        subsection_name = names[0]
        return subsection_name
    else:
        return None

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


def extract_content(data):
    '''
    Function that returns all paragraphs from a section containing subsections as a list
    '''
    text_content = []
    
    if isinstance(data,dict):
        if 'content' in data:
            content = data['content']
            if isinstance(content, list) and all(isinstance(item, str) for item in content):
                text_content.extend(content)
        if 'content' in data:
            for value in data['content']:
                result = extract_content(value)
                if result:
                    text_content.extend(result)
    elif isinstance(data, list):
        for item in data:
            result = extract_content(item)
            if result:
                text_content.extend(result)

    return text_content

def check_if_dict(element_list):
    for element in element_list:
        if type(element) == dict:
            return True
    return False

def extract_results(data):
    '''
    Function to extract results from json file
    '''
    section_names = get_section_names(data)
    section_name = section_selector_2(section_names)    # select section containing results
    if section_name is None:
        return None
    if content_checker(data, section_name) == True:   # check if section contains subsections
        subsection_names = get_subsection_names(data, section_name)
        subsection_name = subsection_selector_2(subsection_names)   # select subsection containing QY information
        if subsection_name is None:
            for element in data['Sections']:
                if element['name'] == section_name:
                    results = extract_content(element)
                    return results
        elif subsection_name is not None:
            for element in data['Sections']:
                if element['name'] == section_name:
                    for subelement in element['content']:
                        if subelement['name'] == subsection_name:
                            results = extract_content(subelement)
                            return results
    elif content_checker(data, section_name) == False:
        for element in data['Sections']:
            if element['name'] == section_name:
                results = extract_content(element)
                if type(element['content'][0]) == str and check_if_dict(element['content']) == True:
                    extra_content = []
                    for para in element['content']:
                        if type(para) == str:
                            extra_content.append(para)
                        if type(para) == dict:
                            break
                    extra_content.extend(results)
                    return extra_content
                return results
    

def get_results(path, dois):
    '''
    Function to extract results from json files given a path and doi list
    '''
    p_results = pd.DataFrame(columns=['DOI','paragraphs'])
    for doi in dois:
        doi = doi.replace(doi[7],'-',1)
        data = get_data(os.path.join(path, doi+'.json'))
        results = extract_results(data)
        doi_save = data['DOI']
        row = {'DOI': doi_save, 'paragraphs': results}
        new_df = pd.DataFrame([row])
        p_results = pd.concat([p_results, new_df], axis=0, ignore_index=True)
    return p_results
        
def select_QY_paragraphs(paragraphs_list):
    '''
    Function to select paragraphs containing QY information
    '''
    if paragraphs_list is None:
        return None
    QY_paragraphs = []
    for paragraph in paragraphs_list:
        if 'QY' in paragraph or 'quantum yield' in paragraph or 'quantum efficiency' in paragraph:
            QY_paragraphs.append(paragraph)
    return QY_paragraphs

def QY_paragraphs_df(p_results):
    '''
    Function to select paragraphs containing QY information from dataframe
    '''
    p_results['QY_paragraphs'] = p_results['paragraphs'].apply(select_QY_paragraphs)
    return p_results

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
            data = get_data(os.path.join(path, file))
            try:
                paragraphs = synthesis_methods(data)
            except(IndexError, TypeError):
                continue
            # paragraphs = synthesis_methods(data)
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

def write_paragraphs_df_to_txt(df, path, filename):
    '''
    Function to write paragraphs from dataframe to txt file with each line containing DOI and paragraph
    Multiple paragraphs from each DOI are split into separate lines with DOI+'no_'+count as DOI
    '''
    with open (os.path.join(path, filename), 'w', encoding='utf-8') as f:
        for row in df.itertuples(index=False):
            if row.paragraphs is not None:
                if type(row.paragraphs[0]) == str and len(row.paragraphs) == 1:
                    f.write(row.DOI +': '+ row.paragraphs[0].replace('\n', ' ') +'\n')
                elif type(row.paragraphs[0]) == str and len(row.paragraphs) != 1:
                    count = 0                                                   #adds counter for paragraphs with same DOI
                    for paragraph in row.paragraphs:
                        f.write(row.DOI+f'_no_{count}' +': '+ paragraph.replace('\n', ' ')  +'\n')
                        count += 1
                elif type(row.paragraphs[0]) == dict:
                    paragraphs = dict_to_str(row.paragraphs)
                    count = 0
                    for paragraph in paragraphs:
                        f.write(row.DOI+f'_no_{count}' +': '+ paragraph.replace('\n', ' ')  +'\n')
                        count += 1

def QY_df_to_txt(df, path, filename):
    ''''
    Function to write QY paragraphs from dataframe to txt file with each line containing DOI and paragraph
    Multiple paragraphs from each DOI are split into separate lines with DOI+'no_'+count as DOI
    '''
    with open (os.path.join(path, filename), 'w', encoding='utf-8') as f:
        for row in df.itertuples(index=False):
            if not row.QY_paragraphs:
                continue
            elif row.QY_paragraphs is not None:
                if type(row.QY_paragraphs[0]) == str and len(row.QY_paragraphs) == 1:
                    f.write(row.DOI +': '+ row.QY_paragraphs[0].replace('\n', ' ') +'\n')
                elif type(row.QY_paragraphs[0]) == str and len(row.QY_paragraphs) != 1:
                    count = 0                                                   #adds counter for paragraphs with same DOI
                    for paragraph in row.QY_paragraphs:
                        f.write(row.DOI+f'_no_{count}' +': '+ paragraph.replace('\n', ' ')  +'\n')
                        count += 1

def simple_df_to_txt(df, path, filename):
    '''
    Function to take dataframe with single pargraph per DOI and write it to txt file with each line containing DOI and paragraph
    '''
    with open (os.path.join(path, filename), 'w', encoding='utf-8') as f:
        for row in df.itertuples(index=False):
            f.write(row.DOI +': '+ row.paragraph.replace('\n', ' ') +'\n')

def paragraph_df_to_tuple(df):
    '''
    Function to convert dataframe with extracted sections from each DOI to list of tuples in format (DOI, paragraph)
    Multiple paragraphs from each DOI are split into separate tuples with DOI+'no_'+count as DOI
    '''
    tuples = []
    for row in df.itertuples(index=False):
        if row.paragraphs is not None:
            if type(row.paragraphs[0]) == str and len(row.paragraphs) == 1:
                tuples.append((row.DOI, row.paragraphs[0].replace('\n', ' ')))
            elif type(row.paragraphs[0]) == str and len(row.paragraphs) != 1:
                count = 0                                               #adds counter for paragraphs with same DOI
                for paragraph in row.paragraphs:
                    tuples.append((row.DOI+f'_no_{count}', paragraph.replace('\n', ' ')))
                    count += 1
            elif type(row.paragraphs[0]) == dict:
                paragraphs = dict_to_str(row.paragraphs)
                count = 0
                for paragraph in paragraphs:
                    tuples.append((row.DOI+f'_no_{count}', paragraph.replace('\n', ' ')))
                    count += 1
    return tuples

def txt_to_tuple(path, filename):
    '''
    Function to convert txt file to list of tuples in format (DOI, paragraph)
    '''
    tuples = []
    with open (os.path.join(path, filename), 'r', encoding='utf-8') as f:
        for line in f:
            doi = line.split(':',1)[0]
            paragraph = line.split(':',1)[1]
            tuples.append((doi, paragraph))
    return tuples

def make_batches(data,batch_size):
    '''
    Function to make batches of data for feeding into classification model
    '''
    batches = [data[i:min(i+batch_size,len(data))] 
               for i in range(0,len(data),batch_size)]
    return batches

def txt_to_csv(path, filename, filename2='p_dataset.csv'):
    '''
    Function to convert txt file containing DOI: paragraph on each line to csv file
    '''
    df = pd.DataFrame(columns=['DOI','paragraph', 'class'])
    with open(os.path.join(path, filename), 'r', encoding='utf-8') as f:
        for line in f:
            doi = line.split(':',1)[0]
            paragraph = line.split(':',1)[1]
            row = {'DOI': doi, 'paragraph': paragraph, 'class': None}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
    
    df.to_csv(os.path.join(path, filename2), index=False, encoding='utf-8')

def copy_files(source_dir, destination_dir):
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_path = os.path.join(root, file)
                destination_path = os.path.join(destination_dir, file)
                shutil.copy2(source_path, destination_path)