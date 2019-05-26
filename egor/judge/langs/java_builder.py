import os
import shutil
import subprocess
import sys
from time import time

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
        task_meta = execution_context['meta']

        java_executable = get_configuration_value('EGOR_JAVA_COMPILER', fallback='javac')
        target_file, target_directory = task_meta.source_file, task_meta.dir
        work_directory = os.path.join(target_directory, 'work')
        os.makedirs(work_directory, exist_ok=True)
        java_flags = '-d {}'.format(work_directory).split(' ')
        if subprocess.call([java_executable, *java_flags, target_file]) != 0:
            logger.error('Could not compile your code ')
            sys.exit(-1)

        execution_context['work_directory'] = work_directory

        return execution_context


class JavaRunStep(RunStep):

    def execute(self, execution_context):
        logger.info('Running your code ...')
        task_meta = execution_context['meta']
        work_dir = execution_context['work_directory']

        run_report = {}

        for test_description in task_meta.tests:
            test_input_path, test_index = test_description['input_file'], test_description['index']
            test_output_path = os.path.join(task_meta.output_dir, 'in-{}.out'.format(test_index))
            run_report[test_index] = {
                'time_out': False,
                'skipped': False
            }
            with open(test_input_path) as in_f, open(test_output_path, "w") as out_f:
                logger.info('Running your code against input file {}'.format(test_index))
                # maybe we add a dynamic way to determine the main class
                start_time = time()
                try:
                    return_code = subprocess.call(['java', 'Main'], stdin=in_f, stdout=out_f,
                                                  cwd=work_dir, timeout=task_meta.time_limit / 1000.0)
                    if return_code != 0:
                        logger.error('execution on file {} finished with a none 0 exist code'.format(test_index))
                    execution_time = time() - start_time
                    run_report[test_index]['execution_time'] = execution_time
                except subprocess.TimeoutExpired:
                    logger.info('execution of file {} timed out'.format(test_index))
                    run_report[test_index]['time_out'] = True

        execution_context['run_report'] = run_report

        return execution_context


class JavaCleanupStep(CleanupStep):

    def execute(self, execution_context):
        task_meta = execution_context['meta']
        work_directory = os.path.join(task_meta.dir, 'work')
        shutil.rmtree(work_directory)
        logger.info('Cleanup work directory {}'.format(work_directory))
        return execution_context
