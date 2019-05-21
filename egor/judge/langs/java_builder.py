import os
import subprocess

from knack.log import get_logger

from egor.config import get_configuration_value
from egor.judge.builder import CompileStep, RunStep, CleanupStep

logger = get_logger(__name__)


class JavaCompileStep(CompileStep):
    """
    Compile cpp files.
    The binaries and compilation parameters, are fetched from configuration, either via command line or via config
    file
    """

    def execute(self, execution_context):
        java_executable = get_configuration_value('EGOR_JAVA_BIN', fallback='javac')
        target_file, target_directory = self.extract_target_paths(execution_context)
        work_directory = os.path.join(target_directory, 'work')
        os.makedirs(work_directory, exist_ok=True)
        java_flags = '-d work'
        logger.info('Compiling your source code ...')
        subprocess.call([java_executable, java_flags, target_file])

    @staticmethod
    def extract_target_paths(execution_context):
        return execution_context['target_file'], execution_context['target_directory']


class JavaRunStep(RunStep):

    def execute(self, execution_context):
        pass


class JavaCleanupStep(CleanupStep):

    def execute(self, execution_context):
        target_directory = execution_context['target_directory']
        work_directory = os.path.join(target_directory, 'work')
        os.rmdir(work_directory)
        logger.info('Cleanup work directory {}'.format(work_directory))
