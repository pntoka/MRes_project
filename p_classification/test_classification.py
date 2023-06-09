import classification

if __name__ == '__main__':

    path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests_json'
    file = 'p_dataset_3.txt'
    classification.classify_paragraphs(path, file, 20, save_file='classification_results.txt')


