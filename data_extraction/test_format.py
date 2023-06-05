import format_tools as ft
import os

if __name__ == '__main__':
    file_path = '/home/ptoka/MRes_project/data_extraction/ceder_extract/para_10_sample.txt'
    save_dir = '/home/ptoka/para_10_sample_pred_elmo.jsonl'
    # ft.txt_to_jsonl(file_path, save_dir)
    path = '/home/ptoka/'
    preds = os.path.join(path, 'predictions_elmo_10_sample.json')
    toks = os.path.join(path, 'mat_results_10_sample.json')
    jsonl = os.path.join(path, 'para_10_sample.jsonl')
    ft.toks_pred_jsonl(toks, preds, jsonl, save_dir)