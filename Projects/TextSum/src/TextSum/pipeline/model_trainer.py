from TextSum.config.configuration import ConfigurationManager
from TextSum.components.model_trainer import ModelTrainer
from TextSum.logging import logger

class ModelTrainingPipeline:
    def __init__(self):
        pass
    
    def main(self):  
        config = ConfigurationManager()
        model_trainer_config = config.get_model_trainer_config()
        model_trainer_config = ModelTrainer(config = model_trainer_config)
        model_trainer_config.train()