from caddo_file_parser.models.fold import Fold
import pandas as pd

from caddo_file_parser.settings.generation_settings import GenerationSettings


class CaddoFile:
    def __init__(self, folds: [Fold], data: pd.DataFrame, settings: GenerationSettings):
        self.folds = folds
        self.data = data
        self.settings = settings

