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
    output jsonl file format: {doi:doi, text:paragraph, label:''}
    '''
    with open(file_path, 'r', encoding='utf-8') as f:
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

class AnnotateConverter:
    def __init__(self, path):
        self.path = path


    def read_jsonl(self, file):  
        '''
        Function to read in jsonl file
        '''
        data = []
        with jsonlines.open(os.path.join(self.path,file), 'r') as f:
            for line in f:
                data.append(line)
        return data
    
    def doi_fixer(self, doi):
        return doi.replace(r'\\', '',1)
    
    def extract_pre_tar_mat(self, para_data):
        precursors = []
        targets = []
        materials = []
        for label in para_data['entities']:
            if label['label'] == 'precursor':
                precursors.append(para_data['text'][label['start_offset']:label['end_offset']])
            elif label['label'] == 'material':
                materials.append(para_data['text'][label['start_offset']:label['end_offset']])
            elif label['label'] == 'target':
                targets.append(para_data['text'][label['start_offset']:label['end_offset']])
        materials.extend(precursors)
        materials.extend(targets)
        return list(set(precursors)), list(set(targets)), list(set(materials))
    
    def extract_time_temp(self, para_data):
        time = []
        temp = []
        for label in para_data['entities']:
            if label['label'] == 'rxn time':
                time.append(para_data['text'][label['start_offset']:label['end_offset']])
            elif label['label'] == 'rxn temp':
                temp.append(para_data['text'][label['start_offset']:label['end_offset']])
        return list(set(time)), list(set(temp))
    
    def temp_converter(self, temp):
        all_temp = {}
        for t in temp:
            temp_dict = {}
            temp_dict['values'] = [round(int(t.split(' ')[0]),1)]
            temp_dict['units'] = t.split(' ')[1]
            all_temp.update(temp_dict)
        return all_temp
    
    def time_converter(self, time):
        all_time = {}
        if len(time) > 1:
            all_time = []
            for t in time:
                time_dict = {}
                try:
                    time_dict['values'] = round(int(t.split(' ')[0]),1)
                    time_dict['units'] = t.split(' ')[1]
                except (ValueError, IndexError):
                    time_dict['values'] = round(int(t),1)
                    time_dict['units'] = ''
                all_time.append(time_dict)
            all_time_dict = {'values':[t['values'] for t in all_time], 'units':all_time[0]['units']}
            return all_time_dict
        for t in time:
            time_dict = {}
            try:
                time_dict['values'] = [round(int(t.split(' ')[0]),1)]
                time_dict['units'] = t.split(' ')[1]
            except (ValueError, IndexError):
                time_dict['values'] = [round(int(t),1)]
                time_dict['units'] = ''
            all_time.update(time_dict)
        return all_time
    
    def extract_amounts(self, para_data):
        mat_amount = []
        for relation in para_data['relations']:
            for label in para_data['entities']:
                if label['id'] == relation['to_id']:
                    mat = para_data['text'][label['start_offset']:label['end_offset']]
                elif label['id'] == relation['from_id']:
                    amount = para_data['text'][label['start_offset']:label['end_offset']]
            mat_amount.append([mat, amount])
        return (mat_amount)
    
    def mat_amount_compile(self, mat_amount, materials):
        all_materials = []    #change this to dict
        for material in materials:
            for mat in mat_amount:
                if material == mat[0]:
                    all_materials.append({mat[0]:mat[1].split(' ')}) 
        for material in materials:
            if material not in [mat[0] for mat in mat_amount]:
                all_materials.append({material:''})
        return all_materials
    
    def pre_tar_compile(self, precursors, targets, all_materials):
        precursors_dict = []
        targets_dict = []
        for precursor in precursors:
            for material in all_materials:
                if precursor == list(material.keys())[0]:
                    precursors_dict.append(material)
        for target in targets:
            for material in all_materials:
                if target == list(material.keys())[0]:
                    targets_dict.append(material)
        return precursors_dict, targets_dict
    
    def compile(self, temp, time, precursors_dict, targets_dict, all_materials, para_data):
        data = {}
        data['all_materials'] = all_materials
        data['precursors'] = precursors_dict
        data['targets'] = targets_dict
        data['temp_values'] = temp
        data['time_values'] = time
        data['doi'] = self.doi_fixer(para_data['doi'])
        data['text'] = para_data['text'][:50]
        return data
    
    def data_compiler(self,file):
        data = []
        for para_data in self.read_jsonl(file):
            precursors, targets, materials = self.extract_pre_tar_mat(para_data)
            time, temp = self.extract_time_temp(para_data)
            all_materials = self.mat_amount_compile(self.extract_amounts(para_data), materials)
            precursors_dict, targets_dict = self.pre_tar_compile(precursors, targets, all_materials)
            data.append(self.compile(self.temp_converter(temp), self.time_converter(time), precursors_dict, targets_dict, all_materials, para_data))
        return data