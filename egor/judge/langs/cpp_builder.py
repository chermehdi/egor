import os
import subprocess
import sys

from knack.log import get_logger

from egor.config import get_configuration_value
from egor.judge.builder import CompileStep, RunStep, CleanupStep

logger = get_logger(__name__)

# maybe make the binary name, same as lowercase task name
DEFAULT_BINARY_NAME = 'exec'


class CppCompileStep(CompileStep):
    """
    Compile cpp files.
    The binaries and compilation parameters, are fetched from configuration, either via command line or via config
    file
    """

    def execute(self, execution_context):
        task_meta = execution_context['meta']

        cpp_executable = get_configuration_value('EGOR_CPP_BIN', fallback='g++')
        target_file = task_meta.source_file
        cpp_flags = get_configuration_value('EGOR_CPP_FLAGS', fallback='-std=c++11 -Wall -O2 -o {}'
                                            .format(DEFAULT_BINARY_NAME)).split(' ')

        logger.info('Compiling your source code ...')

        return_code = subprocess.call([cpp_executable, *cpp_flags, target_file],
                                      cwd=task_meta.dir)

        if return_code != 0:
            logger.error('Could not compile the given file')
            sys.exit(-1)

        # Add the binary name for further customisation
        execution_context['binary_name'] = DEFAULT_BINARY_NAME
        return execution_context


class CppRunStep(RunStep):

    def execute(self, execution_context):
        task_meta = execution_context['meta']

        input_dir, output_dir = task_meta.input_dir, task_meta.output_dir

        executable = '{}.exe'.format(
            execution_context['binary_name']) if sys.platform == 'win32' else './{}'.format(
            execution_context['binary_name'])

        skipped_file_names = []

        for test_description in task_meta.tests:

            test_input_file, test_index = test_description['input_file'], test_description['index']
            test_output_file = os.path.join(output_dir, 'in-{}.out'.format(test_index))
            with open(test_input_file) as in_f, open(test_output_file, "w") as out_f:
                logger.info('Running your code against input file {}'.format(test_index))
                return_code = subprocess.call([executable], stdin=in_f, stdout=out_f, cwd=task_meta.dir)
                if return_code != 0:
                    skipped_file_names.append(str(test_index))
                    logger.error('execution on file {} finished with a none 0 exist code'.format(test_index))

        execution_context['skipped_file_names'] = skipped_file_names

        return execution_context


class CppCleanupStep(CleanupStep):

    def execute(self, execution_context):
        task_meta = execution_context['meta']
        binary = execution_context['binary_name']
        binary_path = os.path.join(task_meta.dir, binary)
        os.remove(binary_path)
        logger.info('Removed binary file {}'.format(binary_path))
        return execution_context
