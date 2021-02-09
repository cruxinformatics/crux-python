import os
import logging

from crux import Crux, TRACE
from crux.exceptions import CruxAPIError, CruxResourceNotFoundError
from crux.models import Dataset
from crux.models.file import File
from datetime import datetime
from typing import Generator


envfile_name = 'client.env'
if os.path.exists(envfile_name):
    with open(envfile_name) as file:
        for line in file:
            if line.startswith('#') or not line.strip():
                continue
            key, value = line.strip().split('=', 1)
            os.environ[key] = value


now = datetime.now().strftime('%Y.%m.%d-%H.%M.%S')
logfile_name = f'client_regression_{now}.log'
logging.basicConfig(
    level=TRACE,
    filename=logfile_name,
)

logger = logging.getLogger(__name__)
logger.setLevel(TRACE)


def log(message):
    logger.log(TRACE, message)


print_styles = dict()
print_styles['SUCCESS'] = 1
print_styles['ERROR'] = 2
print_styles['INFO'] = 3


def print_custom(message, style=print_styles['INFO'], move_caret=True):
    green = '\033[92m'
    yellow = '\033[93m'
    red = '\033[91m'
    end_symbol = '\033[0m'

    if style == print_styles['SUCCESS']:
        color = green
    elif style == print_styles['ERROR']:
        color = red
    else:
        color = yellow

    message = f"{color}{message}{end_symbol}"

    if move_caret:
        message = message.ljust(100)
        print(message)
    else:
        print(message, end='\r')


def format_func_name(name):
    return f'\"{name}\"'.ljust(40)


def print_pending(func_name):
    print_custom(f"{format_func_name(func_name)}: checking...", move_caret=False)


def print_success(func_name):
    print_custom(f"{format_func_name(func_name)}: success", print_styles['SUCCESS'])


def print_failure(func_name):
    print_custom(f"{format_func_name(func_name)}: failure", print_styles['ERROR'])


def print_info(func_name, message):
    print_custom(f"{format_func_name(func_name)}: {message}")


