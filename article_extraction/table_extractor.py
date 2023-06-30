import os
from tabledataextractor import Table
from bs4 import BeautifulSoup

def get_file(doi, path):
    '''
    Function to get file from path
    '''
    doi = doi.replace(doi[7],'-',1) + '.txt'
    with open(os.path.join(path,doi), 'r', encoding='utf-8') as f:
        html_xml_str = f.read()
    return html_xml_str

def get_soup(doi, path):
    '''
    Function to get soup object from file
    '''
    html_xml_str = get_file(doi, path)
    if html_xml_str.startswith('<component xmlns') or html_xml_str.startswith('<full-text-retrieval-response xmlns'):
        soup = BeautifulSoup(html_xml_str, features='xml')
        return soup
    else:
        soup = BeautifulSoup(html_xml_str, features = 'lxml')
        return soup

def get_tables_RSC(soup):
    '''
    Function to get list of tables from RSC file
    '''
    for tag in soup.find_all('div', class_ = 'image_table'):
        tag.extract()
    tables = soup.find_all('table')
    return tables




