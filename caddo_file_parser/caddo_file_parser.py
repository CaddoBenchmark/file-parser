import os
import zipfile

from models.caddo_file import CaddoFile
import pandas as pd
import yaml


class CaddoFileParser:
    def create_file(self, caddo_file: CaddoFile, file_name):
        self.save_data(caddo_file)
        self.save_folds(caddo_file)
        self.pack_to_caddo_file(caddo_file, file_name)
        self.remove_unused_file(caddo_file)

    def save_data(self, caddo_file):
        pd.DataFrame(caddo_file.data).to_csv(
            "data.csv",
            sep=caddo_file.separator,
            index=False
        )

    def save_folds(self, caddo_file):
        for fold in caddo_file.folds:
            fold_number = fold.number
            train_indexes = fold.train_indexes
            test_indexes = fold.test_indexes
            file_content = {
                "number": fold_number,
                "train_indexes": train_indexes,
                "test_indexes": test_indexes
            }
            with open(f"fold_{fold_number}", 'w') as file:
                yaml.dump(file_content, file)

    def pack_to_caddo_file(self, caddo_file, file_name):
        filenames = [f"fold_{fold.number}.yaml" for fold in caddo_file.folds] + ["data.csv"]
        with zipfile.ZipFile(f"{file_name}.caddo", mode="w") as archive:
            for filename in filenames:
                archive.write(filename)

    def remove_unused_file(self, caddo_file):
        filenames = [f"fold_{fold.number}.yaml" for fold in caddo_file.folds] + ["data.csv"]
        for file in filenames:
            os.remove(file)

    def read_data(self, file_name) -> CaddoFile:
        

        