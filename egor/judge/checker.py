import os

from egor.util import DIFFERENT_OUTPUT_CONTENT_TEMPLATE, \
    DIFFERENT_OUTPUT_LENGTH_TEMPLATE, PASSED_TEST_CASE, SKIPPED_TEST_CASE


class Checker:
    """
    Checker that compares generated output against the expected one, following customizable rules, such as comparing
    line by line comparison, ignore spaces, compare values with a delta, validating the expected output against a custom
    logic ...
    """

    def check(self, execution_context):
        """
        Check generated output files for correctness.
        :param execution_context: dictionary of all current execution parameters
        :return: dictionary of the results
        """
        task_meta = execution_context['meta']

        # We might want to skip comparing some files because they timed out or they just don't exist
        skipped_file_names = execution_context['skipped_file_names']

        diff = {}

        for test_description in task_meta.tests:
            test_index, test_expected_output_path = test_description['index'], test_description['output_file']
            contestant_output_path = os.path.join(task_meta.output_dir, 'in-{}.out'.format(test_index))
            if test_description['custom']:
                if test_expected_output_path == '':
                    diff[test_index] = SKIPPED_TEST_CASE.format(test_index)
                    continue
            diff[test_index] = self.compare(contestant_output_path, test_expected_output_path, test_index)

        return diff

    def compare(self, file_1, file2, test_number):
        """
        Compares the content of two files.
        Implementation is dependent on the type of data that we are trying to compare, either precision comparison,
        line by line comparison, should we skip spaces or not...

        :param test_number: Number of the current test case
        :param file_1: judge's output file
        :param file2:  contestant's output file
        :return: True if the files content's can be considered equal, False otherwise
        """
        raise NotImplementedError()


class BasicChecker(Checker):
    """
    Simple line by line checker, two files are different if their content is different by any character, even
    white spaces
    :return Message representing the state of the comparison
    """

    def compare(self, output, expected, test_number) -> str:
        with open(output) as out_f, open(expected) as ex_file:
            output = out_f.readlines()
            expected_output = ex_file.readlines()
            if len(output) != len(expected_output):
                return DIFFERENT_OUTPUT_LENGTH_TEMPLATE.format(len(expected_output), len(output))

            while len(output) and output[len(output) - 1].strip() == '':
                output.pop()
            while len(expected_output) and output[len(expected_output) - 1].strip() == '':
                expected_output.pop()

            for index, line_pair in enumerate(zip(expected_output, output)):
                if line_pair[0].strip() != line_pair[1].strip():
                    return DIFFERENT_OUTPUT_CONTENT_TEMPLATE.format(index + 1, line_pair[0], line_pair[1])
            return PASSED_TEST_CASE.format(test_number)
