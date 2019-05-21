import os
import subprocess
import sys

from knack.log import get_logger

from egor.config import get_configuration_value
from egor.judge.builder import CompileStep, RunStep, CleanupStep

logger = get_logger(__name__)

DEFAULT_BINARY_NAME = 'exec'


class CppCompileStep(CompileStep):
    """
    Compile cpp files.
    The binaries and compilation parameters, are fetched from configuration, either via command line or via config
    file
    """

    def execute(self, execution_context):
        cpp_executable = get_configuration_value('EGOR_CPP_BIN', fallback='g++')
        target_file = execution_context['target_file']
        cpp_flags = get_configuration_value('EGOR_CPP_FLAGS', fallback='-std=c++11 -Wall -O2 -o {}'
                                            .format(DEFAULT_BINARY_NAME)).split(' ')

        logger.info('Compiling your source code ...')

        return_code = subprocess.call([cpp_executable, *cpp_flags, target_file],
                                      cwd=execution_context['target_directory'])

        if return_code != 0:
            logger.erro('Could not compile the given file')
            sys.exit(-1)

        execution_context['binary_name'] = DEFAULT_BINARY_NAME
        return execution_context


class CppRunStep(RunStep):

    def execute(self, execution_context):
        task_directory = execution_context['target_directory']
        input_dir = os.path.join(task_directory, 'input')
        output_dir = os.path.join(task_directory, 'output')

        input_files = os.listdir(input_dir)

        skipped_file_names = []

        for input_file in input_files:
            # ugly code
            input_number = int(input_file.split('-')[1].split('.')[0])
            output_file_name = 'in-{}.out'.format(input_number)
            with open(os.path.join(input_dir, input_file), "r") as in_f, \
                    open(os.path.join(output_dir, output_file_name), "w") as out_f:
                logger.info('Running your code against input file {}'.format(input_file))
                return_code = subprocess.call(['./' + execution_context['binary_name']], stdin=in_f, stdout=out_f,
                                              cwd=task_directory)
                if return_code != 0:
                    skipped_file_names.append(str(input_number))
                    logger.error('execution on file {} finished with a none 0 exist code'.format(input_file))

        execution_context['skipped_file_names'] = skipped_file_names

        return execution_context


class CppCleanupStep(CleanupStep):

    def execute(self, execution_context):
        binary = execution_context['binary_name']
        binary_path = os.path.join(execution_context['target_directory'], binary)
        os.remove(binary_path)
        logger.info('Removed binary file {}'.format(binary_path))
        return execution_context
