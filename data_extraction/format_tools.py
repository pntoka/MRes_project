import json
import os
import jsonlines

def txt_to_json(file_path, save_dir):
    '''
    Function to convert txt file to json file
    txt file format: doi:paragraph on each line
    output json file format: {doi:doi, text:paragraph}
    '''
    with open(file_path, 'r') as f:
        paras = []
        dois = []
        for line in f:
            paras.append(line.split(':',1)[1].strip())
            dois.append(line.split(':',1)[0])
    data = []
    for i in range(len(dois)):
        data.append({'doi':dois[i], 'text':paras[i], 'label':''})
    with open(save_dir, 'w') as f:
        json.dump(data, f, indent=4,sort_keys=True,ensure_ascii=False)
    
def txt_to_jsonl(file_path, save_dir):
    '''
    Function to convert txt file to jsonl file
    txt file format: doi:paragraph on each line
    output jsonl file format: {doi:doi, text:paragraph}
    '''
    with open(file_path, 'r') as f:
        paras = []
        dois = []
        for line in f:
            paras.append(line.split(':',1)[1].strip())
            dois.append(line.split(':',1)[0])
    data = []
    for i in range(len(dois)):
        data.append({'doi':dois[i], 'text':paras[i], 'label':''})
    with open(save_dir, 'w') as f:
        for item in data:
            f.write(json.dumps(item)+'\n')
    
def toks_pred_jsonl(toks, preds, jsonl,  save_dir):
    '''
    Function to convert predictions to jsonl file
    Toks: list of tokenized paragraphs from mat entity recognition
    Preds: list of predictions from olivetti token classifier
    output jsonl file format: {doi:doi, text:paragraph, label:label}
    '''
    with open(toks, 'r') as f:
        toks = json.load(f)
    with open(preds, 'r') as f:
        preds = json.load(f)
    
    all_para = []
    for i, para in enumerate(toks):
        para_labels = []
        for j, sent in enumerate(para):
            for k, label in enumerate(preds[i][j]):
                if label != 'null':
                    para_labels.append([sent['tokens'][k]['start'], sent['tokens'][k]['end'], label])
        all_para.append(para_labels)

    paras = []
    with jsonlines.open(jsonl, 'r') as f:
        for i, line in enumerate(f):
            line['label'] = all_para[i]
            paras.append(line)

    with open(save_dir, 'w') as f:
        for item in paras:
            f.write(json.dumps(item)+'\n')

        

    