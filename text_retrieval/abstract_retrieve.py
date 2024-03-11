import web_scraper
import re
import os
import sys
import time

if __name__ == '__main__':
    save_dir = '/home/ptoka/abstracts/'
    my_api_key = ""
    downloader = web_scraper.FullTextDownloader(web_scraper.PUB_PREFIX, my_api_key)
    with open('/home/ptoka/extracted_dois.txt', 'r', encoding='utf-8') as file:
        dois = file.read().splitlines()
    pattern = r"_no_\d+$"
    completed_dois = []
    orginal_stdout = sys.stdout
    output_file = open('/home/ptoka/abstracts/output.txt', 'w')
    sys.stdout = output_file
    for doi in dois:
        if doi not in completed_dois:
            if re.search(pattern, doi):
                doi = doi.replace(re.search(pattern, doi).group(), '')
                downloader.abstract_downloader(doi, save_dir)
                completed_dois.append(doi)
            else:
                downloader.abstract_downloader(doi, save_dir)
                completed_dois.append(doi)
        time.sleep(0.5)
    output_file.close()
    sys.stdout = orginal_stdout
