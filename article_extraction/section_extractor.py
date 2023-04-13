'''
Package containing functions to extract sections from html/xml files from different publishers
'''

import extractor_tools as tools

def list_to_content_springer(list, list_remove):
    '''
    Function to extract paragraphs embedded between h3 headings (specific to Springer/Nature)
    '''
    data = []
    for element in list:
        if element.name == 'p':
            element_clean = tools.remove_tags_soup(element, list_remove)
            data.append(element_clean.text)
        elif element.name == 'h3':
            return data
    return data
    
def list_to_content_frontiers(list):
    '''
    Function to extract paragraphs in between h3 and h2 headings (specific to Frontiers)
    '''
    data = []
    for element in list:
        if element.name == 'p':
            data.append(element.text)
        elif element.name == 'h3' or element.name == 'h2':
            return data
    return data
    
def subheadings_content_frontiers(list):
    '''
    Function to extract h3 subheadings and paragraphs in between h2 hesadings (specific to Frontiers)
    '''
    data = []
    for i in range(len(list)):
        if list[i].name == 'h3':
            data_sub = {}
            data_sub['name'] = list[i].text
            data_sub['type'] = 'h3'
            data_sub['content'] = list_to_content_frontiers(list[i+1:])
            data.append(data_sub)
        elif list[i].name == 'h2':
            return data
    return data
    
def sections_acs(soup, list_remove):
    paragraph_tags = {'name':'div', 'class':['NLM_p last','NLM_p']}
    main_content = soup.find('div', class_= 'article_content')
    sections = main_content.find_all('div', class_='NLM_sec NLM_sec_level_1')
    data_dict = []
    for section in sections:
        data = {}
        data['name'] = section.find('h2').text
        data['type'] = 'h2'
        data['content'] = []
        if section.find('div', class_ = 'NLM_sec NLM_sec_level_2') is not None:
            elements = section.find_all('div', class_ = 'NLM_sec NLM_sec_level_2')
            for element in elements:
                data_sub = {}    
                data_sub['name'] = element.find('h3').text
                data_sub['type'] = 'h3'
                data_sub['content'] = []
                paragraphs = tools.find_paragraphs(element, paragraph_tags)
                paragraphs = tools.remove_tags_soup_list(paragraphs, list_remove)
                for paragraph in paragraphs:
                    data_sub['content'].append(paragraph.text)
                data['content'].append(data_sub)
        else:
            paragraphs = tools.find_paragraphs(section, paragraph_tags)
            paragraphs = tools.remove_tags_soup_list(paragraphs, list_remove)
            for paragraph in paragraphs:
                data['content'].append(paragraph.text)
        data_dict.append(data)
    return data_dict
    
def sections_wiley(soup, list_remove):
    '''
    Function to get sections from Wiley xml journals
    '''
    clean_body = tools.remove_tags_soup(soup.body, list_remove)
    section_1 = clean_body.section                              
    sections_clean = section_1.find_next_siblings('section')    #gets all sections that are siblings of the first section (main sections)
    sections_clean.insert(0,section_1)
    data_dict = []
    for section in sections_clean:
        data = {}
        data['name'] = section.find('title').text
        data['type'] = section.name
        data['content'] = []
        if section.find('section') is not None:
            if section.find_all(['section','p'])[0].name == 'p':  #deals with paragraphs before subheadings
                data_sub = {}
                data_sub['name'] = section.find('title').text
                data_sub['type'] = section.name
                data_sub['content'] = [section.find('p').text]
                for paragraph in section.p.find_next_siblings('p'):
                    data_sub['content'].append(paragraph.text)
                data['content'].append(data_sub)
            sub_sections = section.find_all('section')
            for element in sub_sections:
                data_sub = {}
                data_sub['content'] = []                           #deals with subheadings and their paragraphs
                data_sub['name'] = element.find('title').text
                data_sub['type'] = element.name
                paragraphs = tools.find_paragraphs(element, {'name':'p'})
                for paragraph in paragraphs:
                    data_sub['content'].append(paragraph.text)
                data['content'].append(data_sub)
        else:
            paragraphs = tools.find_paragraphs(section, {'name':'p'})
            for paragraph in paragraphs:
                data['content'].append(paragraph.text)
        data_dict.append(data)
    return data_dict

