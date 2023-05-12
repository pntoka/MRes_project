import json
from pprint import pprint
from materials_entity_recognition import MatRecognition
from materials_entity_recognition import MatIdentification

if __name__ == '__main__':
    # with open('para_10_sample.txt', 'r') as f:
    #     paras = json.load(f)
    paras = []
    dois = []
    for line in open('para_10_sample.txt', 'r'):
        paras.append(line.split(':',1)[1].strip())
        dois.append(line.split(':',1)[0])
    
    model_new = MatRecognition()
    result = model_new.mat_recognize(paras)
    with open('results_10_sample.json', 'w') as f:
        json.dump(result, f, indent=4,sort_keys=True,ensure_ascii=False)
    with open('sample_dois.txt', 'w') as f:
        for doi in dois:
            f.write(doi + '\n')
    

