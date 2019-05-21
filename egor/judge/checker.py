import os


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

        for index, test_case in enumerate(zip(judge_output, contestant_output)):
            c_file, j_file = test_case
            c_file, j_file = os.path.join(output_directory, c_file), os.path.join(output_directory, j_file)
            # todo: add a more convenient diffing
            if not self.compare(c_file, j_file):
                diff[index] = 'Different output'
        return diff

    def compare(self, file_1, file2):
        """
        Compares the content of two files.
        Implementation is dependent on the type of data that we are trying to compare, either precision comparison,
        line by line comparison, should we skip spaces or not...

        :param file_1: judge's output file
        :param file2:  contestant's output file
        :return: True if the files content's can be considered equal, False otherwise
        """
        raise NotImplementedError()


class BasicChecker(Checker):
    """
    Simple line by line checker, two files are different if their content is different by any character, even
    white spaces
    """

    def compare(self, file_1, file_2):
        with open(file_1) as f1, open(file_2) as f2:
            return f1.read() == f2.read()
