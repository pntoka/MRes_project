'''
Package containing helper functions for article extraction such as removing tags and creating json files
'''

import json

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
    Function to find paragraphs in a soup object based on specific tags with the same name
    '''
    paragraphs = soup.find_all(**tags_list)
    return paragraphs

def find_paragraphs_list(soup, tags_list):
    '''
    Function to find paragraphs in a soup object based on a list of tags with different names
    '''
    paragraphs = []
    for tag in tags_list:
        paragraphs += soup.find_all(**tag)
    return paragraphs

def create_json_data(doi, sections, title, save_dir, keywords = None):
    '''
    Function to create json file of html/xml article
    '''
    data = {}
    data['DOI'] = doi.replace(doi[7],'/',1).replace('.txt','')
    data['Journal']= ""
    if keywords ==  None:
        data['Keywords'] = []
    elif keywords != None:
        data['Keywords'] = keywords
    data['Title'] = title
    data['Sections']= sections
    doi = doi.replace('.txt','.json')
    with open(save_dir+doi, 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys = True, indent=4, ensure_ascii=False)
