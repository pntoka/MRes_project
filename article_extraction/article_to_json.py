'''
Script to get text of article from html or xml file into json file
'''
import to_json
import doi_tools
import os
import sys

if __name__ == '__main__':
    # save_dir = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests_json/'
    # path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests/'
    # dois_file = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/doi_tests/doi_test_nature.txt'
    # dois = doi_tools.doi_list(dois_file)
    # filenames = doi_tools.doi_to_filename(dois)

    original_stdout = sys.stdout
    output_file = open('/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/DOI_data/output_1.txt', 'w')
    sys.stdout = output_file
    path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/DOI_data/batch_no_1'
    filenames = os.listdir(path)
    save_dir = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/DOI_data/batch_no_1_json'
    log_dir = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/DOI_data/log_1.txt'

    for filename in filenames:
        to_json.article_extractor(filename, path, save_dir, log_dir)
    
    output_file.close()
    sys.stdout = original_stdout
    
    
    # doi = '10.1039/C8NJ02086H'
    # path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/html tests/'
    # save_dir = path
    # to_json.article_extractor('10.1080-00032719.2020.1759618.txt', path, save_dir)
    # save_dir = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/html tests/'
    # path = save_dir
    # path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests/'
    # dois_file = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/doi_tests/doi_test_springer.txt'
    # dois = doi_tools.doi_list(dois_file)
    # filenames = doi_tools.doi_to_filename(dois)
    # for filename in filenames:
    #     to_json.article_extractor(filename, path, save_dir)