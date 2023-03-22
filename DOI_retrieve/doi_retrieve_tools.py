'''
Functions to retrieve DOIs using semantic scholar API
'''
import requests
import time
import pandas as pd
import os

def sem_scholar(query, pub_date, offset_number):
    '''
    Function that takes a query, publication date and offset number and returns a json object with the results
    '''
    query = query.replace(" ", "+")
    offset = offset_number
    fields = 'externalIds'   #fields to return, DOIs are in externalIds as well as publication type for further filtering
    types = 'JournalArticle'   #type of publication, JournalArticle is the one of interest
    dates = pub_date    #publication date inclusive
    url = f'https://api.semanticscholar.org/graph/v1/paper/search?query={query}&offset={offset}&limit=100&publicationTypes={types}&fields={fields}&year={dates}'
    response = requests.get(url)
    count = 0
    while response.status_code != 200:
        print('Error: ' + str(response.status_code) +' trying request again')        #if the request is not successful, try again
        time.sleep(0.5)
        response = requests.get(url)
        count += 1
        if count == 10:
            break
    data = response.json()      #return the response as json object
    print(f'Request successful for pub date = {pub_date} and offset = {offset_number}')
    return data


def sem_scholar_2(query, pub_date, offset_number):
    '''
    Function that takes a query, publication date and offset number and returns a json object with the results
    Returns DOI and publication types, searches all publication types
    '''
    query = query.replace(" ", "+")
    offset = offset_number
    fields = 'externalIds,publicationTypes'   #fields to return, DOIs are in externalIds as well as publication type for further filtering
    dates = pub_date    #publication date inclusive
    url = f'https://api.semanticscholar.org/graph/v1/paper/search?query={query}&offset={offset}&limit=100&fields={fields}&year={dates}'
    response = requests.get(url)
    count = 0
    while response.status_code != 200:
        print('Error: ' + str(response.status_code)+' trying request again')        #if the request is not successful, try again
        print('This is the url: ' + url)
        time.sleep(60)
        response = requests.get(url)
        count += 1
        if count == 15:
            break
    data = response.json()      #return the response as json object
    print(f'Request successful for pub date = {pub_date} and offset = {offset_number}')
    return data


def offset_counter(number):
        offsets = (number-1)//100
        return list(range(100,offsets*100+1,100))    #function to create a list of offsets to use in the API request


def doi_list(query, pub_date):
    '''
    Function that takes a query and publication date and returns a list of DOIs
    '''
    offset = 0
    data = sem_scholar(query, pub_date, offset)
    total = data['total']
    doi_list = []
    for paper in data['data']:
            if 'DOI' in paper['externalIds']:
                doi_list.append(paper['externalIds']['DOI'])
    if total > 100:
        offset_list = offset_counter(total)
        for offset in offset_list:
            data = sem_scholar(query, pub_date, offset)
            for paper in data['data']:
                if 'DOI' in paper['externalIds']:
                    doi_list.append(paper['externalIds']['DOI'])
            time.sleep(3)
    return doi_list


def doi_pubtype_dict(query, pub_date):
    '''
    Function that takes a query and publication date and returns a dictionary of DOIs and publication types
    '''
    offset = 0
    data = sem_scholar_2(query, pub_date, offset)
    total = data['total']
    if total == 0:
        print('No results found')
        return None
    new_total = total
    doi_dict = {}
    for paper in data['data']:
        if 'DOI' in paper['externalIds']:
            doi_dict[paper['externalIds']['DOI']] = paper['publicationTypes']
    print(f'Saved {len(doi_dict)} DOIs out of {total} result from {pub_date}')     #print statement to show progress
    if total > 100:
        offset_list = offset_counter(total)
        for offset in offset_list:
            if offset > new_total:
                print('Total is less than offset')
                break
            data = sem_scholar_2(query, pub_date, offset)
            for paper in data['data']:
                if 'DOI' in paper['externalIds']:
                    doi_dict[paper['externalIds']['DOI']] = paper['publicationTypes']
            print(f'Saved {len(doi_dict)} out of {total} results from {pub_date}')  #print statement to show progress
            new_total = data['total']
            time.sleep(3)
    return doi_dict


def doi_dict_filter(doi_dict, pub_type, pub_skip):
    '''
    Function that takes a doi dictionary and a publication type and returns a list of DOIs that match the publication type without the publication type to skip
    '''
    doi_list = []
    for doi, pub_types in doi_dict.items():
        if pub_types == None:
            doi_list.append(doi)
        elif pub_type in pub_types and pub_skip not in pub_types:
            doi_list.append(doi)
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


def doi_list_date_range_2(query, pub_dates, save_dir):
    '''
    Function that takes a query, a list of publication dates and a directory to save the results and returns a list of DOIs
    and return csv file with number of DOIs per publication date. 
    Searches all publication types and returns only JournalArticle and ones with no type specified
    '''
    df = pd.DataFrame(columns=['query', 'pub_date', 'number_of_results'])
    for pub_date in pub_dates:
        doi_dict = doi_pubtype_dict(query, pub_date)
        if doi_dict == None:
            row = {'query': query, 'pub_date': pub_date, 'number_of_results': 0}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            continue
        else:
            print(f'Retrieved {len(doi_dict)} DOIs from {pub_date}')   #print statement to show progress
            doi_results = doi_dict_filter(doi_dict, 'JournalArticle', 'Review')
            print(f'Filtered DOIs to {len(doi_results)}')        #print statement to show progress
            row = {'query': query, 'pub_date': pub_date, 'number_of_results': len(doi_results)}
            new_df = pd.DataFrame([row])
            df = pd.concat([df, new_df], axis=0, ignore_index=True)
            storeDOI(doi_results, save_dir, pub_date)
            print(f'Saved {len(doi_results)} DOIs from {pub_date}')   #print statement to show progress
    df.to_csv(save_dir + 'sem_scholar_results.csv', index=False)


def doi_search(query_list, pub_dates, save_dir):
    '''
    Function that takes a list of queries, a list of publication dates and a directory to save the results and returns a list of DOIs
    and return csv file with number of DOIs per publication date. Results for each query are saved in a different directory
    '''
    for query in query_list:
        save_dir_results = save_dir + query.replace(' ', '_') + '/'
        os.mkdir(save_dir_results)
        doi_list_date_range_2(query, pub_dates, save_dir_results)

def doi_unique(query_list, pub_dates, save_dir):
    '''
    Function that goes through search results for different queries and returns a list of unique DOIs that is saved in a file
    '''
    doi_list = []
    for query in query_list:
        folder = save_dir + query.replace(' ', '_') + '/'
        for year in pub_dates:
            if os.path.exists(folder + f"doi_{year}.txt") == False:
                continue
            else:
                with open(folder + f"doi_{year}.txt", "r", encoding="utf-8") as file:
                    dois = file.read().splitlines()
                doi_list.extend(dois)
    doi_list_unique = list(set(doi_list))   #removes duplicates and leaves only unique dois
    with open(save_dir + f"doi_unique.txt", "a", encoding="utf-8") as save_file:
        for doi in doi_list_unique:      #saves dois to doi.txt file with each doi on new line
            save_file.write(doi + "\n")
    
