'''
Script to retrieve a list of DOIs from semantic scholar based on search query and publication date
'''
import doi_retrieve_tools

if __name__== '__main__':
    query = 'carbon dots hydrothermal synthesis'
    save_dir = '/Users/pnt17/Library/CloudStorage/OneDrive-ImperialCollegeLondon/MRes_project_data/doi_sem_scholar/'
    pub_dates = list(range(2005,2024,1))
    doi_retrieve_tools.doi_list_date_range(query, pub_dates, save_dir)