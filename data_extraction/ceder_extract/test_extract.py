import json
import os
from pprint import pprint
# from materials_entity_recognition import MatRecognition
# from materials_entity_recognition import MatIdentification
import extraction as ext

if __name__ == '__main__':

    # with open('para_10_sample.txt', 'r') as f:
    #     paras = json.load(f)
    # paras = []
    # dois = []
    # for line in open('para_10_sample.txt', 'r'):
    #     paras.append(line.split(':',1)[1].strip())
    #     dois.append(line.split(':',1)[0])
    
    # result = ext.extract_materials(paras)

    # current_path = os.getcwd()
    current_path_2 = '/home/ptoka/MRes_project/data_extraction/ceder_extract'
    paras, dois = ext.paragraph_reader('para_hits.txt', current_path_2)

    with open('mat_results_hits.json', 'r') as f:
        result = json.load(f)
    
    with open('amounts_hits.json', 'r') as f:
        amounts = json.load(f)

    with open('graphs_hits.json', 'r') as f:
        graphs = json.load(f)

        
    data = ext.data_extractor(dois, paras, result, amounts, graphs)

    with open('data_hits.json', 'w') as f:
        json.dump(data, f, indent=4,sort_keys=True,ensure_ascii=False)
    
    
    # heating_operations = ext.heating_operation_extraction(graphs)
    # print(len(heating_operations))
    # print(heating_operations)
   


    # print(len(precursors))
    # print(len(all_materials))
    # model_new = MatRecognition()
    # result = model_new.mat_recognize(paras)
    # print('complete')
    # with open('results_10_sample.json', 'w') as f:
    #     json.dump(result, f, indent=4,sort_keys=True,ensure_ascii=False)
    # with open('sample_dois.txt', 'w') as f:
    #     for doi in dois:
    #         f.write(doi + '\n')
    

