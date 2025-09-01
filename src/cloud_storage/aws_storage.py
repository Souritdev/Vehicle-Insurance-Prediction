import boto3
import pickle
import sys
from botocore.exceptions import ClientError
from src.exception import MyException
from src.logger import logging


class SimpleStorageService:
    def __init__(self):
        try:
            self.s3_client = boto3.client("s3")
        except Exception as e:
            raise MyException(e, sys) from e

    def s3_key_path_available(self, bucket_name: str, s3_key: str) -> bool:
        """
        Check if a specific object exists in S3
        """
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=s3_key)
            # response.get("Contents") can be None if key does not exist
            contents = response.get("Contents", [])
            if contents:
                logging.info(f"S3 key {s3_key} found in bucket {bucket_name}")
                return True
            logging.info(f"S3 key {s3_key} NOT found in bucket {bucket_name}")
            return False
        except ClientError as e:
            raise MyException(e, sys) from e

    def upload_file(self, from_file: str, to_filename: str, bucket_name: str, remove: bool = False) -> None:
        """
        Upload a local file to S3
        """
        try:
            self.s3_client.upload_file(Filename=from_file, Bucket=bucket_name, Key=to_filename)
            logging.info(f"Uploaded {from_file} to s3://{bucket_name}/{to_filename}")
            if remove:
                import os
                os.remove(from_file)
                logging.info(f"Removed local file: {from_file}")
        except Exception as e:
            raise MyException(e, sys) from e

    def load_model(self, model_path: str, bucket_name: str):
        """
        Load a pickled model from S3
        """
        try:
            import io
            logging.info(f"Loading model from s3://{bucket_name}/{model_path}")
            obj = self.s3_client.get_object(Bucket=bucket_name, Key=model_path)
            model_bytes = obj["Body"].read()
            model = pickle.loads(model_bytes)
            logging.info(f"Model loaded successfully from S3")
            return model
        except Exception as e:
            raise MyException(e, sys) from e
