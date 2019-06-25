"""
Data JSON ETL training
    About data json harvester https://hackmd.io/WwUfJozQQMu1I5EFcauhOg?both#datajson-harvester
    load_remote_catalog: https://github.com/GSA/ckanext-datajson/blob/datagov/ckanext/datajson/harvester_datajson.py#L21
    build data json: https://github.com/GSA/ckanext-datajson/blob/datagov/ckanext/datajson/build_datajsonld.py
    actual validator https://github.com/GSA/ckanext-datajson/blob/datagov/ckanext/datajson/datajsonvalidator.py

    check the schema definition: https://project-open-data.cio.gov/v1.1/schema/catalog.json
    validate: maybe with this https://github.com/Julian/jsonschema

"""
import requests
import jsonschema as jss
import json

class JSONSchema:
    """ a JSON Schema definition for validating data.json files """
    json_content = None  # schema content

    def __init__(self, url):
        self.url = url  # URL of de schema definition. e.g. https://project-open-data.cio.gov/v1.1/schema/catalog.json
        try:
            req = requests.get(self.url)
        except Exception as e:
            error = 'ERROR Donwloading schema: {} [{}]'.format(self.url, e)
            raise ValueError('Failed to get schema definition at {}'.format(url))
        
        content = req.content
        try:
            self.json_content = json.loads(content)  # check for encoding errors
        except Exception as e:
            error = 'ERROR parsing JSON data: {} [{}]'.format(content, e)
            raise ValueError(error)



class DataJSON:
    """ a data.json file for read and validation """
    url = None  # URL of de data.json file
    url_download_timeout = 30
    raw_data_json = None  # raw downloaded text
    data_json = None  # JSON readed from data.json file

    datasets = []  # all datasets described in data.json

    def download_data_json(self):
        """ download de data.json file """
        if self.url is None:
            return False, "No URL defined"
        
        try:
            req = requests.get(self.url, timeout=self.url_download_timeout)
        except Exception as e:
            error = 'ERROR Donwloading data: {} [{}]'.format(self.url, e)
            return False, error
            
        self.raw_data_json = req.content
        return True, None
    
    def load_data_json(self):
        """ load as a JSON object """
        try:
            self.data_json = json.loads(self.raw_data_json)  # check for encoding errors
        except Exception as e:
            error = 'ERROR parsing JSON data: {}'.format(e)
            return False, error
    
        return True, None

    def validate_json(self):
        if self.data_json is None:
            return False, 'No data json available'
        schema_definition_url = self.data_json['describedBy']
        schema = JSONSchema(url=schema_definition_url)
        
        # validate with jsonschema lib
        # many data.json are not extrictly valid, we use as if they
        is_valid = True
        try:
            jss.validate(instance=self.data_json, schema=schema.json_content)
        except Exception as e:
            error = "Error validating JsonSchema: {}".format(e)
            is_valid = False
        
        #read datasets by now, even in error
        self.datasets = self.data_json['dataset']

        if not is_valid:
            return False, error
        return True, None
    