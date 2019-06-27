from dataflows import Flow, printer, dump_to_path
from urllib.request import urlopen
import json

# For testing data.json
# just 1 dataset without validation errors http://data.exim.gov/data.json
# 316 datasets with validation erros https://data.wprdc.org/data.json
# 2868 datasets with validation errors https://www.energy.gov/sites/prod/files/2019/04/f61/doe-pdl-4-8-2019_0.json
# 87 MB json with validation errors https://data.nasa.gov/data.json --request_timeout 90

# Get data.json and flow
def data_json(url):

    # Read the data.json from URL
    raw_data = urlopen(url).read()
    json_data = json.loads(raw_data)
    catalog = None
    
    if type(json_data) == dict:
        datasets = json_data.pop('dataset')
        catalog = json_data
        print(f'**** Catalog: {catalog}')
        
    elif type(json_data) == list:  # I never see this but ckan ext expect for it.
        print('List of datasets finded')
        datasets = json_data
    else:
        raise Exception('Unknown data.json type')
        
    row = {}
    for dataset in datasets:
        yield dict(title=dataset['title'],
                    description=dataset['description'],
                    identifier=dataset['identifier'],
                    isPartOf=dataset.get('isPartOf', None))
        
        # row['title'] = dataset['title']
        # row['description'] = dataset['description']
        # yield(row)
        
        # yield(dataset)

def clean_duplicated_identifiers(rows):
    unique_identifiers = []
    duplicates = []
    processed = 0
    for row in rows:
        if row['identifier'] not in unique_identifiers:
            unique_identifiers.append(row['identifier'])
            yield(row)
            processed += 1
        else:
            duplicates.append(row['identifier'])
            print('Duplicated {}'.format(row['identifier']))
    print('{} duplicates deleted. {} OK'.format(len(duplicates), processed))

if __name__ == '__main__':

    # name, url = 'EXIM', 'http://data.exim.gov/data.json'
    name, url = 'WPRDC', 'https://data.wprdc.org/data.json'
    Flow(
        data_json(url),
        clean_duplicated_identifiers,
        printer(num_rows=1), # , tablefmt='html')
        dump_to_path(f'package_{name}'),
    ).process()[1]