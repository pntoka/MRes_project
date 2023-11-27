import web_scraper

if __name__ == '__main__':
    # doi = '10.1007/s00604-017-2367-0'
    doi = '10.1007/s00216-015-9138-8'
    my_api_key = ""
    downloader = web_scraper.FullTextDownloader(web_scraper.PUB_PREFIX, my_api_key)
    links = downloader.crossref_link(doi)
    link = downloader.link_selector(doi, links)
    print(links)
