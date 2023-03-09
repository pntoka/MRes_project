'''
Script to get text of article from html or xml file into json file
'''
import os
import sys
# import pandas as pd
import json

from bs4 import BeautifulSoup
from LimeSoup import (ElsevierSoup, RSCSoup)


class ExtractorTools:
    def __init__(self):
        pass

    def remove_tags_soup_list(self, soup_list, rules):
        '''
        Function to remove tags from a list of soup objects
        '''
        for element in soup_list:
            for rule in rules:
                for tag in element.find_all(**rule):
                    tag.extract()
        return soup_list

    def remove_tags_soup(slef, soup, rules):
        '''
        Function to remove tags from a soup object
        '''
        for rule in rules:
            for tag in soup.find_all(**rule):
                tag.extract()
        return soup
    
    def find_paragraphs(self, soup, tags_list):
        '''
        Function to find paragraphs in a soup object based on specific tags
        '''
        paragraphs = soup.find_all(**tags_list)
        return paragraphs
    
    def create_json_data(self, doi, sections, title, save_dir):
        '''
        Function to create json file of html/xml article
        '''
        data = {}
        data['DOI'] = doi.replace(doi[7],'/',1).replace('.txt','')
        data['Journal']= ""
        data['Keywords'] = []
        data['Title'] = title
        data['Sections']= sections
        doi = doi.replace('.txt','.json')
        with open(save_dir+doi, 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys = True, indent=4, ensure_ascii=False)


