import sys
from pandas import DataFrame

from src.entity.config_entity import VehiclePredictorConfig
from src.entity.s3_estimator import Proj1Estimator
from src.exception import MyException
from src.logger import logging


class VehicleData:
    def __init__(self,
                 Gender,
                 Age,
                 Driving_License,
                 Region_Code,
                 Previously_Insured,
                 Annual_Premium,
                 Policy_Sales_Channel,
                 Vintage,
                 Vehicle_Age_lt_1_Year,
                 Vehicle_Age_gt_2_Years,
                 Vehicle_Damage_Yes):
        """
        Vehicle Data constructor
        Input: all features of the trained model for prediction
        """
        try:
            self.Gender = Gender
            self.Age = Age
            self.Driving_License = Driving_License
            self.Region_Code = Region_Code
            self.Previously_Insured = Previously_Insured
            self.Annual_Premium = Annual_Premium
            self.Policy_Sales_Channel = Policy_Sales_Channel
            self.Vintage = Vintage
            self.Vehicle_Age_lt_1_Year = Vehicle_Age_lt_1_Year
            self.Vehicle_Age_gt_2_Years = Vehicle_Age_gt_2_Years
            self.Vehicle_Damage_Yes = Vehicle_Damage_Yes

        except Exception as e:
            raise MyException(e, sys) from e

    def get_vehicle_input_data_frame(self) -> DataFrame:
        """
        Returns a DataFrame containing the input vehicle data
        """
        try:
            vehicle_input_dict = self.get_vehicle_data_as_dict()
            return DataFrame(vehicle_input_dict)
        except Exception as e:
            raise MyException(e, sys) from e

    def get_vehicle_data_as_dict(self):
        """
        Returns a dictionary of the vehicle data
        """
        logging.info("Entered get_vehicle_data_as_dict method of VehicleData class")
        try:
            input_data = {
                "Gender": [self.Gender],
                "Age": [self.Age],
                "Driving_License": [self.Driving_License],
                "Region_Code": [self.Region_Code],
                "Previously_Insured": [self.Previously_Insured],
                "Annual_Premium": [self.Annual_Premium],
                "Policy_Sales_Channel": [self.Policy_Sales_Channel],
                "Vintage": [self.Vintage],
                "Vehicle_Age_lt_1_Year": [self.Vehicle_Age_lt_1_Year],
                "Vehicle_Age_gt_2_Years": [self.Vehicle_Age_gt_2_Years],
                "Vehicle_Damage_Yes": [self.Vehicle_Damage_Yes]
            }

            logging.info("Created vehicle data dict successfully")
            logging.info("Exited get_vehicle_data_as_dict method of VehicleData class")
            return input_data

        except Exception as e:
            raise MyException(e, sys) from e


class VehicleDataClassifier:
    def __init__(self,
                 prediction_pipeline_config: VehiclePredictorConfig = VehiclePredictorConfig()) -> None:
        """
        :param prediction_pipeline_config: Configuration for prediction
        """
        try:
            self.prediction_pipeline_config = prediction_pipeline_config
        except Exception as e:
            raise MyException(e, sys)

    def predict(self, dataframe: DataFrame) -> str:
        """
        Predicts the outcome using the trained model from S3.
        """
        try:
            logging.info("Entered predict method of VehicleDataClassifier class")

            # Load estimator wrapper
            estimator = Proj1Estimator(
                bucket_name=self.prediction_pipeline_config.model_bucket_name,
                model_path=self.prediction_pipeline_config.model_file_path,
            )

            # Load actual trained model (MyModel) from S3
            my_model = estimator.load_model()

            # Run prediction
            result_df = my_model.predict(dataframe)   # DataFrame with "prediction" column
            result = result_df["prediction"].iloc[0]  # extract single value

            logging.info(f"Prediction result: {result}")
            return str(result)

        except Exception as e:
            raise MyException(e, sys) from e
