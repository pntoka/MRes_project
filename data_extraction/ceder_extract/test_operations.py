from chemdataextractor.doc import Paragraph
from operations_extractor.operations_extractor import OperationsExtractor
import operations_extractor.conditions_extraction as ce
from operations_extractor.build_graph import GraphBuilder
from operations_extractor.utils import make_spacy_tokens
from pprint import pprint
import json

oe = OperationsExtractor()
gb = GraphBuilder()
# sentence = 'The typical procedure for solvothermal CDs was: dissolve 0.50 g m 4-aminophenol in 20 mL H2O, sonicate the solution for 20 min, then heat for 20 h at 200 °C in a Teflon-lined autoclave.'
# sentence = 'The mixture was transferred into a 100 mL Teflon-lined stainless steel autoclave and the hydrothermal synthesis reaction  proceeded at 150 °C for 3 h.'
# sent_toks = [tok for sent in Paragraph(sentence).raw_tokens for tok in sent]
# print(sent_toks)
# spacy_toks = make_spacy_tokens(sentence)
# print(spacy_toks)
# op_labels = oe.get_operations_labels(sent_toks)
# print(op_labels)
# times = ce.get_times_toks(spacy_toks)
# print(times)
# temps = ce.get_temperatures_toks(sent_toks)
# print(temps)
# materials = ['4-aminophenol', 'H2O']
# graph = gb.build_graph(sent_toks,op_labels)
# pprint(graph)
# subsentence = graph[0]['subsent_text']
# print(subsentence)


with open('results_10_sample.json', 'r') as f:
    results = json.load(f)

paragraphs = []
for i in range(len(results)):
    sentences = []
    for element in results[i]:
        sentence = element['sentence']
        sentences.append(sentence)
    paragraphs.append(sentences)

operations = []
graphs = []
for para in paragraphs:
    para_list = []
    para_graphs = []
    for sentence in para:
        sent_toks = [tok for sent in Paragraph(sentence).raw_tokens for tok in sent]
        labels = oe.get_operations_labels(sent_toks)
        para_list.append(dict(labels=labels, sentence=sentence))
        graph = gb.build_graph(sent_toks,labels)
        para_graphs.append(graph)
    operations.append(para_list)
    graphs.append(para_graphs)

with open('operations_10_sample.json', 'w') as f:
    json.dump(operations, f, indent=4,sort_keys=True,ensure_ascii=False)

with open('graphs_10_sample.json', 'w') as f:
    json.dump(graphs, f, indent=4,sort_keys=True,ensure_ascii=False)



