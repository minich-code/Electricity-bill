from src.ElectricityBill.config.configuration import ConfigurationManager
from src.ElectricityBill.components.data_validation import DataValidation
from src.ElectricityBill import logging


STAGE_NAME = "Data Validation stage"

class DataValidationPipeline:
    def __init__(self):
        pass 

    def main(self):
        config = ConfigurationManager()
        data_validation_config = config.get_data_validation_config()
        data_validation = DataValidation(config=data_validation_config)
        data_validation.validate_all_columns()


if __name__ == "__main__":
    try:
        logging.info(f"++++++++++++++++++++++ {STAGE_NAME} started ++++++++++++++++++++++++++")
        obj = DataValidationPipeline()
        obj.main()
        logging.info(f"********************** {STAGE_NAME} completed ****************\n\nx================x")

    except Exception as e:
        logging.exception(e)
        raise e
