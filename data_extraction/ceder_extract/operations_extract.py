import os
import json
import extraction as ext

if __name__ == '__main__':
    path = 'home/ptoka/extracted_data'
    save_dir = '/home/ptoka/extracted_data'
    batch_no = list(range(14,29))
    oe, gb = ext.oe_gb()
    for batch in batch_no:
        with open(os.path.join(save_dir, f'mat_results_batch_{batch}.json'), 'r') as f:
            mat_results = json.load(f)
        operations, graphs = ext.extract_operations_batch(mat_results, oe, gb)
        with open(os.path.join(save_dir, f'operations_batch_{batch}.json'), 'w') as f: 
            json.dump(operations, f, indent=4,sort_keys=True,ensure_ascii=False)
        with open(os.path.join(save_dir, f'graphs_batch_{batch}.json'), 'w') as f:
            json.dump(graphs, f, indent=4,sort_keys=True,ensure_ascii=False)