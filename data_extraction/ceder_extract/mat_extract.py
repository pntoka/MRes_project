import json
import os
import extraction as ext

if __name__ == '__main__':
    path = '/home/ptoka/para_dataset'
    save_dir = '/home/ptoka/extracted_data'
    batch_no = list(range(14,29))
    mat_model = ext.mat_model()
    for batch in batch_no:
        file_name =f'batch_{batch}_pdata.txt'
        paras, dois = ext.paragraph_reader(file_name, path)
        mat_results = ext.model_mat_recognize(paras,mat_model)
        with open(os.path.join(save_dir, f'mat_results_batch_{batch}.json'), 'w') as f:
            json.dump(mat_results, f, indent=4,sort_keys=True,ensure_ascii=False)