'''
Script to get text of article from html or xml file
'''
import os
import sys
import pandas as pd

from bs4 import BeautifulSoup

class ArticleExtractor():
    def __init__(self):
        pass

    def doi_to_filename(self, dois):
        filenames = []
        for doi in dois:
            filenames.append(doi.replace('/', '-')+'.txt')
        return filenames
    
    def doi_list(self, filename):
        dois = []
        for line in open(filename, 'r'):
            dois.append(line.strip())
        return dois

def RSC_content(data):
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



import LimeSoup