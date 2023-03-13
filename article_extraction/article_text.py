'''
Script to get text of article from html or xml file into json file
'''
import article_to_json
import doi_tools

if __name__ == '__main__':
    save_dir = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests_json/'
    path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests/'
    dois_file = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/doi_tests/doi_test_acs.txt'
    dois = doi_tools.doi_list(dois_file)
    filenames = doi_tools.doi_to_filename(dois)
    for filename in filenames:
        article_to_json.article_extractor(filename, path, save_dir)