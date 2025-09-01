import sys
from pandas import DataFrame
from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import MyModel


class Proj1Estimator:
    """
    This class is used to save and retrieve our model from S3 and do predictions
    """

    def __init__(self, bucket_name: str, model_path: str):
        try:
            self.bucket_name = bucket_name
            self.model_path = model_path
            self.s3 = SimpleStorageService()
            self.loaded_model: MyModel = None
        except Exception as e:
            raise MyException(e, sys) from e

    def is_model_present(self) -> bool:
        """Check if model exists in S3"""
        try:
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=self.model_path)
        except Exception as e:
            raise MyException(e, sys) from e

    def load_model(self) -> MyModel:
        """Load the model from S3"""
        try:
            if self.loaded_model is None:
                self.loaded_model = self.s3.load_model(model_path=self.model_path, bucket_name=self.bucket_name)
            return self.loaded_model
        except Exception as e:
            raise MyException(e, sys) from e

    def save_model(self, from_file: str, remove: bool = False) -> None:
        """Upload a local model file to S3"""
        try:
            self.s3.upload_file(from_file=from_file, to_filename=self.model_path,
                                bucket_name=self.bucket_name, remove=remove)
        except Exception as e:
            raise MyException(e, sys) from e

    def predict(self, dataframe: DataFrame):
        """Predict using the loaded model"""
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe)
        except Exception as e:
            raise MyException(e, sys) from e
