from .builder import ExecutionPipeline
from .builder import TestingStep
from .langs import JavaCompileStep, JavaRunStep, JavaCleanupStep, CppCompileStep, CppRunStep, \
    CppCleanupStep


def get_execution_context(file_name, directory_path):
    return {
        'target_file': file_name,
        'target_directory': directory_path
    }


def execute_java_task(file_name, directory_path):
    execution_context = get_execution_context(file_name, directory_path)

    pipeline = ExecutionPipeline([
        JavaCompileStep(),
        JavaRunStep(),
        JavaCleanupStep(),
    ])

    pipeline.execute(execution_context)


def execute_cpp_task(file_name, directory_path):
    execution_context = get_execution_context(file_name, directory_path)

    pipeline = ExecutionPipeline([
        CppCompileStep(),
        CppRunStep(),
        CppCleanupStep(),
        TestingStep()
    ])

    pipeline.execute(execution_context)


def execute_python_task(file_name, directory_path):
    pass
