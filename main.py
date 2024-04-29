from src.ElectricityBill import logging
from src.ElectricityBill.pipelines.stage_01_data_ingestion import DataIngestionPipeline
from src.ElectricityBill.pipelines.stage_02_data_validation import DataValidationPipeline


STAGE_NAME = "Data Ingestion Stage"
try:
    logging.info(f"++++++++++++++++++++++ {STAGE_NAME} started ++++++++++++++++++++++++++")
    data_ingestion = DataIngestionPipeline()
    data_ingestion.main()
    logging.info(f"*************** stage {STAGE_NAME} completed ****************\n\nx================x")
except Exception as e:
    logging.exception(e)
    raise e


STAGE_NAME = "Data Validation Stage"
try:
    logging.info(f"++++++++++++++++++++++ {STAGE_NAME} started ++++++++++++++++++++++++++")
    data_ingestion = DataValidationPipeline()
    data_ingestion.main()
    logging.info(f"*************** stage {STAGE_NAME} completed ****************\n\nx================x")
except Exception as e:
    logging.exception(e)
    raise e