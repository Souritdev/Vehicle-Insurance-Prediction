import boto3
import os, sys, pickle
from io import StringIO
from typing import Union, List, Optional
from pandas import DataFrame, read_csv
from botocore.exceptions import ClientError
from mypy_boto3_s3.service_resource import Bucket

from src.configuration.aws_connection import S3Client
from src.logger import logging
from src.exception import MyException


class SimpleStorageService:
    """
    A utility class for interacting with AWS S3 storage.
    Provides file management, data uploads, and retrieval methods.
    """

    def __init__(self):
        try:
            s3_client = S3Client()
            self.s3_resource = s3_client.s3_resource
            self.s3_client = s3_client.s3_client
        except Exception as e:
            raise MyException(e, sys)

    def s3_key_path_available(self, bucket_name: str, s3_key: str) -> bool:
        """
        Check if a given key/prefix exists in the S3 bucket.
        """
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = list(bucket.objects.filter(Prefix=s3_key))
            return len(file_objects) > 0
        except Exception as e:
            raise MyException(e, sys)

    @staticmethod
    def read_object(
        object_name: object,
        decode: bool = True,
        make_readable: bool = False
    ) -> Union[StringIO, str, bytes]:
        """
        Reads the specified S3 object with optional decoding and formatting.
        :param object_name: boto3 ObjectSummary or list with one ObjectSummary
        :param decode: Whether to decode bytes to string
        :param make_readable: Whether to return as StringIO for pandas
        """
        try:
            if isinstance(object_name, list):
                logging.debug(f"[DEBUG] read_object received LIST, using first element.")
                object_name = object_name[0]

            logging.debug(f"[DEBUG] Reading object: {object_name.key}")
            body = object_name.get()["Body"].read()

            if decode:
                body = body.decode()

            return StringIO(body) if make_readable else body
        except Exception as e:
            logging.error(f"[ERROR] Failed to read S3 object {object_name}: {e}")
            raise MyException(e, sys) from e

    def get_bucket(self, bucket_name: str) -> Bucket:
        try:
            return self.s3_resource.Bucket(bucket_name)
        except Exception as e:
            raise MyException(e, sys) from e

    def get_file_object(self, filename: str, bucket_name: str) -> object:
        """
        Return the first matching file object from S3 bucket for a given prefix.
        """
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = list(bucket.objects.filter(Prefix=filename))

            if not file_objects:
                raise FileNotFoundError(f"No files found in {bucket_name} with prefix '{filename}'")

            if len(file_objects) > 1:
                logging.warning(f"[WARN] Multiple files found for prefix '{filename}', returning first match.")

            return file_objects[0]
        except Exception as e:
            raise MyException(e, sys) from e

    def load_model(self, model_name: str, bucket_name: str, model_dir: Optional[str] = None) -> object:
        """
        Load a pickled model from S3.
        WARNING: Only use with trusted sources (pickle is unsafe otherwise).
        """
        try:
            model_file = f"{model_dir}/{model_name}" if model_dir else model_name
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            model = pickle.loads(model_obj)
            logging.info(f"✅ Model '{model_name}' loaded from s3://{bucket_name}/{model_file}")
            return model
        except Exception as e:
            raise MyException(e, sys) from e

    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        """
        Create a "folder" (zero-size key ending with "/") in the S3 bucket.
        """
        try:
            folder_obj = folder_name.rstrip("/") + "/"
            self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            logging.info(f"✅ Folder ensured: s3://{bucket_name}/{folder_obj}")
        except Exception as e:
            raise MyException(e, sys) from e

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = False) -> None:
        """
        Upload a local file to S3.
        :param remove: If True, remove local file after upload
        """
        try:
            logging.debug(f"[DEBUG] Uploading {from_filename} → s3://{bucket_name}/{to_filename}")
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            if remove and os.path.exists(from_filename):
                os.remove(from_filename)
                logging.debug(f"[DEBUG] Local file {from_filename} removed after upload")
        except Exception as e:
            raise MyException(e, sys) from e

    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        """
        Save a DataFrame locally as CSV, then upload it to S3.
        """
        try:
            data_frame.to_csv(local_filename, index=False, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
            logging.info(f"✅ DataFrame uploaded as CSV → s3://{bucket_name}/{bucket_filename}")
        except Exception as e:
            raise MyException(e, sys) from e

    def get_df_from_object(self, object_: object) -> DataFrame:
        """
        Convert an S3 object into a pandas DataFrame.
        """
        try:
            content = self.read_object(object_, make_readable=True)
            df = read_csv(content, na_values="na")
            logging.debug(f"[DEBUG] DataFrame loaded with shape {df.shape}")
            return df
        except Exception as e:
            raise MyException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        """
        Read a CSV file from S3 into a pandas DataFrame.
        """
        try:
            csv_obj = self.get_file_object(filename, bucket_name)
            return self.get_df_from_object(csv_obj)
        except Exception as e:
            raise MyException(e, sys) from e
