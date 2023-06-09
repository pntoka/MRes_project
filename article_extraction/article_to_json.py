'''
Script to get text of article from html or xml file into json file
'''
import to_json
# import doi_tools
import os
import sys

if __name__ == '__main__':
    batch_numbers = list(range(1, 3))
    for number in batch_numbers:
        original_stdout = sys.stdout
        output_file = open('/home/ptoka/article_json/output_' + str(number) + '.txt', 'w')
        sys.stdout = output_file
        path = '/home/ptoka/scrape/batch_no_' + str(number)
        filenames = os.listdir(path)
        if not os.path.exists('/home/ptoka/article_json/batch_no_' + str(number) + '_json'):
            os.mkdir('/home/ptoka/article_json/batch_no_' + str(number) + '_json')
        save_dir = '/home/ptoka/article_json/batch_no_' + str(number) + '_json'
        for filename in filenames:
            to_json.article_extractor(filename, path, save_dir)
        output_file.close()
        sys.stdout = original_stdout
    
