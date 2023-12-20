from TextSum.pipeline.data_ingestion import DataIngestionTrainingPipeline
from TextSum.logging import logger

STAGE_NAME = "Data Ingesion"

try:
    logger.info(f">>>>>> {STAGE_NAME} started <<<<<<")
    data_ingestion = DataIngestionTrainingPipeline()
    data_ingestion.main()
    logger.info(f">>>>>> {STAGE_NAME} completed <<<<<<")
    
except Exception as e:
    logger.exception(e)
    raise e