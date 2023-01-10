from caddo_file_parser.models.index_set import IndexSet
import pandas as pd

from caddo_file_parser.settings.generation_settings import GenerationSettings


class CaddoFile:
    def __init__(self, index_sets: [IndexSet], data: pd.DataFrame, settings: GenerationSettings):
        self.index_sets = index_sets
        self.data = data
        self.settings = settings

