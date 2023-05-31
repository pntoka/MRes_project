import os
from token_classifier_fastext import TokenClassifier
import json

if __name__ == '__main__':
    tc = TokenClassifier()
    tc.load()
    path = '/home/ptoka/MRes_project/data_extraction/olivetti_extract'
    with open(os.path.join(path,'para_10_sample_tokenized.json'), 'r') as f:
        all_paras = json.load(f)
    
    all_predictions = []
    for para in all_paras:
        para_predictions = tc.predict_many(para)
        all_predictions.append(para_predictions)

    with open('predictions_10_sample.json', 'w') as f:
        json.dump(all_predictions, f, indent=4,sort_keys=True,ensure_ascii=False)
    