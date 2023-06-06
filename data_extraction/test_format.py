import format_tools as ft
import os

if __name__ == '__main__':
    # file_path = '/home/ptoka/MRes_project/data_extraction/ceder_extract/para_10_sample.txt'
    # save_dir = '/home/ptoka/para_10_sample_pred_elmo.jsonl'
    # # ft.txt_to_jsonl(file_path, save_dir)
    # path = '/home/ptoka/'
    # preds = os.path.join(path, 'predictions_elmo_10_sample.json')
    # toks = os.path.join(path, 'mat_results_10_sample.json')
    # jsonl = os.path.join(path, 'para_10_sample.jsonl')
    # ft.toks_pred_jsonl(toks, preds, jsonl, save_dir)

    path = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/annotations'
    file = 'ceder_10_sample.jsonl'
    convert = ft.AnnotateConverter(path)
    data = convert.read_jsonl(file)
    # print(data[3])
    pre, tar, mat = convert.extract_pre_tar_mat(data[1])
    print(pre)
    print(tar)
    print(mat)
    time, temp  = convert.extract_time_temp(data[3])
    time = convert.time_converter(time)
    temp = convert.temp_converter(temp)
    mat_amount = convert.extract_amounts(data[1])
    all_materials = convert.mat_amount_compile(mat_amount, mat)
    pre_dict, tar_dict = convert.pre_tar_compile(pre, tar, all_materials)
    # print(mat_amount)
    # print(all_materials)
    # print(pre_dict)
    # print(tar_dict)
    print(convert.compile(temp, time, pre_dict, tar_dict, all_materials, data[0]))
    # print(convert.data_compiler(file))

    


