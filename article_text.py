'''
Script to get text of article from html or xml file
'''
import os
import sys
import pandas as pd
import json

from bs4 import BeautifulSoup

class ACSExtractor():
    def __init__(self):
        pass
    list_remove = [
    {'name':'a'}, #remove links
    {'name':'span'}, #remove inline equations
    ]
    paragraph_tags = {'name':'div', 'class':['NLM_p last','NLM_p']}




class ArticleExtractor():
    def __init__(self):
        pass

    def doi_to_filename(self, dois):
        '''
        Function to convert a list of dois to a list of filenames of the full text html/xml
        '''
        filenames = []
        for doi in dois:
            filenames.append(doi.replace('/', '-')+'.txt')
        return filenames
    
    def doi_list(self, filename):
        '''
        Function to read dois from a file and return a list of dois
        '''
        dois = []
        for line in open(filename, 'r'):
            dois.append(line.strip())
        return dois

def RSC_content(data):
    '''
    Function to extract paragraphs as a list from RSC json file
    '''
    content = []
    for element in range(len(data['Sections'])):
        if type(data['Sections'][element]['content'][0]) == str:
            for item in data['Sections'][element]['content']:
                content.append(item)
        elif type(data['Sections'][element]['content'][0]) == dict:
            for item in range(len(data['Sections'][element]['content'])):
                if type(data['Sections'][element]['content'][item]['content'][0]) == str:
                    for item2 in data['Sections'][element]['content'][item]['content']:
                        content.append(item2)
    return content

def create_json_data(doi,paragraphs,title):
    '''
    Function to create a json file with the extracted paragraphs
    '''
    data = {}
    data['DOI'] = doi.replace(doi[7],'/').replace('.txt','')
    data['Journal']= ""
    data['Keywords'] = []
    data['Title'] = title
    data['Sections'] = {'content':[]}
    for paragraph in paragraphs:
        data['Sections']['content'].append(paragraph.text)
    return data

def remove_tags_soup_list(soup_list, rules):
    '''
    Function to remove tags from a list of soup objects
    '''
    for element in soup_list:
        for rule in rules:
            for tag in element.find_all(**rule):
                tag.extract()
    return soup_list

def remove_tags_soup(soup, rules):
    '''
    Function to remove tags from a soup object
    '''
    for rule in rules:
        for tag in soup.find_all(**rule):
            tag.extract()
    return soup

def find_paragraphs(soup, tags_list):
    '''
    Function to find paragraphs in a soup object based on specific tags
    '''
    paragraphs = soup.find_all(**tags_list)
    return paragraphs

def ACS_to_json(soup, doi, save_dir):
    '''
    Function specific to ACS html journals to extract paragraphs and save as json file
    '''
    list_remove = [      
        {'name':'a'}, #remove links
        {'name':'span'}, #remove inline equations
    ]
    paragraph_tags = {'name':'div', 'class':['NLM_p last','NLM_p']}
    title = soup.find('h1', class_='article-title').text
    paragraphs = find_paragraphs(soup, paragraph_tags)
    paragraphs_clean = remove_tags_soup_list(paragraphs, list_remove)
    data = create_json_data(doi, paragraphs_clean, title)
    with open(save_dir+doi, 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys = True, indent=4, ensure_ascii=False)


def Wiley_to_json(soup, doi, save_dir):
    '''
    Function to extract paragraphs from Wiley xml journals and save as json file
    doi is the txt file name
    '''
    list_remove = [{'name': ['link', 'tabular']}] #removes links and tables
    paragraph_tags = {'name': 'p'} #all relevant paragraphs are in body
    title = soup.header.find('articleTitle').text
    clean_body = remove_tags_soup_list(soup.body, list_remove)
    paragraphs_clean = find_paragraphs(clean_body, paragraph_tags)
    data = create_json_data(doi, paragraphs_clean, title)
    with open(save_dir+doi, 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys = True, indent=4, ensure_ascii=False)

def list_to_content(list, list_remove):
    '''
    Function to extract paragraphs embedded between h3 headings (specific to Springer)
    '''
    data = []
    for element in list:
        if element.name == 'p':
            element_clean = remove_tags_soup(element, list_remove)
            data.append(element_clean.get_text(strip=True))
        elif element.name == 'h3':
            return data
    return data

def sections_springer(soup, list_remove):
    '''
    Function to get sections from Springer html journals
    '''
    main_content = soup.body.find_all('div', 'main-content')
    sections = main_content[0].find_all('section')
    data_dict = []
    for section in sections:
        data = {}
        data['name'] = section.find('h2').text
        data['type'] = 'h2'
        data['content'] = []
        if section.find('h3') is not None:
            section_clean = remove_tags_soup(section, list_remove)
            elements = section_clean.find_all(['h3','p'])
            for i in range(len(elements)):
                data_sub = {}
                if elements[i].name == 'h3':
                    data_sub['name'] = elements[i].text
                    data_sub['type'] = 'h3'
                    data_sub['content'] = list_to_content(elements[i+1:], list_remove)
                    data['content'].append(data_sub)
        else:
            section_clean = remove_tags_soup(section, list_remove)
            for paragraph in section_clean.find_all('p'):
                paragraph_clean = remove_tags_soup(paragraph, list_remove)
                data['content'].append(paragraph_clean.get_text(strip=True))
        data_dict.append(data)
    return data_dict


def Springer_to_json(soup, doi, save_dir):
    '''
    Function to extract paragraphs from Springer html journals and save as json file
    '''
    list_remove = [{'name':'figure'}] #removes figures
    sections = sections_springer(soup, list_remove)
    title = soup.find('h1', class_ = 'c-article-title').get_text(strip=True)
    data = {}
    data['DOI'] = doi.replace(doi[7],'/',1).replace('.txt','')
    data['Journal']= ""
    data['Keywords'] = []
    data['Title'] = title
    data['Sections']= sections
    with open(save_dir+doi, 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys = True, indent=4, ensure_ascii=False)



import LimeSoup