class SectionExtractor:
    def __init__(self):
        self.tools = ExtractorTools()

    def list_to_content(self, list, list_remove):
        '''
        Function to extract paragraphs embedded between h3 headings (specific to Springer/Nature)
        '''
        data = []
        for element in list:
            if element.name == 'p':
                element_clean = self.tools.remove_tags_soup(element, list_remove)
                data.append(element_clean.text)
            elif element.name == 'h3':
                return data
        return data
    
    def list_to_content_frontiers(self, list):
        '''
        Function to extract paragraphs in between h3 and h2 headings (specific to Frontiers)
        '''
        data = []
        for element in list:
            if element.name == 'p':
                data.append(element.text)
            elif element.name == 'h3' or element.name == 'h2':
                return data
        return data
    
    def subheadings_content_frontiers(self, list):
        '''
        Function to extract h3 subheadings and paragraphs in between h2 hesadings (specific to Frontiers)
        '''
        data = []
        for i in range(len(list)):
            if list[i].name == 'h3':
                data_sub = {}
                data_sub['name'] = list[i].text
                data_sub['type'] = 'h3'
                data_sub['content'] = self.list_to_content_frontiers(list[i+1:])
                data.append(data_sub)
            elif list[i].name == 'h2':
                return data
        return data
    
    def sections_acs(self, soup, list_remove):
        paragraph_tags = {'name':'div', 'class':['NLM_p last','NLM_p']}
        main_content = soup.find('div', class_= 'article_content')
        sections = main_content.find_all('div', class_='NLM_sec NLM_sec_level_1')
        data_dict = []
        for section in sections:
            data = {}
            data['name'] = section.find('h2').text
            data['type'] = 'h2'
            data['content'] = []
            if section.find('div', class_ = 'NLM_sec NLM_sec_level_2') is not None:
                elements = section.find_all('div', class_ = 'NLM_sec NLM_sec_level_2')
                for element in elements:
                    data_sub = {}    
                    data_sub['name'] = element.find('h3').text
                    data_sub['type'] = 'h3'
                    data_sub['content'] = []
                    paragraphs = self.tools.find_paragraphs(element, paragraph_tags)
                    paragraphs = self.tools.remove_tags_soup_list(paragraphs, list_remove)
                    for paragraph in paragraphs:
                        data_sub['content'].append(paragraph.text)
                    data['content'].append(data_sub)
            else:
                paragraphs = self.tools.find_paragraphs(section, paragraph_tags)
                paragraphs = self.tools.remove_tags_soup_list(paragraphs, list_remove)
                for paragraph in paragraphs:
                    data['content'].append(paragraph.text)
            data_dict.append(data)
        return data_dict
    
    def sections_wiley(self, soup, list_remove):
        '''
        Function to get sections from Wiley xml journals
        '''
        clean_body = self.tools.remove_tags_soup(soup.body, list_remove)
        section_1 = clean_body.section                              
        sections_clean = section_1.find_next_siblings('section')    #gets all sections that are siblings of the first section (main sections)
        sections_clean.insert(0,section_1)
        data_dict = []
        for section in sections_clean:
            data = {}
            data['name'] = section.name
            data['type'] = section.find('title').text
            data['content'] = []
            if section.find('section') is not None:
                if section.find_all(['section','p'])[0].name == 'p':  #deals with paragraphs before subheadings
                    data_sub = {}
                    data_sub['name'] = section.find('title').text
                    data_sub['type'] = section.name
                    data_sub['content'] = [section.find('p').text]
                    for paragraph in section.p.find_next_siblings('p'):
                        data_sub['content'].append(paragraph.text)
                    data['content'].append(data_sub)
                sub_sections = section.find_all('section')
                for element in sub_sections:
                    data_sub = {}
                    data_sub['content'] = []                           #deals with subheadings and their paragraphs
                    data_sub['name'] = element.find('title').text
                    data_sub['type'] = element.name
                    paragraphs = self.tools.find_paragraphs(element, {'name':'p'})
                    for paragraph in paragraphs:
                        data_sub['content'].append(paragraph.text)
                    data['content'].append(data_sub)
            else:
                paragraphs = self.tools.find_paragraphs(section, {'name':'p'})
                for paragraph in paragraphs:
                    data['content'].append(paragraph.text)
            data_dict.append(data)
        return data_dict
    
    def sections_springer_nature(self, soup, list_remove):
        '''
        Function to get sections from Springer and Nature html journals
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
                section_clean = self.tools.remove_tags_soup(section, list_remove)
                elements = section_clean.find_all(['h3','p'])
                for i in range(len(elements)):
                    if elements[i].name == 'h3':
                        data_sub = {}
                        data_sub['name'] = elements[i].text
                        data_sub['type'] = 'h3'
                        data_sub['content'] = self.list_to_content(elements[i+1:], list_remove)
                        data['content'].append(data_sub)
            else:
                section_clean = self.tools.remove_tags_soup(section, list_remove)
                for paragraph in section_clean.find_all('p'):
                    paragraph_clean = self.tools.remove_tags_soup(paragraph, list_remove)
                    data['content'].append(paragraph_clean.text)
            data_dict.append(data)
        return data_dict

    def sections_frontiers(self, soup, list_remove):
        '''
        Function to extract sections from Frontiers html journals
        '''
        main_content = soup.find('div', class_='JournalFullText')
        main_content = self.tools.remove_tags_soup(main_content, list_remove)
        elements = main_content.find_all(['p','h2','h3'])
        data_dict = []
        for i in range(len(elements)):
            if elements[i].name == 'h2':
                data = {}
                data['name'] = elements[i].text
                data['type'] = 'h2'
                data['content'] = []
                if elements[i].next_sibling is not None:
                    if elements[i].next_sibling.name == 'p':
                        data['content'] = self.list_to_content_frontiers(elements[i+1:])
                if elements[i].next_sibling is not None:
                    if elements[i].next_sibling.name == 'h3':
                        data['content']= self.subheadings_content_frontiers(elements[i+1:])
                data_dict.append(data)
        return data_dict
    
    def sections_tandf(self, soup, list_remove):
        '''
        Function to extract sections from Taylor and Francis html journals
        '''
        main_content = soup.find('div', class_ = 'hlFld-Fulltext')
        sections = main_content.find_all('div', class_ = ['NLM_sec NLM_sec_level_1', 'NLM_sec NLM_sec-type_intro NLM_sec_level_1'])
        sections_clean = self.tools.remove_tags_soup_list(sections, list_remove)
        data_dict = []
        for section in sections_clean:
            data = {}
            data['name'] = section.find('h2').text
            data['type'] = 'h2'
            data['content'] = []
            if section.find('div', class_ = 'NLM_sec NLM_sec_level_2') is not None:
                elements = section.find_all('div', class_ = 'NLM_sec NLM_sec_level_2') 
                for element in elements:
                    data_sub = {}
                    data_sub['name'] = element.find('h3').text
                    data_sub['type'] = 'h3'
                    data_sub['content'] = []
                    paragraphs = self.tools.find_paragraphs(element, {'name':'p'})
                    # paragraphs = remove_tags_soup_list(paragraphs, {'name':'button'})
                    for paragraph in paragraphs:
                        data_sub['content'].append(paragraph.text)
                    data['content'].append(data_sub)
            else:
                paragraphs = self.tools.find_paragraphs(section, {'name':'p'})
                for paragraph in paragraphs:
                    data['content'].append(paragraph.text)
            data_dict.append(data)
        return data_dict
    
    def sections_mdpi(self, soup, list_remove):
        '''
        Function to extract sections from MDPI html journals
        '''
        main_content = soup.find('div', class_= 'html-body')
        section_1 = main_content.find('section')                #get main sections based on first section
        sections = section_1.find_next_siblings('section')
        sections.insert(0,section_1)
        data_dict = []
        for section in sections:
            data = {}
            data['name'] = section.find('h2').text
            data['type'] = 'h2'
            data['content'] = []
            if section.find('section') is not None:
                sub_sections_1 = section.find('section')
                sub_sections = sub_sections_1.find_next_siblings('section')
                sub_sections.insert(0,sub_sections_1)
                for sub_section in sub_sections:
                    data_sub = {}
                    data_sub['name'] = sub_section.find('h4').text
                    data_sub['type'] = 'h4'
                    data_sub['content'] = []
                    if sub_section.find('section') is not None:
                        sub_sub_sections = sub_section.find_all('section')
                        for sub_sub_section in sub_sub_sections:                #deal with sub-sub-sections
                            data_sub_sub = {}
                            data_sub_sub['name'] = sub_sub_section.find('h4').text
                            data_sub_sub['type'] = 'h4'
                            data_sub_sub['content'] = []
                            paragraphs = self.tools.find_paragraphs(sub_sub_section,{'name':'div', 'class':'html-p'})
                            paragraphs_clean = self.tools.remove_tags_soup_list(paragraphs, list_remove)
                            for paragraph in paragraphs_clean:
                                data_sub_sub['content'].append(paragraph.text)
                            data_sub['content'].append(data_sub_sub)
                    else:                                       
                        paragraphs = self.tools.find_paragraphs(sub_section,{'name':'div', 'class':'html-p'})  #deals with subsections without sub-sub-sections
                        paragraphs_clean = self.tools.remove_tags_soup_list(paragraphs, list_remove)
                        for paragraph in paragraphs_clean:
                            data_sub['content'].append(paragraph.text)
                    data['content'].append(data_sub)
            else:
                paragraphs = self.tools.find_paragraphs(section,{'name':'div', 'class':'html-p'})
                paragraphs_clean = self.tools.remove_tags_soup_list(paragraphs, list_remove)
                for paragraph in paragraphs_clean:
                    data['content'].append(paragraph.text)
            data_dict.append(data)
        return data_dict


class ArticleExtractor:
    def __init__(self):
        self.tools = ExtractorTools()
        self.section_extractor = SectionExtractor()

    def ACS_to_json(self, soup, doi, save_dir):
        '''
        Function specific to ACS html journals to extract paragraphs and save as json file
        '''
        list_remove = [      
            {'name':'a'}, #remove links
            {'name':'span'}, #remove inline equations
        ]
        title = soup.find('span', class_='hlFld-Title').text
        sections = self.section_extractor.sections_acs(soup, list_remove)
        self.tools.create_json_data(doi,sections,title,save_dir)

    def Wiley_to_json(self, soup, doi, save_dir):
        '''
        Function to extract paragraphs from Wiley xml journals and save as json file
        doi is the txt file name
        '''
        list_remove = [{'name': ['link', 'tabular', 'figure']}] #removes links and tables
        title = soup.header.find('articleTitle').text
        sections = self.section_extractor.sections_wiley(soup, list_remove)
        self.tools.create_json_data(doi, sections, title, save_dir)

    def Springer_Nature_to_json(self, soup, doi, save_dir):
        '''
        Function to extract paragraphs from Springer or Nature html journals and save as json file
        '''
        list_remove = [{'name':'figure'}] #removes figures
        sections = self.section_extractor.sections_springer_nature(soup, list_remove)
        title = soup.find('h1', class_ = 'c-article-title').text
        self.tools.create_json_data(doi, sections, title, save_dir)

    def Frontiers_to_json(self, soup, doi, save_dir):
        '''
        Function to extract paragraphs from Frontiers html journals and save as json file
        '''
        list_remove = [{'name':'a'}, {'name':'div'}] #removes links and figures
        title = soup.find('h1').text
        sections = self.section_extractor.sections_frontiers(soup, list_remove)
        self.tools.create_json_data(doi, sections, title, save_dir)

    def TandF_to_json(self, soup, doi, save_dir):
        '''
        Function to extract paragraphs from Taylor and Francis html journals and save as json file
        '''
        list_remove = [{'name': 'div', 'class':'figure figureViewer'},
                    {'name': 'div', 'class':'tableView'},
                    {'name': 'div', 'class':'hidden rs_skip'},
                {'name':'span'}
                ]
        sections = self.section_extractor.sections_tandf(soup, list_remove)
        title = soup.find('span', class_ = 'NLM_article-title hlFld-title').text
        self.tools.create_json_data(doi, sections, title, save_dir)
    
    def MDPI_to_json(self, soup, doi, save_dir):
        '''
        Function to extract paragraphs from MDPI html journals and save as json file
        '''
        list_remove = [{'name': 'div'}]
        sections = self.section_extractor.sections_mdpi(soup, list_remove)
        title = soup.find('h1').text
        self.tools.create_json_data(doi, sections, title, save_dir)
    
    def RSC_to_json(self, path, doi, save_dir):
        '''
        Function to extract paragraphs from RSC html journals using LimeSoup parser and save as json file
        '''
        with open(path+doi, 'r', encoding='utf-8') as f:
            html_str = f.read()
        data = RSCSoup.parse(html_str)
        with open(save_dir+doi.replace('.txt', '.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

    def Elsevier_to_json(self, path, doi, save_dir):
        '''
        Function to extract paragraphs from Elsevier xml journals using LimeSoup parser and save as json file
        '''
        with open(path+doi, 'r', encoding='utf-8') as f:
            xml_str = f.read()
        data = ElsevierSoup.parse(xml_str)
        with open(save_dir+doi.replace('.txt', '.json'), 'w', encoding='utf-8') as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

class DOItools():
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

def article_extractor(doi, path, save_dir):
    '''
    Function to extract paragraphs from html/xml files and save as json file
    '''
    pub_prefix = {"RSC": "10.1039", "ACS": "10.1021", "Nature":"10.1038", "Science":"10.1126", "Frontiers":"10.3389", "MDPI":"10.3390", "Wiley": "10.1002", "Springer":"10.1007", "TandF":"10.1080", "Elsevier":"10.1016"}
    prefix = doi[:7]

    with open(path+doi, 'r', encoding='utf-8') as f:
        html_xml_str = f.read()
    soup = BeautifulSoup(html_xml_str, 'html.parser')
    
    if prefix == pub_prefix['ACS']:
        ArticleExtractor().ACS_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['Wiley']:
        soup = BeautifulSoup(html_xml_str, 'xml')
        ArticleExtractor().Wiley_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['Springer']:
        ArticleExtractor().Springer_Nature_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['Nature']:
        ArticleExtractor().Springer_Nature_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['Frontiers']:
        ArticleExtractor().Frontiers_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['TandF']:
        ArticleExtractor().TandF_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['MDPI']:
        ArticleExtractor().MDPI_to_json(soup, doi, save_dir)
    elif prefix == pub_prefix['RSC']:
        ArticleExtractor().RSC_to_json(path, doi, save_dir)
    elif prefix == pub_prefix['Elsevier']:
        ArticleExtractor().Elsevier_to_json(path, doi, save_dir)
    else:
        print('Journal not recognised')


if __name__ == '__main__':
    save_dir = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests_json/'
    path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests/'
    dois_file = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/doi_test.txt'
    dois = DOItools().doi_list(dois_file)
    filenames = DOItools().doi_to_filename(dois)
    for filename in filenames:
        article_extractor(filename, path, save_dir)