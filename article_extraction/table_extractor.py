import os
from tabledataextractor import Table
from bs4 import BeautifulSoup
import pandas as pd
import json
import re

def get_file(doi, path):
    '''
    Function to get file from path based on doi
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
    if tables == None:
        return None
    return tables

def get_tables_generic(soup):
    '''
    Function to get list of tables from file of ACS, Elsevier, Wiley
    '''
    tables = soup.find_all('table')
    if tables == None:
        return None
    return tables

def get_table_links_springer_nature(soup, doi):
    tables = soup.find_all('div', class_ = 'c-article-table')
    if tables == None:
        return None
    table_nums = [i for i in range(1, len(tables)+1)]
    table_links = []
    rest_of_doi = doi.split('/',1)[1]
    if doi.startswith('10.1007'):
        for num in table_nums:
            table_links.append('https://link.springer.com/article/10.1007/'+rest_of_doi+'/tables/'+str(num))
    elif doi.startswith('10.1038'):
        for num in table_nums:
            table_links.append('https://www.nature.com/articles/'+rest_of_doi+'/tables/'+str(num))
    return table_links

def table_filter_springer_nature(tables_link):
    qy_keywords = ['QY', 'Quantum Yield', 'qauntum yield', 'QY(%)']
    table_list = []
    for link in tables_link:
        table = Table(link)
        for keyword in qy_keywords:
            if keyword in table.col_header.ravel().tolist() or keyword in table.row_header.ravel().tolist():
                table_list.append(table)
                break
    return table_list

def get_tables_springer_nature(table_links):
    tables = []
    for link in table_links:
        try:
            table = Table(link)
            tables.append(table)
        except:
            continue
        
    return tables

def table_filter(tables):
    qy_keywords = ['QY', 'Quantum Yield', 'qauntum yield', 'QY(%)', 'QY (%)']
    table_list = []
    for element in tables:
        try:
            table = Table(element)
        except:
            continue

        for keyword in qy_keywords:
            if keyword in table.col_header.ravel().tolist() or keyword in table.row_header.ravel().tolist():
                table_list.append(table)
                break
    return table_list
    

def find_ref_col(df):
    ref_keywords = ['Reference','reference','ref', 'Ref', 'Ref.','REF']
    for col in df.columns:
        if any(keyword in col for keyword in ref_keywords):
            return col
    return None

def this_work_cell(df, ref_col):
    this_work_keywords = ['this work', 'This work', 'This Work', 'This study', 'This Study', 'this study']
    for cell in df[ref_col]:
        if any(keyword in cell for keyword in this_work_keywords):
            return cell

def find_QY_col(df):
    QY_keywords = ['QY', 'Quantum Yield', 'qauntum yield', 'QY(%)', 'QY (%)']
    for col in df.columns:
        if any(keyword in col for keyword in QY_keywords):
            return col
    return None

def data_extract(tables):
    QY_values = []
    for table in tables:
        df = table.to_pandas()
        ref_col = find_ref_col(df)
        QY_col = find_QY_col(df)
        if ref_col != None:
            this_work = this_work_cell(df, ref_col)
            if this_work != None:
                QY_values.extend(df.loc[df[ref_col] == this_work, QY_col].values)
        elif ref_col == None:
            try:
                QY_values.extend(df[QY_col].values)
            except:
                continue
    return QY_values

def get_tables(doi,path):
    soup = get_soup(doi, path)
    if doi.startswith('10.1039'):
        tables = get_tables_RSC(soup)
        if tables == None:
            return None
    elif doi.startswith('10.1007') or doi.startswith('10.1038'):
        tables_link = get_table_links_springer_nature(soup, doi)
        if tables_link != None:
            tables = get_tables_springer_nature(tables_link)
        else:
            return None
    else:
        tables = get_tables_generic(soup)
        if tables == None:
            return None
    return tables

def extract_QY(dois, path, save_dir):
    doi_QY_dict = []
    pattern =  r"_no_\d+$"
    for i, doi in enumerate(dois):
        print(f'{i+1}/{len(dois)}')
        doi_2 = doi
        if re.search(pattern, doi):
            doi = doi.replace(re.search(pattern, doi).group(), '')
        doi_dict = {}
        tables = get_tables(doi,path)
        if tables == None:
            doi_dict['DOI'] = doi_2
            doi_dict['QY'] = []
            doi_QY_dict.append(doi_dict)
            continue
        tables_filtered = table_filter(tables)
        if not tables_filtered:
            doi_dict['DOI'] = doi_2
            doi_dict['QY'] = []
            doi_QY_dict.append(doi_dict)
            continue
        QY_values = data_extract(tables_filtered)
        doi_dict['DOI'] = doi_2
        doi_dict['QY'] = QY_values
        doi_QY_dict.append(doi_dict)
    with open(save_dir, 'w') as f:
        json.dump(doi_QY_dict, f, indent=4, sort_keys=True, ensure_ascii=False)

        