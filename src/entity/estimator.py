import sys
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import MyException
from src.logger import logging


class TargetValueMapping:
    def __init__(self):
        # Conventional mapping: Yes -> 1, No -> 0
        self.yes: int = 1
        self.no: int = 0

    def _asdict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class MyModel:
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        """
        :param preprocessing_object: Pre-fitted sklearn Pipeline or transformer
        :param trained_model_object: Trained sklearn model
        """
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame) -> DataFrame:
        """
        Accepts raw input DataFrame, applies preprocessing transformations,
        and performs prediction using the trained model.
        Returns predictions as a pandas DataFrame.
        """
        try:
            logging.info("Starting prediction process.")

            # Step 1: Apply preprocessing / scaling transformations
            transformed_feature = self.preprocessing_object.transform(dataframe)

            # Step 2: Perform prediction
            logging.info("Using the trained model to get predictions")
            predictions = self.trained_model_object.predict(transformed_feature)

            # Return as DataFrame for consistency
            return pd.DataFrame(predictions, columns=["prediction"])

        except Exception as e:
            logging.error("Error occurred in predict method", exc_info=True)
            raise MyException(e, sys) from e

    def __repr__(self):
        return (f"MyModel(preprocessing_object={type(self.preprocessing_object).__name__}, "
                f"model={type(self.trained_model_object).__name__})")

    def __str__(self):
        return f"Trained Model: {type(self.trained_model_object).__name__}"
