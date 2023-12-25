from TextSum.pipeline.data_ingestion import DataIngestionTrainingPipeline
from TextSum.pipeline.data_ingestion import DataValidationTrainingPipeline
from TextSum.logging import logger

STAGE_NAME = "Data Ingestion"

try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
    
except Exception as e:
    logger.exception(e)
    raise e

STAGE_NAME = "Data Validation"

try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    data_validation = DataValidationTrainingPipeline()
    data_validation.main()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
    
except Exception as e:
    logger.exception(e)
    raise e