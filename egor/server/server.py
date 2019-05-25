import json
import os
import socketserver
from http.server import BaseHTTPRequestHandler

import urllib3
from knack.log import get_logger

from egor.meta import MetaDataHandler

logger = get_logger(__name__)

task_meta = None


def extract_name(task_name: str):
    return task_name.replace(' ', '').replace('.', '')


def create_task(task_description):
    """
    Creates the task's files and directories
    """
    global task_meta

    task_object = json.loads(task_description)

    task_name = extract_name(task_object['name'])
    # setting the task name to be returned by the start_server method
    # so it can be accessible outside of this module

    logger.info('Creating task {} ...'.format(task_name))
    cur_dir_path = os.path.abspath(os.path.curdir)
    task_dir_path = os.path.join(cur_dir_path, task_name)
    input_dir_path = os.path.join(task_dir_path, 'input')
    output_dir_path = os.path.join(task_dir_path, 'output')

    task_meta = MetaDataHandler(os.path.join(task_dir_path, 'egor-meta.json'))
    task_meta.name = task_name
    task_meta.dir = task_dir_path

    # Create input/output directories
    os.makedirs(task_dir_path, exist_ok=True)
    os.makedirs(input_dir_path, exist_ok=True)
    os.makedirs(output_dir_path, exist_ok=True)
    task_meta.input_dir = input_dir_path
    task_meta.output_dir = output_dir_path
    task_meta.tests = []

    # Add tests
    for index, test in enumerate(task_object['tests']):
        test_input_path = os.path.join(
            input_dir_path, 'in-{}.in'.format(index + 1))
        test_output_path = os.path.join(
            output_dir_path, 'in-{}-expected.out'.format(index + 1))

        test_description = {
            'input_file': test_input_path,
            'output_file': test_output_path,
            'index': index + 1,
            'custom': False
        }
        task_meta.tests.append(test_description)

        with open(test_input_path, 'w') as input_file:
            logger.info('Creating file {}'.format(test_input_path))
            input_file.write(test['input'])
        with open(test_output_path, 'w') as output_file:
            logger.info('Creating file {}'.format(test_output_path))
            output_file.write(test['output'])


class TaskServer(BaseHTTPRequestHandler):

    def do_POST(self):
        task_description = self.rfile.read(
            int(self.headers['Content-Length'])).decode('ascii')

        create_task(task_description)


def start_server(port):
    with socketserver.TCPServer(('127.0.0.1', port), TaskServer) as httpd:
        httpd.handle_request()
        # We fire a last request at the server in order to take it out of the
        try:
            urllib3.urlopen(
                'http://%s:%s/' % (httpd.server_address[1], httpd.server_address[1]))
        except:
            # If the server is already shut down, we receive a socket error,
            # which we ignore.
            pass
        httpd.server_close()
    return task_meta
