import unittest

import yaml
from pandas import DataFrame
from yaml import SafeLoader

from caddo_file_parser.caddo_file_parser import CaddoFileParser
from caddo_file_parser.models.caddo_file import CaddoFile
from caddo_file_parser.models.fold import Fold
from caddo_file_parser.settings.generation_settings import GenerationSettings
from caddo_file_parser.settings.generation_settings_loader import GenerationSettingsLoader


class FileSavingTest(unittest.TestCase):
    def test_save_caddo_file(self):
        caddo_file_parser = CaddoFileParser()
        caddo_file = self._create_caddo_file()
        caddo_file_parser.create_file(caddo_file)

    def _create_caddo_file(self):
        settings_loader = GenerationSettingsLoader()
        with open("settings.yaml", 'r') as file:
            settings = settings_loader.load_settings_object(yaml.load(file, Loader=SafeLoader))
            caddo_file = CaddoFile(
                folds=[
                    Fold(1, [1, 2, 3], [4, 5, 6], 10),
                    Fold(2, [7, 8, 9], [10, 11, 12], 12)
                ],
                data=DataFrame(
                    data=[[1, 2], [3, 4], [5, 6]],
                    columns=["col_A", "col_B"]
                ),
                settings=settings
            )
            return caddo_file
