import os
import pidentifier as ptools
from synthesis_classifier import get_model, get_tokenizer, run_batch
import torch
model = get_model()
tokenizer = get_tokenizer()

def classify_paragraphs(path, file, batch_size, save_file='results.txt'):
    '''
    Function that reads file with paragraphs and classifies them using MatBERT synthesis classifier
    model from the Ceder group. Results are saved in file from same folder as input file as results.txt
    
    :param path: path to file with paragraphs
    :param file: filename with paragraphs
    :param batch_size: batch size for classification
    '''
    with open(os.path.join(path, file), 'r') as f:
        paragraphs = list(map(str.strip, f))
    
    batches = ptools.make_batches(paragraphs, batch_size)

    results_all = []
    for batch in batches:
        result = run_batch(batch, model, tokenizer)
        for res in result:
            result_dict = {}
            result_dict['DOI'] = res['text'].split(':',1)[0]
            result_dict['text'] = res['text'].split(':',1)[1][:75]
            result_dict['result'] = max(res['scores'].items(), key=lambda x: x[1])
            results_all.append(result_dict)

    with open(os.path.join(path, save_file), 'w') as f:
        for result in results_all:
            f.write(str(result) + '\n')
