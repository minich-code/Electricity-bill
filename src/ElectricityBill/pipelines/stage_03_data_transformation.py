from src.ElectricityBill.config.configuration import ConfigurationManager
from src.ElectricityBill.components.data_transformation import DataTransformation
from src.ElectricityBill import logging
from pathlib import Path
import os

STAGE_NAME = "Data Transformation Stage"

class DataTransformationPipeline:
    def __init__(self):
        pass


    def main(self):
        try:
            with open(Path("artifacts/data_validation/status.txt"), "r") as f:
                status = f.read().split(" ")[-1]


            if status == "True":
                 # Create a ConfigurationManager object
                config = ConfigurationManager()
                # Get the data transformation configuration
                data_transformation_config = config.get_data_transformation_config()
                # Initiate data transformation
                data_transformation = DataTransformation(config=data_transformation_config)
                # Perform train-test splitting and store the results
                self.X_train, self.X_test, self.y_train, self.y_test = data_transformation.train_test_splitting()

                train_path = os.path.join(data_transformation_config.root_dir, "train.csv")
                test_path = os.path.join(data_transformation_config.root_dir, "test.csv")

                # Initiate data transformation and store the results
                self.X_train_transformed, self.X_test_transformed, self.y_train, self.y_test = data_transformation.initiate_data_transformation(
                    train_path, test_path
                )
            else:
                raise Exception("Your data schema is not valid")

        except Exception as e:
            print(e)