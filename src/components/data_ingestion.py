import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

# from src.components.model_trainer import ModelTrainerConfig
# from src.components.model_trainer import ModelTrainer


@dataclass                                   #this is the decorator
class DataIngestionConfig:                    #so now dataingestion component know where to save my trainpath,testpath and raw data path as we had given the inputs
    train_data_path: str = os.path.join('artifacts',"train.csv")
    test_data_path: str = os.path.join('artifacts',"test.csv")
    raw_data_path: str = os.path.join('artifacts',"data.csv")
    
#if we have to only define the variable then we could have used dataclass 
# but if we have some other function inside the class then we will use some constructor inside the class 
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig() #ingestion_config variable will consist of all this 3 values present in DataIngestionConfig.
        
    def initiate_data_ingestion(self):    #if some data is stored somewhwere i will write code inside it this function will work 
        logging.info("Entered the data ingestion method or component")
        try:
            df = pd.read_csv("notebook\data\stud.csv")
            logging.info("Read the dataset as dataframe") #we are using logging many times because whenever the exception rise we can easily know where it happened
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True) #making directories and checking if it exist then use that only
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info("Train Test Split initiated")
            train_set,test_set = train_test_split(df,test_size=0.2,random_state=42) #from this we will get train and test set from the df
            
            train_set.to_csv(self.ingestion_config.train_data_path,index = False,header=True)
            
            test_set.to_csv(self.ingestion_config.test_data_path,index = False,header=True)
            
            logging.info("Ingestion of data is completed")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
                
            )
            
        except Exception as e :
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    obj= DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
        
    data_transformation = DataTransformation()
    data_transformation.initiate_data_transformation(train_data,test_data)
    
                         
    