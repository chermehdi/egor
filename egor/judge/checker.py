import os

from egor.util import extract_test_number_from_filename, DIFFERENT_OUTPUT_CONTENT_TEMPLATE, \
    DIFFERENT_OUTPUT_LENGTH_TEMPLATE, PASSED_TEST_CASE


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
        target_directory = execution_context['target_directory']
        output_directory = os.path.join(target_directory, 'output')

        # We might want to skip comparing some files because they timed out or they just don't exist
        skipped_file_names = execution_context['skipped_file_names']

        output_files = os.listdir(output_directory)

        judge_output = sorted(list(filter(lambda file: 'expected' in file, output_files)))

        contestant_output = sorted(list(filter(lambda file: 'expected' not in file, output_files)))

        diff = {}

        for index, test_case in enumerate(zip(contestant_output, judge_output)):
            c_file, j_file = test_case
            c_file, j_file = os.path.join(output_directory, c_file), os.path.join(output_directory, j_file)
            # todo: add a more convenient diffing
            test_number = extract_test_number_from_filename(c_file)
            diff[test_number] = self.compare(c_file, j_file, test_number)
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
            for index, line_pair in enumerate(zip(expected_output, output)):
                if line_pair[0] != line_pair[1]:
                    return DIFFERENT_OUTPUT_CONTENT_TEMPLATE.format(index + 1, line_pair[0], line_pair[1])
            return PASSED_TEST_CASE.format(test_number)
