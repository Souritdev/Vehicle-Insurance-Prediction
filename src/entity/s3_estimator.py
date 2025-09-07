import sys
import pickle
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
        :param model_path: Full path (key) of the model file in the bucket
        """
        self.bucket_name = bucket_name
        self.s3 = SimpleStorageService()
        self.model_path = model_path
        self.loaded_model: Optional[MyModel] = None

    def is_model_present(self, model_path: Optional[str] = None) -> bool:
        """Check if the model exists in S3."""
        try:
            model_key = model_path or self.model_path
            exists = self.s3.s3_key_path_available(
                bucket_name=self.bucket_name,
                s3_key=model_key
            )
            logging.info(f"Model presence check for {model_key}: {exists}")
            return exists
        except Exception as e:
            logging.error(f"Error while checking model in S3: {e}")
            return False

    def load_model(self) -> MyModel:
        """Load and unpickle the model bundle from S3, wrap into MyModel."""
        try:
            logging.info(f"Loading model from S3: s3://{self.bucket_name}/{self.model_path}")

            local_path = self.s3.download_file(
                from_filename=self.model_path,
                bucket_name=self.bucket_name
            )

            with open(local_path, "rb") as f:
                bundle = pickle.load(f)

            if not isinstance(bundle, dict) or "preprocessor" not in bundle or "model" not in bundle:
                raise ValueError(
                    f"Model bundle must be a dict with keys 'preprocessor' and 'model'. Got: {type(bundle)}"
                )

            self.loaded_model = MyModel(
                preprocessing_object=bundle["preprocessor"],
                trained_model_object=bundle["model"]
            )

            logging.info("Model successfully loaded into memory")
            return self.loaded_model

        except Exception as e:
            raise MyException(e, sys)

    def save_model(self, preprocessor=None, model=None, from_file: str = None, remove: bool = False) -> None:
        """
        Save model bundle (preprocessor + model) or upload an existing model file to S3.
        """
        try:
            if from_file:
                logging.info(f"Uploading local model file {from_file} to S3: s3://{self.bucket_name}/{self.model_path}")
                self.s3.upload_file(
                    from_filename=from_file,
                    to_filename=self.model_path,
                    bucket_name=self.bucket_name,
                    remove=remove
                )
            else:
                logging.info(f"Saving model bundle to S3: s3://{self.bucket_name}/{self.model_path}")
                bundle = {"preprocessor": preprocessor, "model": model}

                import tempfile
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pkl") as tmp:
                    pickle.dump(bundle, tmp)
                    tmp_path = tmp.name

                self.s3.upload_file(
                    from_filename=tmp_path,
                    to_filename=self.model_path,
                    bucket_name=self.bucket_name,
                    remove=True
                )

            logging.info("Model successfully uploaded to S3")

        except Exception as e:
            raise MyException(e, sys)

    def predict(self, dataframe: DataFrame):
        """Run predictions using the loaded model."""
        try:
            if self.loaded_model is None:
                logging.info("Model not loaded in memory. Loading now...")
                self.load_model()

            predictions = self.loaded_model.predict(dataframe=dataframe)
            logging.info(f"Predictions generated for {len(dataframe)} rows")
            return predictions

        except Exception as e:
            raise MyException(e, sys)