def sections_wiley_html(soup, list_remove):
    '''
    Function to get sections from Wiley html file
    '''
    paragraph_tags = [{'name': 'p'}, {'name': 'div', 'class' : 'paragraph-element'}]
    main_content = soup.find('section', 'article-section article-section__full')
    sections = main_content.find_all('section', 'article-section__content')
    data_dict = []
    for section in sections:
        data = {}
        data['name'] = section.find('h2').text
        data['type'] = 'h2'
        data['content'] = []
        if section.find('h3') is not None:
            section_clean = tools.remove_tags_soup(section, list_remove)
            elements = section_clean.find_all('section', 'article-section__sub-content')
            for element in elements:
                data_sub = {}
                data_sub['name'] = element.find('h3').text
                data_sub['type'] = 'h3'
                data_sub['content'] = []
                paragraphs = tools.find_paragraphs_list(element, paragraph_tags)
                for paragraph in paragraphs:
                    data_sub['content'].append(paragraph.text)
                data['content'].append(data_sub)
        else:
            section_clean = tools.remove_tags_soup(section, list_remove)
            paragraphs = tools.find_paragraphs_list(section_clean, paragraph_tags)
            for paragraph in paragraphs:
                data['content'].append(paragraph.text)
        data_dict.append(data)
    return data_dict

def sections_springer_nature(soup, list_remove):
    '''
    Function to get sections from Springer and Nature html journals
    '''
    main_content = soup.body.find_all('div', 'main-content')
    sections = main_content[0].find_all('section')
    data_dict = []
    for section in sections:
        data = {}
        data['name'] = section.find('h2').text
        data['type'] = 'h2'
        data['content'] = []
        if section.find('h3') is not None:
            section_clean = tools.remove_tags_soup(section, list_remove)
            elements = section_clean.find_all(['h3','p'])
            for i in range(len(elements)):
                if elements[i].name == 'h3':
                    data_sub = {}
                    data_sub['name'] = elements[i].text
                    data_sub['type'] = 'h3'
                    data_sub['content'] = list_to_content_springer(elements[i+1:], list_remove)
                    data['content'].append(data_sub)
        else:
            section_clean = tools.remove_tags_soup(section, list_remove)
            for paragraph in section_clean.find_all('p'):
                paragraph_clean = tools.remove_tags_soup(paragraph, list_remove)
                data['content'].append(paragraph_clean.text)
        data_dict.append(data)
    return data_dict

def sections_frontiers(soup, list_remove):
    '''
    Function to extract sections from Frontiers html journals
    '''
    main_content = soup.find('div', class_='JournalFullText')
    main_content = tools.remove_tags_soup(main_content, list_remove)
    elements = main_content.find_all(['p','h2','h3'])
    data_dict = []
    for i in range(len(elements)):
        if elements[i].name == 'h2':
            data = {}
            data['name'] = elements[i].text
            data['type'] = 'h2'
            data['content'] = []
            if elements[i].next_sibling is not None:
                if elements[i].next_sibling.name == 'p':
                    data['content'] = list_to_content_frontiers(elements[i+1:])
            if elements[i].next_sibling is not None:
                if elements[i].next_sibling.name == 'h3':
                    data['content']= subheadings_content_frontiers(elements[i+1:])
            data_dict.append(data)
    return data_dict

