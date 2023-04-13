'''
Package containing functions to extract paragraphs from html and xml files and save as json files
for diffrerent publishers (RSC, Elsevier, ACS, Wiley, Springer, Nature, Frontiers, Taylor and Francis, MDPI)

'''

import extractor_tools as tools
import section_extractor
from LimeSoup import (ElsevierSoup, RSCSoup)
import json
from bs4 import BeautifulSoup

def ACS_to_json(soup, doi, save_dir):
    '''
    Function specific to ACS html journals to extract paragraphs and save as json file
    '''
    list_remove = [      
        {'name':'a'}, #remove links
        {'name':'span'}, #remove inline equations
    ]
    title = soup.find('span', class_='hlFld-Title').text
    sections = section_extractor.sections_acs(soup, list_remove)
    tools.create_json_data(doi,sections,title,save_dir)

def Wiley_to_json(soup, doi, save_dir):
    '''
    Function to extract paragraphs from Wiley xml journals and save as json file
    doi is the txt file name
    '''
    list_remove = [{'name': ['link', 'tabular', 'figure']}] #removes links and tables
    titles = soup.header.find_all('titleGroup')
    title = titles[-1].find('title').text
    keywords = soup.header.find_all('keywordGroup')
    keywords = [keyword.text for keyword in keywords[0].find_all('keyword')]
    sections = section_extractor.sections_wiley(soup, list_remove)
    tools.create_json_data(doi, sections, title, save_dir, keywords=keywords)

def Wiley_html_to_json(soup, doi, save_dir):
    '''
    Function to extract paragraphs from Wiley html journals and save as json file
    doi is the txt file name
    '''
    list_remove = [{'name': 'section', 'class': 'article-section__inline-figure'},
               {'name': 'div', 'class': 'article-table-content'},
               {'name': 'div', 'class': 'inline-equation'},
               {'name': 'span'}, {'name': 'a'}]        #removes links, tables, figures, inline equations
    title = soup.find('h1').text
    sections = section_extractor.sections_wiley_html(soup, list_remove)
    tools.create_json_data(doi, sections, title, save_dir)

def Springer_Nature_to_json(soup, doi, save_dir):
    '''
    Function to extract paragraphs from Springer or Nature html journals and save as json file
    '''
    list_remove = [{'name':'figure'}] #removes figures
    sections = section_extractor.sections_springer_nature(soup, list_remove)
    title = soup.find('h1', class_ = 'c-article-title').text
    tools.create_json_data(doi, sections, title, save_dir)

def Frontiers_to_json(soup, doi, save_dir):
    '''
    Function to extract paragraphs from Frontiers html journals and save as json file
    '''
    list_remove = [{'name':'div'}] #removes figures
    title = soup.find('h1').text
    sections = section_extractor.sections_frontiers(soup, list_remove)
    tools.create_json_data(doi, sections, title, save_dir)

def TandF_to_json(soup, doi, save_dir):
    '''
    Function to extract paragraphs from Taylor and Francis html journals and save as json file
    '''
    list_remove = [{'name': 'div', 'class':'figure figureViewer'},
                {'name': 'div', 'class':'tableView'},
                {'name': 'div', 'class':'hidden rs_skip'},
            {'name':'span'}
            ]
    sections = section_extractor.sections_tandf(soup, list_remove)
    title = soup.find('span', class_ = 'NLM_article-title hlFld-title').text
    tools.create_json_data(doi, sections, title, save_dir)
    
def MDPI_to_json(soup, doi, save_dir):
    '''
    Function to extract paragraphs from MDPI html journals and save as json file
    '''
    list_remove = [{'name': 'div'}]
    sections = section_extractor.sections_mdpi(soup, list_remove)
    title = soup.find('h1').text
    tools.create_json_data(doi, sections, title, save_dir)
    
def RSC_to_json(path, doi, save_dir):
    '''
    Function to extract paragraphs from RSC html journals using LimeSoup parser and save as json file
    '''
    with open(path+doi, 'r', encoding='utf-8') as f:
        html_str = f.read()
    data = RSCSoup.parse(html_str)
    with open(save_dir+doi.replace('.txt', '.json'), 'w', encoding='utf-8') as f:
        json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

def Elsevier_to_json(path, doi, save_dir):
    '''
    Function to extract paragraphs from Elsevier xml journals using LimeSoup parser and save as json file
    '''
    with open(path+doi, 'r', encoding='utf-8') as f:
        xml_str = f.read()
    doc = BeautifulSoup(xml_str, 'xml')
    if len(doc.find_all('rawtext')) == 0:
        data = ElsevierSoup.parse(xml_str)
        with open(save_dir+doi.replace('.txt', '.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

def article_extractor(doi, path, save_dir):
    '''
    Function to extract paragraphs from given html/xml file and save as json file based on publisher
    '''
    pub_prefix = {"RSC": "10.1039", "ACS": "10.1021", "Nature":"10.1038", "Science":"10.1126", "Frontiers":"10.3389", "MDPI":"10.3390", "Wiley": "10.1002", "Springer":"10.1007", "TandF":"10.1080", "Elsevier":"10.1016"}
    prefix = doi[:7]

    with open(path+doi, 'r', encoding='utf-8') as f:
        html_xml_str = f.read()
    soup = BeautifulSoup(html_xml_str, 'html.parser')
    
    if prefix == pub_prefix['ACS']:
        ACS_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['Wiley']:
        if html_xml_str.startswith('<html class'):
            Wiley_html_to_json(soup, doi, save_dir)
        if html_xml_str.startswith('<component xmlns'):
            soup = BeautifulSoup(html_xml_str, 'xml')
            Wiley_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['Springer']:
        Springer_Nature_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['Nature']:
        Springer_Nature_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['Frontiers']:
        Frontiers_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['TandF']:
        TandF_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['MDPI']:
        MDPI_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['RSC']:
        RSC_to_json(path, doi, save_dir)
    elif prefix == pub_prefix['Elsevier']:
        Elsevier_to_json(path, doi, save_dir)
    else:
        print('Journal not recognised')