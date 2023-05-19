from materials_entity_recognition import MatRecognition
from MaterialAmountExtractor import get_materials_amounts
from operations_extractor.operations_extractor import OperationsExtractor
from operations_extractor.build_graph import GraphBuilder
import os
import json

oe = OperationsExtractor()
gb = GraphBuilder()

def extract_materials(paras):
    '''
    Extracts materials from a list of paragraphs.
    :param paras: list of paragraphs
    '''
    model_new = MatRecognition()
    result = model_new.mat_recognize(paras)
    return result

def extract_materials_amounts(mat_results):
    '''
    Extracts materials and amounts from a list of paragraphs.
    :param mat_results: results of extract_materials
    '''
    paragraphs_amounts = []
    for i, result in enumerate(mat_results):
        material_amounts = []
        for element in mat_results[i]:
            sentence = element['sentence']
            materials = []
            for material in element['all_materials']:
                materials.append(material['text'])
            m_m = get_materials_amounts.GetMaterialsAmounts(sentence, materials)
            material_amounts.append(m_m.final_result())
        paragraphs_amounts.append(material_amounts)
    return paragraphs_amounts

def extract_operations(mat_results):
    '''
    Extracts operations and builds graphs from a list of paragraphs.
    :param mat_results: results of extract_materials
    '''
    operations = []
    graphs = []
    for result in mat_results:
        para_operations = []
        para_graphs = []
        for sentence in result:
            sent_toks = [tok['text'] for tok in sentence['tokens']]
            labels = oe.get_operations_labels(sent_toks)
            para_operations.append(dict(labels=labels, sentence=sentence['sentence']))
            graph = gb.build_graph(sent_toks,labels)
            para_graphs.append(graph)
        operations.append(para_operations)
        graphs.append(para_graphs)
    return operations, graphs

def paragraph_reader(filename, path):
    '''
    Reads paragraphs from a file.
    :param filename: name of file
    '''
    paras = []
    dois = []
    for line in open(os.path.join(filename, path), 'r'):
        paras.append(line.split(':',1)[1].strip())
        dois.append(line.split(':',1)[0])
    return paras, dois

def materials_extraction(mat_results):
    precursors_para = []
    all_materials_para = []
    for result in mat_results:
        precursors = []
        all_materials = []
        for sentence in result:
            for material in sentence['all_materials']:
                all_materials.append(material['text'])
            for material in sentence['precursors']:
                precursors.append(material['text'])
        precursors_para.append(precursors)
        all_materials_para.append(all_materials)
    return precursors_para, all_materials_para
        

def data_compilation(mat_results, graphs, paras, dois):
    '''
    Compiles the results of the extraction into a single dictionary.
    :param mat_results: results of extract_materials
    :param graphs: results of extract_operations
    :param paras: list of paragraphs
    :param dois: list of dois
    '''
    data = []
    for i, result in enumerate(mat_results):
        data_dict = dict(doi=dois[i], paragraphs=[])

