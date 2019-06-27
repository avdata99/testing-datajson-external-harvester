from dataflows import Flow, printer, dump_to_path
from urllib.request import urlopen
import json

# For testing data.json
# just 1 dataset without validation errors http://data.exim.gov/data.json
# 316 datasets with validation erros https://data.wprdc.org/data.json
# 2868 datasets with validation errors https://www.energy.gov/sites/prod/files/2019/04/f61/doe-pdl-4-8-2019_0.json
# 87 MB json with validation errors https://data.nasa.gov/data.json --request_timeout 90


class DataJsonDataflowsHarvest:

    catalog = None  # info about data.json file
    datasets = None  # list of datasets in data.json

    parent_identifiers = []  # list of identifiers named in "isPartOf" property of harvested datasets
    child_identifiers = []  # datasets using "isPartOf" property

    valid_schemas = {
                    "https://project-open-data.cio.gov/v1.1/schema": '1.1',
                    }

    def check_catalog(self):
        catalog = self.catalog

        # https://github.com/GSA/ckanext-datajson/blob/datagov/ckanext/datajson/harvester_base.py#L120
        errors = []
        
        # https://github.com/GSA/ckanext-datajson/blob/datagov/ckanext/datajson/harvester_base.py#L137
        schema_value = catalog.get('conformsTo', '')
        if schema_value not in self.valid_schemas.keys():
            errors.append(f'Error reading json schema value. "{schema_value}" is not known schema')
        schema_version = self.valid_schemas.get(schema_value, '1.0')

        # list of needed catalog values  # https://github.com/GSA/ckanext-datajson/blob/datagov/ckanext/datajson/harvester_base.py#L152
        catalog_fields = ['@context', '@id', 'conformsTo', 'describedBy']
        self.catalog_extras = dict(('catalog_'+k, v) for (k, v) in catalog.items() if k in catalog_fields)

        return len(errors) == 0, errors


    def data_json_to_package(row):
        pass

# for saving importan data
dh = DataJsonDataflowsHarvest()

# Get data.json and flow
def data_json(url):

    # Read the data.json from URL
    raw_data = urlopen(url).read()
    json_data = json.loads(raw_data)
    #we expect az catalog an a list of datasets
    dh.catalog = None
    
    if type(json_data) == dict:
        datasets = json_data.pop('dataset')
        dh.catalog = json_data
        ok, errors = dh.check_catalog()
        print(f'**** Catalog: {dh.catalog}')
        print(f'******* is ok?: {ok}')
        for error in errors:
            print(f'************* error: {error}')

    elif type(json_data) == list:  # I never see this but ckan ext expect for it.
        print('List of datasets finded')
        datasets = json_data
    else:
        raise Exception('Unknown data.json type')
        
    row = {}
    for dataset in datasets:
        # yield dict(title=dataset['title'], description=dataset['description'])
        
        # row['title'] = dataset['title']
        # row['description'] = dataset['description']
        # yield(row)
        
        yield(dataset)

def list_parents(row):
    # get a list of datasets with "isPartOf" and his childs.
    # https://github.com/GSA/ckanext-datajson/blob/datagov/ckanext/datajson/harvester_base.py#L145
    if row.get('isPartOf', None):
        dh.parent_identifiers.append(row['isPartOf'])
        dh.child_identifiers.append(row['identifier'])
        print('{} is part of {}'.fortmat(row['identifier'], row['isPartOf']))


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
    name, url = 'WPRDC_FULL', 'https://data.wprdc.org/data.json'
    Flow(
        data_json(url),
        clean_duplicated_identifiers,
        list_parents,
        printer(num_rows=1), # , tablefmt='html')
        dump_to_path(f'package_{name}'),
    ).process()[1]