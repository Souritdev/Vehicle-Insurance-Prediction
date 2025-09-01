import sys
import pandas as pd
from pandas import DataFrame
from sklearn.pipeline import Pipeline

from src.exception import MyException
from src.logger import logging


class TargetValueMapping:
    def __init__(self):
        self.yes: int = 0
        self.no: int = 1

    def _asdict(self):
        return self.__dict__

    def reverse_mapping(self):
        mapping_response = self._asdict()
        return dict(zip(mapping_response.values(), mapping_response.keys()))


class MyModel:
    """
    Wrapper class for trained model and preprocessing pipeline
    """
    def __init__(self, preprocessing_object: Pipeline, trained_model_object: object):
        self.preprocessing_object = preprocessing_object
        self.trained_model_object = trained_model_object

    def predict(self, dataframe: pd.DataFrame) -> DataFrame:
        try:
            logging.info("Starting prediction process.")

            if not isinstance(self.preprocessing_object, Pipeline):
                raise MyException("preprocessing_object is not a valid sklearn Pipeline", sys)

            # Apply preprocessing transformations
            transformed_features = self.preprocessing_object.transform(dataframe)

            # Make predictions
            logging.info("Using the trained model to get predictions")
            predictions = self.trained_model_object.predict(transformed_features)
            return predictions

        except Exception as e:
            logging.error("Error occurred in predict method", exc_info=True)
            raise MyException(e, sys) from e

    def __repr__(self):
        return f"{type(self.trained_model_object).__name__}()"

    def __str__(self):
        return f"{type(self.trained_model_object).__name__}()"
