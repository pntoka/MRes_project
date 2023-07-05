import paper_filter as pf


if __name__ == '__main__':
    save_dir = r'C:\Users\Piotr\OneDrive - Imperial College London\MRes_project_data\abstracts'
    data_file = r'C:\Users\Piotr\OneDrive - Imperial College London\MRes_project_data\ceder_extract_data\all_extracted_data_clean.json'
    data = pf.get_data(data_file)
    exclude_list = [
        '10.1002/nano.202100140', '10.3390/c8040068','10.1007/s42114-022-00616-x',
        '10.3390/photochem1030023','10.3390/C5010012','10.1002/bte2.20220041','10.1016/j.microc.2021.106272','10.3390/PROCEEDINGS2110652','10.1007/s13203-018-0193-x',
        '10.1007/s40243-013-0017-y','10.1039/C3CE40579F','10.1016/j.mseb.2008.09.016','10.1039/D0NJ01754J','10.1007/s41127-022-00055-x','10.1021/CG0504556','10.1002/NANO.202100099','10.1080/10584587.2012.685696',
        '10.1016/j.microc.2021.106273','10.1080/10584587.2012.686796','10.1039/C5RA09613H'
    ]
    abs_keywords = [
        'Carbon dots', 'carbon dots', 'carbon dot', 'Carbon dot', 'CD', 'CDs', 'Graphene quantum dots', 'graphene quantum dots',
        'graphene quantum dot', 'Graphene quantum dot', 'GQDs', 'GQD', 'Carbon nanodots', 'carbon nanodots', 'carbon nanodot',
        'CPDs', 'CPD', 'carbon polymer dots', 'Carbon polymer dots', 'carbon polymer dot', 'Carbon polymer dot', 'carbon quantum dots',
        'carbon quantum dot', 'Carbon quantum dots', 'Carbon quantum dot', 'CQDs', 'CQD', 'carbon nanoparticles', 'Carbon nanoparticles',
        'carbon-dots', 'Carbon-dots', 'CNDs', 'CND'

    ]
    mat_keywords = [
        'CDs', 'CD', 'carbon dots', 'GQD', 'GQDs', 'CNDs', 'CND'
    ]
    # doi = '10.1002/cssc.201700474'
    # for entry in data:
    #     if entry['doi'] == doi:
    #         data_test = [entry]
    results = pf.filter_dois(data, exclude_list, abs_keywords, mat_keywords, save_dir)
    print(len(results))
    with open(r'C:\Users\Piotr\OneDrive - Imperial College London\MRes_project_data\abstracts\filter_results.txt', 'w', encoding='utf-8') as file:
        for result in results:
            file.write(str(result)+'\n')
