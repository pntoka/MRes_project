import classification

if __name__ == '__main__':
    batch_no = list(range(11,29))
    for batch in batch_no:
        path = '/home/ptoka/paras_id'
        file = f'batch_{batch}_paras.txt'
        save_file = f'batch_{batch}_classification_results.txt'
        classification.classify_paragraphs(path, file, 50, save_file=save_file)
    # path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/full_text_tests_json'
    # file = 'p_dataset_3.txt'
    # classification.classify_paragraphs(path, file, 20, save_file='classification_results.txt')