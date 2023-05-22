import json
from MaterialAmountExtractor import get_materials_amounts

if __name__ == '__main__':
    with open('results_10_sample.json', 'r') as f:
        results = json.load(f)
    
    paragraphs = []
    for i in range(len(results)):
        material_amounts = []
        for element in results[i]:
            sentence = element['sentence']
            materials = []
            for material in element['all_materials']:
                materials.append(material['text'])
            m_m = get_materials_amounts.GetMaterialsAmounts(sentence, materials)
            material_amounts.append(m_m.final_result())
        paragraphs.append(material_amounts)


    with open('material_amounts_10_sample.json', 'w') as f:
        json.dump(paragraphs, f, indent=4,sort_keys=True,ensure_ascii=False)
    # with open('material_amounts_10_sample.json', 'r') as f:
    #     results = json.load(f)
    # print(results[0][0])
    # print(results[0][0]==None)


    # materials_in_sentence = ["3-amino-4-chlorophenylboronic acid","3-aminobenzeneboronic acid", "water"]
    # sentence = str("3-amino-4-chlorophenylboronic acid (0.3428 g) and 3-aminobenzeneboronic acid (0.2739 g) was dissolved in 20 mL distilled water and sonicated for 2 min, respectively.")
    # m_m = get_materials_amounts.GetMaterialsAmounts(sentence, materials_in_sentence)
    # print(m_m.final_result())
