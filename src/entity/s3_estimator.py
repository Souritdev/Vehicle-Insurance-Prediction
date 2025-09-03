import sys
from typing import Optional
from pandas import DataFrame

from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import MyModel
from src.logger import logging


class Proj1Estimator:
    """
    Wrapper class to save, load, and use ML models stored in an S3 bucket.
    """

    def __init__(self, bucket_name: str, model_path: str):
        """
        :param bucket_name: Name of your S3 bucket
        :param model_path: Path (key) of the model file in the bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: Optional[MyModel] = None

    def is_model_present(self, model_path: str) -> bool:
        """
        Check if the model exists in S3.
        """
        try:
            return self.s3.s3_key_path_available(
                bucket_name=self.bucket_name,
                s3_key=model_path
            )
        except MyException as e:
            logging.error(f"Error while checking model in S3: {e}")
            return False

    def load_model(self) -> MyModel:
        """
        Load the model from S3 and store it in memory.
        """
        try:
            logging.info(f"Loading model from S3: {self.bucket_name}/{self.model_path}")
            self.loaded_model = self.s3.load_model(
                self.model_path,
                bucket_name=self.bucket_name
            )
            return self.loaded_model
        except Exception as e:
            raise MyException(e, sys)

    def save_model(self, from_file: str, remove: bool = False) -> None:
        """
        Upload a local model file to S3.
        :param from_file: Path to local model file
        :param remove: If True, delete local file after upload
        """
        try:
            logging.info(f"Saving model to S3: {self.bucket_name}/{self.model_path}")
            self.s3.upload_file(
                from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove
            )
        except Exception as e:
            raise MyException(e, sys)

    def predict(self, dataframe: DataFrame) -> DataFrame:
        """
        Run predictions using the loaded model. Loads model from S3 if not already in memory.
        :param dataframe: Input features as pandas DataFrame
        :return: Predictions as a pandas DataFrame
        """
        try:
            if self.loaded_model is None:
                logging.info("Model not loaded in memory. Loading now...")
                self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise MyException(e, sys)
