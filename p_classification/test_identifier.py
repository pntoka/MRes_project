import pidentifier as pid
import os

if __name__ == '__main__':
    path = r'C:\Users\Piotr\OneDrive - Imperial College London\MRes_project_data\full_text_tests_json'
    # file = '10.1021-acsomega.0c03290.json'
    file = '10.1016-j.jphotochem.2019.112201.json'
    data = pid.get_data(os.path.join(path, file))
    section_names = pid.get_section_names(data)
    name = pid.section_selector_2(section_names)
    # print(name)
    sub_names = pid.get_subsection_names(data, name)
    print(sub_names)
    sub_name = pid.subsection_selector_2(sub_names)
    print(sub_name)
    for element in data['Sections']:
        if element['name'] == name:
            test = element
    # content = pid.extract_text_content_2(test)
    # print(content)
    # print(test.values()[0])
    # print(len(test.values()))
    # text_content = []
    # content = pid.extract_content(test)
    # print(len(content))
    # for element in content:
    #     print(element[:100])