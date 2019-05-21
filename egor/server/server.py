import json
import os
import socketserver
from http.server import BaseHTTPRequestHandler

import urllib3
from knack.log import get_logger

logger = get_logger(__name__)

task_meta = {}


def extract_name(task_name: str):
    return task_name.replace(' ', '').replace('.', '')


def create_task(task_description):
    """
    Creates the task's files and directories
    """
    task_object = json.loads(task_description)
    task_name = extract_name(task_object['name'])
    # setting the task name to be returned by the start_server method
    # so it cann be accessible outside of this module
    task_meta['name'] = task_name

    logger.info('Creating task {} ...'.format(task_name))
    cur_dir_path = os.path.abspath(os.path.curdir)
    task_dir_path = os.path.join(cur_dir_path, task_name)
    input_dir_path = os.path.join(task_dir_path, 'input')
    output_dir_path = os.path.join(task_dir_path, 'output')

    # Create input/output directories
    os.makedirs(task_dir_path, exist_ok=True)
    os.makedirs(input_dir_path, exist_ok=True)
    os.makedirs(output_dir_path, exist_ok=True)

    # Add tests
    for index, test in enumerate(task_object['tests']):
        test_input_name = os.path.join(
            input_dir_path, 'in-{}.in'.format(index + 1))
        test_output_name = os.path.join(
            output_dir_path, 'in-{}-expected.out'.format(index + 1))

        with open(test_input_name, 'w') as input_file:
            logger.info('Creating file {}'.format(test_input_name))
            input_file.write(test['input'])
        with open(test_output_name, 'w') as output_file:
            logger.info('Creating file {}'.format(test_output_name))
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
