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
    '''
    Extracts precursors and all materials from results of extract_materials and returns the unique entries.
    :param mat_results: results of extract_materials
    '''
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
        precursors_para.append(list(set(precursors)))
        all_materials_para.append(list(set(all_materials)))
    return precursors_para, all_materials_para

def amount_compiler(amounts, all_materials_para, precursors_para):
    '''
    Compiles the results of extract_materials_amounts into a single dictionary.
    :param amounts: results of extract_materials_amounts
    :param all_materials_para: all_materialst list from results of materials_extraction
    '''
    amount_dict = []
    precursors_dict = []
    for i, para in enumerate(amounts):
        para_dict = {}
        for sentence in para:
            if sentence != None:
                for material in all_materials_para[i]:
                    if material in sentence:
                        para_dict[material] = sentence[material]
        for material in all_materials_para[i]:
            if material not in para_dict:
                para_dict[material] = None
        amount_dict.append(para_dict)
    for i, para in enumerate(amount_dict):
        precursors = {}
        for precursor in precursors_para[i]:
            if precursor in para:
                precursors[precursor] = para[precursor]
        precursors_dict.append(precursors)

    return amount_dict, precursors_dict

def heating_operation_extraction(graphs):
    '''
    Extract information about heating operations from operation graphs.
    :param graphs: graph results of extract_operations
    '''
    heating_operations = []
    for i, para in enumerate(graphs):
        para_operations = []
        for sentence in para:
            if sentence:
                for operation in sentence:
                    operations = {}
                    if operation['op_type'] == 'HeatingOperation':
                        operations['subject'] = operation['subject']
                        if operation['temp_values']:
                            operations['temp_values'] = dict(
                                max = operation['temp_values'][0]['max'], min = operation['temp_values'][0]['min'],
                                units = operation['temp_values'][0]['units'], values = operation['temp_values'][0]['values'])
                        if not operation['temp_values']:
                            operations['temp_values'] = dict(max = None, min = None, units = None, values = None)
                        if operation['time_values']:
                            operations['time_values'] = dict(max = operation['time_values'][0]['max'], min = operation['time_values'][0]['min'],
                                units = operation['time_values'][0]['units'], values = operation['time_values'][0]['values'])
                        if not operation['time_values']:
                            operations['time_values'] = dict(max = None, min = None, units = None, values = None)
                        para_operations.append(operations)
        heating_operations.append(para_operations)
    return heating_operations


def data_compilation(dois, paras, amount_dict, precursors_dict, heating_operations):
    '''
    Compiles the results of materials_extraction, amount_compiler, and heating_operation_extraction into a single dictionary.
    :param dois: list of dois
    :param paras: list of paragraphs
    :param amount_dict: all_materials results of amount_compiler
    :param precursors_dict: precursor results of amount_compiler
    :param heating_operations: results of heating_operation_extraction
    '''
    data = []
    for i, para in enumerate(paras):
        para_dict = {}
        para_dict['doi'] = dois[i]
        para_dict['paragraph'] = para[:50], '...', para[-50:]
        para_dict['all_materials'] = amount_dict[i]
        para_dict['precursors'] = precursors_dict[i]
        para_dict['heating_operations'] = heating_operations[i]
        data.append(para_dict)
    return data