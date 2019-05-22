import os
import shutil
import subprocess
import sys

from knack.log import get_logger

from egor.config import get_configuration_value
from egor.judge.builder import CompileStep, RunStep, CleanupStep

logger = get_logger(__name__)


def extract_target_paths(execution_context):
    return execution_context['target_file'], execution_context['target_directory']


class JavaCompileStep(CompileStep):
    """
    Compile cpp files.
    The binaries and compilation parameters, are fetched from configuration, either via command line or via config
    file
    :return The modified execution context
    """

    def execute(self, execution_context):
        logger.info('Compiling your source code ...')

        java_executable = get_configuration_value('EGOR_JAVA_COMPILER', fallback='javac')
        target_file, target_directory = extract_target_paths(execution_context)
        work_directory = os.path.join(target_directory, 'work')
        os.makedirs(work_directory, exist_ok=True)
        java_flags = '-d work'.split(' ')
        if subprocess.call([java_executable, *java_flags, target_file]) != 0:
            logger.error('Could not compile your code ')
            sys.exit(-1)

        execution_context['work_directory'] = work_directory

        return execution_context


class JavaRunStep(RunStep):

    def execute(self, execution_context):
        logger.info('Running your code ...')
        work_dir = execution_context['work_directory']
        task_file, task_directory = extract_target_paths(execution_context)
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
                return_code = subprocess.call(['java', 'Main'], stdin=in_f, stdout=out_f,
                                              cwd=work_dir)
                if return_code != 0:
                    skipped_file_names.append(str(input_number))
                    logger.error('execution on file {} finished with a none 0 exist code'.format(input_file))

        execution_context['skipped_file_names'] = skipped_file_names

        return execution_context


class JavaCleanupStep(CleanupStep):

    def execute(self, execution_context):
        target_directory = execution_context['target_directory']
        work_directory = os.path.join(target_directory, 'work')
        shutil.rmtree(work_directory)
        logger.info('Cleanup work directory {}'.format(work_directory))

        return execution_context
