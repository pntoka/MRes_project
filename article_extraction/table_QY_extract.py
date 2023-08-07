import table_extractor as te
import os

if __name__ == '__main__':
    path = '/home/ptoka'
    dois_file = 'rel_dois.txt'
    with open(os.path.join(path, dois_file), 'r', encoding='utf-8') as file:
        dois = file.read().splitlines()
    save_dir = '/home/ptoka/table_QY_extract.json'
    article_path = '/home/ptoka/rel_dois'
    te.extract_QY(dois, article_path, save_dir)