"""
Script to retrieve full text of articles in html or xml format from 
DOI using Crossref API with webscraping and using Elsevier API
"""

import sys
import os
import requests
from crossref.restful import Works, Journals
import re
import urllib.request
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

class FullTextDownloader:
    def __init__(self, pub_prefix,api_key):
        self.pub_prefix = pub_prefix
        self.api_key = api_key
    
    def crossref_link(self, doi):
        opener = opener = urllib.request.build_opener()
        opener.addheaders = [('Accept', 'application/vnd.crossref.unixsd+xml')]
        r=opener.open('http://dx.doi.org/'+doi)
        links = re.findall(r"(?<=\<).+?(?=\>)",r.info()['Link']) #finds links that are between < and >
        return links
    
    def downloadElsevier(self, doi, save_dir):
        if not os.path.exists(save_dir):
            print(
                f"{save_dir} directory does not exists.\nCreating directory {save_dir}"
            )
            os.makedirs(save_dir)

        article_url = "https://api.elsevier.com/content/article/doi/" + doi
        article = requests.get(
            article_url,
            headers={
                "x-els-apikey": self.api_key,
                "Content-Type": "application/xml",
                },
        ).text
        if doi:
            with open(
                save_dir + "\\" + doi.replace("/", "-")+'.txt', "w+", encoding="utf-8"
            ) as save_file:
                save_file.write(article)
        else:
            print("Empty DOI!")

    def link_selector(self, doi, links):
        prefix = doi[:7]
        if prefix == self.pub_prefix['RSC']:
            link = re.sub('articlepdf','articlehtml',links[1])
            return link #html link
        elif prefix == self.pub_prefix['ACS']:
            link = re.sub('pdf/','',links[1])
            return link #html link
        elif prefix == self.pub_prefix['Wiley']:
            for link in links:
                if 'full-xml' in link:
                    return link #full text in xml
        elif prefix == self.pub_prefix['Frontiers']:
            return links[1] #full text html link
        elif prefix == self.pub_prefix['MDPI']:
            link = re.sub('/pdf','',links[1])
            return link #html link
        elif prefix == self.pub_prefix['Springer']:
            return links[2]  #full text html link but some may be just pdf
        elif prefix == self.pub_prefix['Nature']:
            return links[2]  #html link   
        elif prefix == self.pub_prefix['TandF']:
            link = re.sub('/pdf','',links[1])
            return link
        elif prefix == self.pub_prefix['Science']:
            print('URLs from Science get 403 error')
    
    def web_scrape(self,doi,link,save_dir):
        options = Options()
        options.binary_location = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
        driver = webdriver.Firefox(executable_path=r"C:\Users\Piotr\geckodriver.exe", options=options)
        driver.get(link)
        page = driver.page_source.encode('utf-8')
        # driver.close()
        with open(
            save_dir +'\\'+ doi.replace('/','-') +'.txt', 'wb'
            ) as save_file:
            save_file.write(page)
            save_file.close()
        driver.close()


if __name__ == '__main__':
    
    pub_prefix = {"RSC": "10.1039", "ACS": "10.1021", "Nature":"10.1038", "Science":"10.1126", "Frontiers":"10.3389", "MDPI":"10.3390", "Wiley": "10.1002", "Springer":"10.1007", "TandF":"10.1080", "Elsevier":"10.1016"}
    save_dir = r"C:\Users\Piotr\MRes_project\full_texts_test"
    my_api_key  = "4c35b0bb7a3b3dd148b4561345bdf7d9"
    downloader = FullTextDownloader(pub_prefix,my_api_key)
    with open(r"C:\Users\Piotr\MRes_project\DOIs_test\doi_2.txt",'r') as file:
        for line in file:
            if not line:
                break
            doi  = line.strip()
            if doi[:7] == pub_prefix["Elsevier"]:
                downloader.downloadElsevier(doi, save_dir)
            else:
                links = downloader.crossref_link(doi)
                link = downloader.link_selector(doi, links)
                downloader.web_scrape(doi,link,save_dir)
    # doi = "10.1002/chir.23509"
    # doi = "10.1002/bio.3803"
    # links = downloader.crossref_link(doi)
    # link = downloader.link_selector(doi, links)
    # downloader.web_scrape(doi, link, save_dir)


