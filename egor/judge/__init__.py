from .builder import ExecutionPipeline
from .builder import TestingStep
from .langs import JavaCompileStep, JavaRunStep, JavaCleanupStep, CppCompileStep, CppRunStep, \
    CppCleanupStep


def get_execution_context(task_meta):
    return {
        'meta': task_meta
    }


def execute_java_task(task_meta):
    execution_context = get_execution_context(task_meta)

    pipeline = ExecutionPipeline([
        JavaCompileStep(),
        JavaRunStep(),
        JavaCleanupStep(),
        TestingStep()
    ])

    pipeline.execute(execution_context)


def execute_cpp_task(task_meta):
    execution_context = get_execution_context(task_meta)

    pipeline = ExecutionPipeline([
        CppCompileStep(),
        CppRunStep(),
        CppCleanupStep(),
        TestingStep()
    ])

    pipeline.execute(execution_context)


def execute_python_task(task_meta):
    pass
