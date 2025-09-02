import boto3
from src.configuration.aws_connection import S3Client
from io import StringIO
from typing import Union, List
import os, sys
from src.logger import logging
from mypy_boto3_s3.service_resource import Bucket
from src.exception import MyException
from botocore.exceptions import ClientError
from pandas import DataFrame, read_csv
import pickle


class SimpleStorageService:
    """
    A class for interacting with AWS S3 storage, providing methods for file management, 
    data uploads, and data retrieval in S3 buckets.
    """

    def __init__(self):
        try:
            s3_client = S3Client()
            self.s3_resource = s3_client.s3_resource
            self.s3_client = s3_client.s3_client
        except Exception as e:
            raise MyException(e, sys)

    def s3_key_path_available(self, bucket_name, s3_key) -> bool:
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=s3_key)]
            return len(file_objects) > 0
        except Exception as e:
            raise MyException(e, sys)

    @staticmethod
    def read_object(object_name: object, decode: bool = True, make_readable: bool = False) -> Union[StringIO, str]:
        """
        Reads the specified S3 object with optional decoding and formatting.
        """
        try:
            if isinstance(object_name, list):  # ✅ Handle list case
                logging.debug(f"[DEBUG] read_object received a LIST with {len(object_name)} items.")
                object_name = object_name[0]

            logging.debug(f"[DEBUG] Reading object: {object_name}")

            body = object_name.get()["Body"].read()
            data = body.decode() if decode else body
            return StringIO(data) if make_readable else data
        except Exception as e:
            logging.error(f"[ERROR] Failed to read S3 object: {object_name} | Error: {e}")
            raise MyException(e, sys) from e

    def get_bucket(self, bucket_name: str) -> Bucket:
        try:
            bucket = self.s3_resource.Bucket(bucket_name)
            return bucket
        except Exception as e:
            raise MyException(e, sys) from e

    def get_file_object(self, filename: str, bucket_name: str) -> object:
        """
        Always return a SINGLE object (first match).
        """
        try:
            bucket = self.get_bucket(bucket_name)
            file_objects = [file_object for file_object in bucket.objects.filter(Prefix=filename)]

            logging.debug(f"[DEBUG] get_file_object found {len(file_objects)} objects for prefix '{filename}'")

            if not file_objects:
                raise FileNotFoundError(f"No files found in bucket '{bucket_name}' with prefix '{filename}'")

            return file_objects[0]  # ✅ Always return first object
        except Exception as e:
            logging.error(f"[ERROR] Failed to get file object for {filename} in {bucket_name}: {e}")
            raise MyException(e, sys) from e

    def load_model(self, model_name: str, bucket_name: str, model_dir: str = None) -> object:
        try:
            model_file = model_dir + "/" + model_name if model_dir else model_name
            logging.debug(f"[DEBUG] Loading model: {model_file} from bucket {bucket_name}")
            file_object = self.get_file_object(model_file, bucket_name)
            model_obj = self.read_object(file_object, decode=False)
            model = pickle.loads(model_obj)
            logging.info("✅ Production model loaded from S3 bucket.")
            return model
        except Exception as e:
            logging.error(f"[ERROR] Failed to load model {model_name} from {bucket_name}: {e}")
            raise MyException(e, sys) from e

    def create_folder(self, folder_name: str, bucket_name: str) -> None:
        try:
            self.s3_resource.Object(bucket_name, folder_name).load()
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                folder_obj = folder_name + "/"
                self.s3_client.put_object(Bucket=bucket_name, Key=folder_obj)
            logging.info(f"✅ Folder created: {folder_name}/ in {bucket_name}")

    def upload_file(self, from_filename: str, to_filename: str, bucket_name: str, remove: bool = True):
        try:
            logging.debug(f"[DEBUG] Uploading {from_filename} → s3://{bucket_name}/{to_filename}")
            self.s3_resource.meta.client.upload_file(from_filename, bucket_name, to_filename)
            if remove:
                os.remove(from_filename)
                logging.debug(f"[DEBUG] Local file {from_filename} removed after upload")
        except Exception as e:
            logging.error(f"[ERROR] Failed to upload {from_filename} to {bucket_name}: {e}")
            raise MyException(e, sys) from e

    def upload_df_as_csv(self, data_frame: DataFrame, local_filename: str, bucket_filename: str, bucket_name: str) -> None:
        try:
            data_frame.to_csv(local_filename, index=None, header=True)
            self.upload_file(local_filename, bucket_filename, bucket_name)
            logging.info(f"✅ DataFrame uploaded as CSV to s3://{bucket_name}/{bucket_filename}")
        except Exception as e:
            logging.error(f"[ERROR] Failed to upload DataFrame to {bucket_name}: {e}")
            raise MyException(e, sys) from e

    def get_df_from_object(self, object_: object) -> DataFrame:
        try:
            content = self.read_object(object_, make_readable=True)
            df = read_csv(content, na_values="na")
            logging.debug(f"[DEBUG] DataFrame loaded with shape {df.shape}")
            return df
        except Exception as e:
            logging.error(f"[ERROR] Failed to convert object to DataFrame: {e}")
            raise MyException(e, sys) from e

    def read_csv(self, filename: str, bucket_name: str) -> DataFrame:
        try:
            logging.debug(f"[DEBUG] Reading CSV {filename} from bucket {bucket_name}")
            csv_obj = self.get_file_object(filename, bucket_name)
            df = self.get_df_from_object(csv_obj)
            return df
        except Exception as e:
            logging.error(f"[ERROR] Failed to read CSV {filename} from {bucket_name}: {e}")
            raise MyException(e, sys) from e
