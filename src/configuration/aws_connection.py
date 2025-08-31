import boto3
import os
from src.constants import AWS_SECRET_ACCESS_KEY_ENV_KEY, AWS_ACCESS_KEY_ID_ENV_KEY, REGION_NAME


class S3Client:
    s3_client = None
    s3_resource = None

    def __init__(self, region_name=REGION_NAME):
        """
        This Class gets AWS credentials from environment variables 
        and creates a connection with S3 bucket. 
        Raises exception if any environment variable is missing.
        """

        if S3Client.s3_resource is None or S3Client.s3_client is None:
            __access_key_id = os.getenv(AWS_ACCESS_KEY_ID_ENV_KEY)
            __secret_access_key = os.getenv(AWS_SECRET_ACCESS_KEY_ENV_KEY)

            if not __access_key_id:
                raise Exception(f"❌ Environment variable {AWS_ACCESS_KEY_ID_ENV_KEY} is not set.")
            if not __secret_access_key:
                raise Exception(f"❌ Environment variable {AWS_SECRET_ACCESS_KEY_ENV_KEY} is not set.")

            # Initialize boto3 clients
            S3Client.s3_resource = boto3.resource(
                's3',
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name
            )
            S3Client.s3_client = boto3.client(
                's3',
                aws_access_key_id=__access_key_id,
                aws_secret_access_key=__secret_access_key,
                region_name=region_name
            )

        self.s3_resource = S3Client.s3_resource
        self.s3_client = S3Client.s3_client
