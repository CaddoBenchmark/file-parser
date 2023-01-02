from models.fold import Fold
import pandas as pd


class CaddoFile:
    def __init__(self, folds: [Fold], data: pd.DataFrame, separator: str):
        self.folds = folds
        self.data = data
        self.separator = separator

