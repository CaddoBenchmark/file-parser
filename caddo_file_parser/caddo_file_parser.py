import os
import zipfile
import io

from yaml import SafeLoader

from caddo_file_parser.models.caddo_file import CaddoFile
import pandas as pd
import yaml

from caddo_file_parser.models.fold import Fold
from caddo_file_parser.settings.generation_settings_loader import GenerationSettingsLoader


class Dumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(Dumper, self).increase_indent(flow, False)


class CaddoFileParser:

    def create_file(self, caddo_file: CaddoFile):
        self.save_data(caddo_file)
        self.save_folds(caddo_file)
        self.pack_to_caddo_file(caddo_file)
        self.remove_unused_file(caddo_file)

    def save_data(self, caddo_file):
        pd.DataFrame(caddo_file.data).to_csv(
            "data.csv",
            sep=caddo_file.settings.data_output_file_separator,
            index=False
        )

    def save_folds(self, caddo_file):
        for fold in caddo_file.folds:
            fold_number = fold.number
            train_indexes = fold.train_indexes
            test_indexes = fold.test_indexes
            seed = fold.seed
            file_content = {
                "number": fold_number,
                "train_indexes": train_indexes,
                "test_indexes": test_indexes,
                "seed": seed
            }
            with open(f"fold_{fold_number}.yaml", 'w') as file:
                yaml.dump(file_content, file, Dumper=Dumper, default_flow_style=False)

    def pack_to_caddo_file(self, caddo_file):
        filenames = [f"fold_{fold.number}.yaml" for fold in caddo_file.folds] + ["data.csv"] + ["settings.yaml"]
        with zipfile.ZipFile(f"{caddo_file.settings.data_output_file_name}.caddo", "w") as archive:
            for filename in filenames:
                archive.write(filename)

    def remove_unused_file(self, caddo_file):
        filenames = [f"fold_{fold.number}.yaml" for fold in caddo_file.folds] + ["data.csv"]
        for file in filenames:
            os.remove(file)

    def read_data(self, file_name) -> CaddoFile:

        with zipfile.ZipFile(file_name + ".caddo", "r") as zf:
            generation_settings = self.read_settings(zf)
            data = self.read_csv_data(zf, generation_settings)
            folds = self.read_folds(zf, generation_settings)
        caddo_file: CaddoFile = CaddoFile(folds, data, generation_settings)
        return caddo_file

    def read_settings(self, zf):
        settings_file = zf.read("settings.yaml").decode(encoding="utf-8")
        settings_yaml = yaml.load(settings_file, Loader=SafeLoader)
        return GenerationSettingsLoader().load_settings_object(settings_yaml)

    def read_csv_data(self, zf, generation_settings):
        separator = generation_settings.data_output_file_separator
        data_csv = zf.read("data.csv").decode(encoding="utf-8")
        return pd.read_csv(io.StringIO(data_csv), sep=separator)

    def read_folds(self, zf, generation_settings):
        folds = []
        runs = generation_settings.data_splitting_folding_runs
        for i in range(runs):
            file = zf.read(f"fold_{i}.yaml").decode(encoding="utf-8")
            data: Fold = yaml.load(file, Loader=SafeLoader)
            folds.append(data)
        return folds