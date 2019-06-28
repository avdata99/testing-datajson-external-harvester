import json
import requests
import logging
logger = logging.getLogger(__name__)

class CKANPortalAPI:
    """ API and data from data.gov 
        API SPECS: https://docs.ckan.org/en/latest/api/index.html """
        
    base_url = 'https://catalog.data.gov'  # default data.gov
    package_list_url = '/api/3/action/package_list'  # redirect to package_search (?)
    package_search_url = '/api/3/action/package_search'  # iterate with start and rows GET params
    package_list = None  

    def get_all_package_list(self, rows=1000):
        """ get all packages using search (list is not working 
            "rows" is the page size """
        
        start = 0
        sort = "metadata_modified desc"

        params = {'start': start, 'rows': rows, 'sort': sort}
        url = '{}{}'.format(self.base_url, self.package_list_url)
        page = 0
        #TODO check for a real paginated version
        while url:
            page += 1
            logger.debug(f'Searching {url} PAGE:{page} start:{start}, rows:{rows}')
            
            try:
                req = requests.get(url, params=params)
            except Exception as e:
                error = 'ERROR Donwloading package list: {} [{}]'.format(url, e)
                raise ValueError('Failed to get package list at {}'.format(url))
            
            content = req.content
            try:
                json_content = json.loads(content)  # check for encoding errors
            except Exception as e:
                error = 'ERROR parsing JSON data: {} [{}]'.format(content, e)
                raise ValueError(error)
            
            if not json_content['success']:
                error = 'API response failed: {}'.format(json_content.get('error', None))
                raise ValueError(error)
            
            result = json_content['result']
            count_results = result['count']
            sort_results = result['sort']
            facet_results = result['facets']
            results = result['results']
            real_results_count = len(results)
            logger.debug(f'{real_results_count} results')

            if real_results_count == 0:
                url = None
            else:
                start += rows
                params = {'start': start, 'rows': rows, 'sort': sort}

            yield(results)


if __name__ == '__main__':
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('api.log')
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)
    logger.setLevel(logging.DEBUG)

    cpa = CKANPortalAPI()
    resources = 0
    for packages in cpa.get_all_package_list():
        for package in packages:
            pkg_resources = len(package['resources'])
            resources += pkg_resources
        print('{} total resources'.format(resources))
    
