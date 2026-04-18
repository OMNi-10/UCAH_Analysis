from smt.surrogate_models.surrogate_model import SurrogateModel
from smt.surrogate_models import krg

import numpy as np


class AeroModel:
    training_csv: str

    input_params: list[str] = []
    # output_params: list[str] = []
    surrogate_models: dict[str, type[SurrogateModel]] = {}

    def setTrainingCSV(self, csv_file: str):
        self.training_csv = csv_file

    def updateFit(self):
        X, Y = 0, 0



        for output_param in list(self.surrogate_models.keys()):
            sm: type[SurrogateModel] = self.surrogate_models[output_param]
            sm.set_training_values()

    def predict(self, input: np.ndarray) -> np.ndarray:
        """
        Takes in an input vector and returns the vector of predicted values.
        """

        output = []
        for sm in self.surrogate_models.values():
            output.append(sm.predict_values(input))
        return np.array(output)

    def predict_var(self, input: np.ndarray) -> np.ndarray:
        """
        Takes in an input vector and returns the vector of predicted variances.
        :param input:
        :return:
        """

        output = []
        for sm in self.surrogate_models.values():
            output.append(sm.predict_values(input))
        return np.array(output)


def csv_to_in_out(csv_path: str, input_params: list[str], output_params: list[str]):
    columns: dict[str, list] = {}

    inputs: dict[str, list] = {}
    outputs: dict[str, list] = {}
    for column_name in columns.keys():
        if column_name in input_params:
            inputs[column_name] = columns[column_name]
        elif column_name in output_params:
            outputs[column_name] = columns[column_name]