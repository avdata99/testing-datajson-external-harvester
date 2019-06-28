""" 
Harvest a list of data.json sources and compare with CKAN resources
Finally create, update or delete packages and resources in CKAN
Any source must inform an URL an the ID to compare.
"""

import json
import os
from slugify import slugify
from .libs.data_json import DataJSON
from .libs.data_gov_api import CKANPortalAPI
import sys
import argparse
import logging
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument("--url", type=str, help="URL of the data.json")
parser.add_argument("--name", type=str, help="Name of the resource (for generate the containing folder)")
parser.add_argument("--request_timeout", type=int, default=30, help="Request data.json URL timeout")
args = parser.parse_args()

base_folder = 'temp_files'  # data.json and API results from CKAN instances
local_folder = os.path.join(base_folder, args.name)
if not os.path.isdir(local_folder):
    os.mkdir(local_folder)

local_data_json_file = os.path.join(local_folder, 'data.json')
local_logs_file = os.path.join(local_folder, 'log')
local_package_json_file = os.path.join(local_folder, 'datapackages.json')

c_handler = logging.StreamHandler()
f_handler = logging.FileHandler(local_logs_file)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.setLevel(logging.DEBUG)

datajson = DataJSON()
datajson.url = args.url

ret, info = datajson.download_data_json(timeout=args.request_timeout)
if not ret:
    logger.error('Error getting data: {}'.format(info))
    sys.exit(1)
logger.info('Downloaded OK')

ret, info = datajson.load_data_json()
if not ret:
    logger.error('Error loading JSON data: {}'.format(info))
    sys.exit(1)
    
logger.info('JSON OK')
ret, info = datajson.validate_json()
if not ret:
    logger.error('Error validating data: {}\n----------------\n'.format(info))
    # continue  # USE invalid too
    logger.info('Validate FAILED: {} datasets'.format(len(datajson.datasets)))
else:
    logger.info('Validate OK: {} datasets'.format(len(datajson.datasets)))
c = 0
for dataset in datajson.datasets: 
    c += 1
    if c < 10:
        logger.debug(' - Dataset: {}'.format(dataset['title']))
        # logger.debug(' - Dataset: {}: {}'.format(dataset['title'], dataset['description']))
    else:
        logger.debug(' ... ')
        break

datajson.save_data_json(path=local_data_json_file)
datajson.save_datasets(path=local_package_json_file)