def sections_tandf(soup, list_remove):
    '''
    Function to extract sections from Taylor and Francis html journals
    '''
    main_content = soup.find('div', class_ = 'hlFld-Fulltext')
    sections = main_content.find_all('div', class_ = ['NLM_sec NLM_sec_level_1', 'NLM_sec NLM_sec-type_intro NLM_sec_level_1',
                                                      'NLM_sec NLM_sec-type_results NLM_sec_level_1', 'NLM_sec NLM_sec-type_conclusions NLM_sec_level_1',
                                                      'NLM_sec NLM_sec-type_other NLM_sec_level_1', 'NLM_sec NLM_sec-type_results|discussion NLM_sec_level_1'])
    sections_clean = tools.remove_tags_soup_list(sections, list_remove)
    data_dict = []
    for section in sections_clean:
        data = {}
        data['name'] = section.find('h2').text
        data['type'] = 'h2'
        data['content'] = []
        if section.find('div', class_ = 'NLM_sec NLM_sec_level_2') is not None:
            elements = section.find_all('div', class_ = 'NLM_sec NLM_sec_level_2') 
            for element in elements:
                if element.find('div', class_ = 'NLM_sec NLM_sec_level_3') is not None:     #deals with h4 subheadings in subsection
                    data_sub = {}
                    data_sub['name'] = element.find('h3').text
                    data_sub['type'] = 'h3'
                    data_sub['content'] = []                                    
                    first_paragraph = element.p
                    paragraphs = first_paragraph.find_next_siblings('p')       #gets content before h4 subheadings
                    paragraphs.insert(0, first_paragraph)
                    for paragraph in paragraphs:
                        data_sub['content'].append(paragraph.text)
                    data['content'].append(data_sub)
                    sub_elements = element.find_all('div', class_ = 'NLM_sec NLM_sec_level_3')
                    for sub_element in sub_elements:
                        data_sub = {}
                        data_sub['name'] = sub_element.find('h4').text
                        data_sub['type'] = 'h4'                                 #gets content of h4 subheadings
                        data_sub['content'] = []
                        first_paragraph = sub_element.p
                        paragraphs = first_paragraph.find_next_siblings('p')
                        paragraphs.insert(0, first_paragraph)
                        for paragraph in paragraphs:
                            data_sub['content'].append(paragraph.text)
                        data['content'].append(data_sub)
                else:
                    data_sub = {}
                    data_sub['name'] = element.find('h3').text
                    data_sub['type'] = 'h3'
                    data_sub['content'] = []
                    paragraphs = tools.find_paragraphs(element, {'name':'p'})
                    # paragraphs = remove_tags_soup_list(paragraphs, {'name':'button'})
                    for paragraph in paragraphs:
                        data_sub['content'].append(paragraph.text)
                    data['content'].append(data_sub)
        else:
            paragraphs = tools.find_paragraphs(section, {'name':'p'})
            for paragraph in paragraphs:
                data['content'].append(paragraph.text)
        data_dict.append(data)
    return data_dict

def sections_mdpi(soup, list_remove):
    '''
    Function to extract sections from MDPI html journals
    '''
    main_content = soup.find('div', class_= 'html-body')
    section_1 = main_content.find('section')                #get main sections based on first section
    sections = section_1.find_next_siblings('section')
    sections.insert(0,section_1)
    data_dict = []
    for section in sections:
        data = {}
        data['name'] = section.find('h2').text
        data['type'] = 'h2'
        data['content'] = []
        if section.find('section') is not None:
            sub_sections_1 = section.find('section')
            sub_sections = sub_sections_1.find_next_siblings('section')
            sub_sections.insert(0,sub_sections_1)
            for sub_section in sub_sections:
                data_sub = {}
                data_sub['name'] = sub_section.find('h4').text
                data_sub['type'] = 'h4'
                data_sub['content'] = []
                if sub_section.find('section') is not None:
                    sub_sub_sections = sub_section.find_all('section')
                    for sub_sub_section in sub_sub_sections:                #deal with sub-sub-sections
                        data_sub_sub = {}
                        data_sub_sub['name'] = sub_sub_section.find('h4').text
                        data_sub_sub['type'] = 'h4'
                        data_sub_sub['content'] = []
                        paragraphs = tools.find_paragraphs(sub_sub_section,{'name':'div', 'class':'html-p'})
                        paragraphs_clean = tools.remove_tags_soup_list(paragraphs, list_remove)
                        for paragraph in paragraphs_clean:
                            data_sub_sub['content'].append(paragraph.text)
                        data_sub['content'].append(data_sub_sub)
                else:                                       
                    paragraphs = tools.find_paragraphs(sub_section,{'name':'div', 'class':'html-p'})  #deals with subsections without sub-sub-sections
                    paragraphs_clean = tools.remove_tags_soup_list(paragraphs, list_remove)
                    for paragraph in paragraphs_clean:
                        data_sub['content'].append(paragraph.text)
                data['content'].append(data_sub)
        else:
            paragraphs = tools.find_paragraphs(section,{'name':'div', 'class':'html-p'})
            paragraphs_clean = tools.remove_tags_soup_list(paragraphs, list_remove)
            for paragraph in paragraphs_clean:
                data['content'].append(paragraph.text)
        data_dict.append(data)
    return data_dict