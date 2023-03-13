'''
Package converts dois to filenames and read dois from a file
'''

def doi_to_filename(dois):
    '''
    Function to convert a list of dois to a list of filenames of the full text html/xml
    '''
    filenames = []
    for doi in dois:
        filenames.append(doi.replace('/', '-')+'.txt')
    return filenames
    
def doi_list(filename):
    '''
    Function to read dois from a file and return a list of dois
    '''
    dois = []
    for line in open(filename, 'r'):
        dois.append(line.strip())
    return dois