def run_tests():
    """Main Function containing tests"""

    api_key = os.getenv('CRUX_API_KEY')
    dataset_id = os.getenv('CRUX_DATASET_ID')
    resource_id = os.getenv('CRUX_RESOURCE_ID')

    if not api_key:
        raise ValueError("Missing API key for Crux client!")

    client = Crux(api_key)

    def fetch_dataset():
        try:
            ds_id = dataset_id

            if not dataset_id:
                datasets = client.list_datasets()
                log(datasets)
                ds_id = datasets[0].id

            dataset = client.get_dataset(ds_id)
            log(dataset)

            return dataset
        except (TypeError, CruxResourceNotFoundError) as e:
            if isinstance(err, CruxResourceNotFoundError):
                log(e)
            raise ValueError('missing dataset for testing')

    def fetch_resource():
        try:
            r_id = resource_id

            if not r_id:
                dataset = fetch_dataset()
                resources = dataset.list_resources()
                log(resources)

                resource = next(resources)

                if not resource:
                    raise TypeError

                r_id = resource.id

            resource = client.get_resource(r_id)
            log(resource)

            return resource
        except TypeError:
            raise ValueError('missing resource for testing')
        except CruxAPIError as e:
            if str(e) == f'{{\'statusCode\': 400, \'error\': \'Bad Request\', \'message\': \'Incorrect type - expected a resource. id={r_id}\', \'data\': \'Incorrect type - expected a resource. id={r_id}\'}}':
                log(e)
                raise ValueError('missing resource for testing')
            else:
                raise e

    """test functions themselves"""
    def whoami():
        func_name = 'whoami'
        print_pending(func_name)

        try:
            response = client.whoami()
            log(response)

            api_key_received = response.to_dict()['apiKey']

            if api_key_received != api_key:
                raise KeyError

            print_success(func_name)
        except KeyError:
            print_failure(func_name)

    def list_datasets():
        func_name = 'list_datasets'
        print_pending(func_name)

        response = client.list_datasets()
        log(response)

        if isinstance(response, list):
            print_success(func_name)
        else:
            print_failure(func_name)

    def get_dataset():
        func_name = 'get_dataset'
        print_pending(func_name)

        try:
            response = fetch_dataset()
        except ValueError as e:
            print_info(func_name, e)
            return

        if isinstance(response, Dataset):
            print_success(func_name)
        else:
            print_failure(func_name)

    def find_resources_by_label():
        func_name = 'Dataset.find_resources_by_label'
        print_pending(func_name)

        try:
            dataset = fetch_dataset()
        except ValueError as e:
            print_info(func_name, e)
            return

        response = dataset.find_resources_by_label([
            {'op': 'ne', 'key': 'id', 'val': '0'}
        ])
        log(response)

        if isinstance(response, Generator):
            print_success(func_name)
        else:
            print_failure(func_name)

    def get_files_range():
        func_name = 'Dataset.get_files_range'
        print_pending(func_name)

        try:
            dataset = fetch_dataset()
        except ValueError as e:
            print_info(func_name, e)
            return

        response = dataset.get_files_range(start_date="1/1/2021")
        log(response)

        if isinstance(response, Generator):
            print_success(func_name)
        else:
            print_failure(func_name)

    def download_files():
        func_name = 'Dataset.download_files'
        print_pending(func_name)

        try:
            dataset = fetch_dataset()
        except ValueError as e:
            print_info(func_name, e)
            return

        response = dataset.download_files(folder='usr/bin/local', local_path='/')
        log(response)

        if isinstance(response, Generator):
            print_success(func_name)
        else:
            print_failure(func_name)

    def list_dataset_permissions():
        func_name = 'Dataset.list_permissions'
        print_pending(func_name)

        try:
            dataset = fetch_dataset()
            response = dataset.list_permissions()
            log(response)
        except ValueError as e:
            print_info(func_name, e)
            return
        except CruxAPIError as e:
            log(e)
            if not (e.status_code == 403):
                raise e
            print_info(func_name, 'lacking access to check')
            return

        if isinstance(response, Generator):
            print_success(func_name)
        else:
            print_failure(func_name)

    def get_resource():
        func_name = 'Dataset.get_resource'
        print_pending(func_name)

        try:
            response = fetch_resource()
            log(response)
        except ValueError as e:
            print_info(func_name, e)
            return

        if isinstance(response, File):
            print_success(func_name)
        else:
            print_failure(func_name)

    def download_resource():
        func_name = 'Resource.download'
        print_pending(func_name)

        try:
            resource = fetch_resource()
        except ValueError as e:
            print_info(func_name, e)
            return

        file_path = 'TEST___download_resource___FEEL_FREE_TO_DELETE___'

        response = resource.download(file_path)
        log(response)

        if response and os.path.exists(file_path):
            print_success(func_name)
            os.remove(file_path)
        else:
            print_failure(func_name)

    def iter_resource_content():
        func_name = 'Resource.iter_content'
        print_pending(func_name)

        try:
            resource = fetch_resource()
        except ValueError as e:
            print_info(func_name, e)
            return

        response = resource.iter_content()
        log(response)

        if isinstance(response, Generator):
            print_success(func_name)
        else:
            print_failure(func_name)

    def list_resource_permissions():
        func_name = 'Resource.list_permissions'
        print_pending(func_name)

        try:
            resource = fetch_resource()
            response = resource.list_permissions()
            log(response)
        except ValueError as e:
            print_info(func_name, e)
            return
        except CruxAPIError as e:
            log(e)
            if not (e.status_code == 403):
                raise e
            print_info(func_name, 'lacking access to check')
            return

        if isinstance(response, Generator):
            print_success(func_name)
        else:
            print_failure(func_name)

    whoami()
    list_datasets()
    get_dataset()
    find_resources_by_label()
    get_files_range()
    download_files()
    list_dataset_permissions()
    get_resource()
    download_resource()
    iter_resource_content()
    list_resource_permissions()


try:
    run_tests()
except Exception as err:
    log(err)
    print_custom('Error occurred during tests\' run: ' + str(err), print_styles['ERROR'])

print_custom(f'\nLogs of the tests\' run could be found at "{logfile_name}".')
