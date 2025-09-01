import sys
from pandas import DataFrame
from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.entity.estimator import MyModel


class Proj1Estimator:
    """
    Class to handle S3 model retrieval and prediction
    """
    def __init__(self, bucket_name: str, model_path: str):
        self.bucket_name = bucket_name
        self.model_path = model_path
        self.s3 = SimpleStorageService()
        self.loaded_model: MyModel = None

    def is_model_present(self, **kwargs) -> bool:
        """
        Check if model exists in S3
        Accepts keyword argument 'model_path'
        """
        try:
            model_path = kwargs.get("model_path", self.model_path)
            return self.s3.s3_key_path_available(bucket_name=self.bucket_name, s3_key=model_path)
        except MyException as e:
            print(e)
            return False

    def load_model(self) -> MyModel:
        """
        Load model from S3
        """
        try:
            loaded_obj = self.s3.load_model(self.model_path, bucket_name=self.bucket_name)
            if not isinstance(loaded_obj, MyModel):
                raise MyException(
                    f"Loaded object is not MyModel instance. Got {type(loaded_obj)} instead", sys
                )
            return loaded_obj
        except Exception as e:
            raise MyException(e, sys) from e

    def save_model(self, from_file: str, remove: bool = False) -> None:
        """
        Upload model file to S3
        """
        try:
            self.s3.upload_file(
                from_file,
                to_filename=self.model_path,
                bucket_name=self.bucket_name,
                remove=remove
            )
        except Exception as e:
            raise MyException(e, sys)

    def predict(self, dataframe: DataFrame):
        """
        Make prediction using loaded model
        """
        try:
            if self.loaded_model is None:
                self.loaded_model = self.load_model()
            return self.loaded_model.predict(dataframe=dataframe)
        except Exception as e:
            raise MyException(e, sys)