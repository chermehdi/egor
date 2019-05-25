import json
import os

from knack.log import get_logger

logger = get_logger(__name__)


class MetaDataHandler:
    """
    Facade for operations specific to meta data file
    The task meta data will contain the following attributes
    - name: the task name / directory name
    - tests: an array with all the tests associated with the task
    - source_file: the path to the source file of the test
    - lang: the language to be used to run the test
    - input_dir: path to the input directory
    - output_dir: path to the output directory
    """

    def __init__(self, file_path, exists=False):
        self.file_path = file_path
        if exists:
            meta_data = self.load()
            for key in meta_data.keys():
                self.__setattr__(key, meta_data[key])

    def load(self) -> dict:
        """
        Loads and parses the meta data from the file
        :return: dictionary of meta data
        """
        if not os.path.exists(self.file_path):
            logger.error('Could not find meta file {}'.format(self.file_path))
            raise Exception()
        with open(self.file_path, encoding='utf-8') as meta_file:
            return json.loads(meta_file.read())

    def persist(self) -> None:
        """
        Saves the in memory representation of meta data into the original file
        :return: None
        """
        logger.info('Generating or Updating meta data file {}'.format(self.file_path))
        with open(self.file_path, 'w', encoding='utf-8') as meta_file:
            meta_file.write(json.dumps(self, default=lambda value: value.__dict__))

    def __setattr__(self, key, value) -> None:
        self.__dict__[key] = value

    def __getattr__(self, key):
        # todo: return default values instead of raising errors
        return self.__dict__[key]
