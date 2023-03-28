'''
Script to download full text articles from a list of DOIs
'''
import web_scraper

if __name__ == '__main__':
    save_dir = "/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/html tests/"
    file_path = "/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/html tests/iop_dois_copy.txt"
    my_api_key  = "" #insert your own API key
    web_scraper.text_downloader(file_path, save_dir, my_api_key)
