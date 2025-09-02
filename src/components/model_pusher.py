import sys
from src.cloud_storage.aws_storage import SimpleStorageService
from src.exception import MyException
from src.logger import logging
from src.entity.artifact_entity import ModelPusherArtifact, ModelEvaluationArtifact
from src.entity.config_entity import ModelPusherConfig
from src.entity.s3_estimator import Proj1Estimator


class ModelPusher:
    def __init__(self, model_evaluation_artifact: ModelEvaluationArtifact,
                 model_pusher_config: ModelPusherConfig):
        """
        :param model_evaluation_artifact: Output reference of data evaluation artifact stage
        :param model_pusher_config: Configuration for model pusher
        """
        self.s3 = SimpleStorageService()
        self.model_evaluation_artifact = model_evaluation_artifact
        self.model_pusher_config = model_pusher_config
        self.proj1_estimator = Proj1Estimator(
            bucket_name=model_pusher_config.bucket_name,
            model_path=model_pusher_config.s3_model_key_path
        )

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        """
        Upload trained model to S3 and return artifact details
        """
        logging.info("Entered initiate_model_pusher method of ModelPusher class")

        try:
            print("---------------------------------------------------------------")
            print(f"✅ Trained model local path: {self.model_evaluation_artifact.trained_model_path}")
            print(f"✅ Target bucket: {self.model_pusher_config.bucket_name}")
            print(f"✅ Target S3 key (model_path): {self.model_pusher_config.s3_model_key_path}")

            logging.info("Uploading new model to S3 bucket....")

            # Upload trained model file to S3
            self.proj1_estimator.save_model(
                from_file=self.model_evaluation_artifact.trained_model_path
            )

            model_pusher_artifact = ModelPusherArtifact(
                bucket_name=self.model_pusher_config.bucket_name,
                s3_model_path=self.model_pusher_config.s3_model_key_path
            )

            print(f"🎯 Model successfully uploaded to s3://{model_pusher_artifact.bucket_name}/"
                  f"{model_pusher_artifact.s3_model_path}")

            logging.info(f"Model pusher artifact: [{model_pusher_artifact}]")
            logging.info("Exited initiate_model_pusher method of ModelPusher class")

            return model_pusher_artifact

        except Exception as e:
            raise MyException(e, sys) from e
