# ETL for data.json

Training for ETL in data.json files.  

## Usage

```
usage: harvest_data_json.py [-h] [--url URL] [--name NAME]

optional arguments:
  -h, --help   show this help message and exit
  --url URL    URL of the data.json
  --name NAME  Name of the resource (for generate the containing folder)
```
### Real examples

```
python3 harvest_data_json.py --name exim --url http://data.exim.gov/data.json

python3 harvest_data_json.py --name "Western Pennsylvania Regional Data Center" --url https://data.wprdc.org/data.json

python3 harvest_data_json.py --name energy-data --url https://www.energy.gov/sites/prod/files/2019/04/f61/doe-pdl-4-8-2019_0.json

#NASA requires more time (--request_timeout), it has 87MB (24432 datasets) of data.json.
python3 harvest_data_json.py --name NASA-data --url https://data.nasa.gov/data.json --request_timeout 90

```

## OK example

```
Downloaded OK
JSON OK
Validate OK. 1 datasets
 - Dataset: Authorizations From 10/01/2006 Thru 12/31/2018: This file contains all authorizations approved between 10/01/2006 and 12/31/2018
Please note that the asterisked Working Capital transactions were extended during the period of EXIM Bank’s lapse in authority in conformance with original authorization agreements. These deals were originally authorized before the lapse as multiyear facilities with annual extensions. This record represents the extension of the prior authorization. EXIM did not authorize new business during its lapse in authority. 
```

## Error example
```
Downloaded OK
JSON OK
Error validating data: Error validating JsonSchema: '[[REDACTED-EX B6]]' is not of type 'array'

Failed validating 'type' in schema['properties']['dataset']['items']['properties']['keyword']:
    {'description': 'Tags (or keywords) help users discover your dataset; '
                    'please include terms that would be used by technical '
                    'and non-technical users.',
     'items': {'minLength': 1, 'type': 'string'},
     'minItems': 1,
     'title': 'Tags',
     'type': 'array'}

On instance['dataset'][43]['keyword']:
    '[[REDACTED-EX B6]]'
----------------
Validate FAILED. 2868 datasets

 - Dataset: Agency Parking: Agency parking application that provides the capability to record and query parking assignments. Access is limited to designated personnel of the Facilities and Logistics
 - Dataset: Congressional and Intergovernmental Affairs webpage: The Office of Congressional and Intergovernmental Affairs is dedicated to its mission of providing guidance on legislative and policy issues, informing constituencies on energy matters, and serving as a liaison between the Department, Congress, State, local, and Tribal governments, as well as other Federal agencies and stakeholder groups.
 - Dataset: DATA Act for U.S. Department of Energy: This is a link where the U.S. Department of Energy DATA Act reporting can be found.
 - Dataset: Agency IT Policy Archive: IT Policy Archive
 
 ...
 ...

```
