import json
import os
from slugify import slugify
from data_json_harvest.datajson import DataJSON

data_json_examples = [{'name': 'Energy data', 'json_url': 'https://www.energy.gov/sites/prod/files/2019/04/f61/doe-pdl-4-8-2019_0.json'},
                        {'name': 'Western Pennsylvania Regional Data Center', 'json_url': 'https://data.wprdc.org/data.json'},
                        {'name': 'NASA data', 'json_url': 'https://data.nasa.gov/data.json'},
                        {'name': 'Expo-Impo Bank data', 'json_url': 'http://data.exim.gov/data.json'}
                        ]

def get_data_json_examples(destination_folder='sample-data-json'):
    for data_json in data_json_examples:
        local_file_name = '{}-{}'.format(slugify(data_json['name']), 'data.json')
        local_file = os.path.join(destination_folder, local_file_name)

        # Write logs for each file
        f = open('{}.log'.format(local_file), 'w')

        datajson = DataJSON()
        datajson.url = data_json['json_url']
        ret, info = datajson.download_data_json()
        if not ret:
            f.write('Error getting data: {}\n'.format(info))
            continue
        f.write('Downloaded OK\n')
        ret, info = datajson.load_data_json()
        if not ret:
            f.write('Error loading JSON data: {}'.format(info))
            continue
        f.write('JSON OK\n')
        ret, info = datajson.validate_json()
        if not ret:
            f.write('Error validating data: {}\n----------------\n'.format(info))
            # continue  # USE invalid too
            f.write('Validate FAILED. {} datasets\n'.format(len(datajson.datasets)))
        else:
            f.write('Validate OK. {} datasets\n'.format(len(datajson.datasets)))
        for dataset in datajson.datasets: 
            f.write('\n - Dataset: {}: {}'.format(dataset['title'], dataset['description']))
        f.close()
        
        # write as a local file
        dmp = json.dumps(datajson.data_json, indent=2)
        f = open(local_file, 'w')
        f.write(dmp)
        f.close()

if __name__ == '__main__':
    get_data_json_examples()