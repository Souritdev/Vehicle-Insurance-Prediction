import boto3
from io import BytesIO, StringIO
import os
import sys
import pickle
from pandas import DataFrame, read_csv
from botocore.exceptions import ClientError
from mypy_boto3_s3.service_resource import Bucket

from src.exception import MyException
from src.logger import logging
from src.configuration.aws_connection import S3Client


class SimpleStorageService:
    """
    Class to interact with AWS S3 storage for uploading, downloading, and deleting files.
    """

    def __init__(self):
        s3_client = S3Client()
        self.s3_resource = s3_client.s3_resource
        self.s3_client = s3_client.s3_client

    def s3_key_path_available(self, bucket_name, s3_key) -> bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            return len(file_objects) > 0
        except Exception as e:
            raise MyException(e, sys)

    def get_bucket(self, bucket_name: str) -> Bucket:
        try:
            return self.s3_resource.Bucket(bucket_name)
        except Exception as e:
            raise MyException(e, sys)

    def get_file_object(self, filename: str, bucket_name: str):
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [obj for obj in bucket.objects.filter(Prefix=filename)]
            if len(file_objects) == 0:
                raise FileNotFoundError(f"{filename} not found in bucket {bucket_name}")
            return file_objects[0]
        except Exception as e:
            raise MyException(e, sys)

    def read_object(self, s3_object, decode=True, make_readable=False):
        try:
            body = s3_object.get()["Body"].read()
            if decode:
                body = body.decode()
            if make_readable:
                return StringIO(body)
            return body
        except Exception as e:
            raise MyException(e, sys)

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        try:
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            if remove:
                os.remove(from_filename)
        except Exception as e:
            raise MyException(e, sys)

    def load_model(self, model_name: str, bucket_name: str):
        """
        Load a pickled MyModel object from S3
        """
        try:
            file_obj = self.get_file_object(model_name, bucket_name)
            model_bytes = self.read_object(file_obj, decode=False)
            model = pickle.loads(model_bytes)
            logging.info(f"Model {model_name} loaded from S3 bucket {bucket_name}")
            return model
        except Exception as e:
            raise MyException(e, sys)
