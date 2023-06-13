import json
import multiprocessing as mp
import os
import extraction as ext

if __name__ == '__main__':
    path = '/home/ptoka/extracted_data'
    save_dir = '/home/ptoka/extracted_data'
    batch_no = list(range(1,2))
    for batch in batch_no:
        with open(os.path.join(path, f'mat_results_batch_{batch}.json'), 'r') as f:
            mat_results = json.load(f)
        num_cpus = 10
        pool = mp.Pool(processes=num_cpus)
        results = pool.map(ext.extract_materials_amounts_batch, mat_results)
        pool.close()
        pool.join()
        with open(os.path.join(save_dir, f'amounts_batch_{batch}.json'), 'w') as f:
            json.dump(results, f, indent=4,sort_keys=True,ensure_ascii=False)

