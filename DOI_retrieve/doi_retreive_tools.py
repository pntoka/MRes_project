'''
Functions to retrieve DOIs using semantic scholar API
'''
import requests
import time
import pandas as pd

def sem_scholar(query, pub_date, offset_number):
    '''
    Function that takes a query, publication date and offset number and returns a json object with the results
    '''
    query = query.replace(" ", "+")
    offset = offset_number
    fields = 'externalIds'   #fields to return, DOIs are in externalIds
    types = 'JournalArticle'   #type of publication, JournalArticle is the one of interest
    dates = pub_date    #publication date inclusive
    url = f'https://api.semanticscholar.org/graph/v1/paper/search?query={query}&offset={offset}&limit=100&fields={fields}&publicationTypes={types}&year={dates}'
    response = requests.get(url)
    count = 0
    while response.status_code != 200:
        print('Error: ' + str(response.status_code))        #if the request is not successful, try again
        time.sleep(0.5)
        response = requests.get(url)
        count += 1
        if count == 10:
            break
    data = response.json()      #return the response as json object
    return data

def offset_counter(number):
        return list(range(100,number+1,100))    #function to create a list of offsets to use in the API request

def doi_list(query, pub_date):
    '''
    Function that takes a query and publication date and returns a list of DOIs
    '''
    offset = 0
    data = sem_scholar(query, pub_date, offset)
    total = data['total']
    doi_list = []
    if total > 100:
        offset_list = offset_counter(total)
        for offset in offset_list:
            data = sem_scholar(query, pub_date, offset)
            for paper in data['data']:
                if 'DOI' in paper['externalIds']:
                    doi_list.append(paper['externalIds']['DOI'])
                    time.sleep(0.5)
    else:
        for paper in data['data']:
            if 'DOI' in paper['externalIds']:
                doi_list.append(paper['externalIds']['DOI'])
    return doi_list

def storeDOI(dois, save_dir, pub_date):   #Function to save list of dois for specific publication date
    with open(save_dir + f"doi_{pub_date}.txt", "a", encoding="utf-8") as save_file:
        for doi in dois:      #saves dois to doi.txt file with each doi on new line
            save_file.write(doi + "\n")


def doi_list_date_range(query, pub_dates, save_dir):
    '''
    Function that takes a query, a list of publication dates and a directory to save the results and returns a list of DOIs
    and return csv file with number of DOIs per publication date
    '''
    df = pd.DataFrame(columns=['query', 'pub_date', 'number_of_results'])
    for pub_date in pub_dates:
        doi_results = doi_list(query, pub_date)
        row = {'query': query, 'pub_date': pub_date, 'number_of_results': len(doi_results)}
        new_df = pd.DataFrame([row])
        df = pd.concat([df, new_df], axis=0, ignore_index=True)
        storeDOI(doi_results, save_dir, pub_date)
    df.to_csv(save_dir + 'sem_scholar_results.csv', index=False)

