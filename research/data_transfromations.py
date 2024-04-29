#Entity 
from dataclasses import dataclass 
from pathlib import Path 

from src.ElectricityBill.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH, SCHEMA_FILE_PATH
from src.ElectricityBill.utils.commons import read_yaml, create_directories


# Component 
import os 
from src.ElectricityBill import logging 
from sklearn.model_selection import train_test_split
import pandas as pd 
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline 
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

from src.ElectricityBill.utils.commons import save_object

@dataclass
class DataTransformationConfig:
    root_dir: Path
    data_path: Path
    numerical_cols: list
    categorical_cols: list

    
    

class ConfigurationManager:
    def __init__(
        self,
        config_filepath=CONFIG_FILE_PATH,
        params_filepath=PARAMS_FILE_PATH,
        schema_filepath=SCHEMA_FILE_PATH):

        
        """Initialize ConfigurationManager."""
        # Read YAML configuration files to initialize configuration parameters
        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)
        self.schema = read_yaml(schema_filepath)

        # Create necessary directories specified in the configuration
        create_directories([self.config.artifacts_root])

    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation 

        create_directories([config.root_dir])


        data_transformation_config = DataTransformationConfig(
            root_dir=Path(config.root_dir),
            data_path=Path(config.data_path),
            numerical_cols= list(config.numerical_cols),
            categorical_cols= list(config.categorical_cols)
        )
        return data_transformation_config



class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config

    def get_transformer_obj(self):
        try:
            # Separate numerical and categorical columns 
            numerical_cols = self.config.numerical_cols
            categorical_cols = self.config.categorical_cols

            # Create a pipeline for numerical columns
            numerical_transformer = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='median')),
                    ('scaler', StandardScaler())
                ]
            )

            # Create a pipeline for categorical columns
            categorical_transformer = Pipeline(
                steps=[
                    ('imputer', SimpleImputer(strategy='most_frequent', fill_value='missing')),
                    ('onehot', OneHotEncoder(handle_unknown='ignore'))
                ]
            )

            # Create a column transformer with the numerical and categorical pipelines
            preprocessor = ColumnTransformer(
                transformers=[
                    ('numerical', numerical_transformer, numerical_cols),
                    ('categorical', categorical_transformer, categorical_cols)
                ],
                remainder='passthrough'
            )
            
            return preprocessor
        
        except Exception as e:
            logging.error(f"Error in get_transformer_obj: {e}")
            raise e

    def train_test_splitting(self):
        df = pd.read_csv(self.config.data_path)
        X = df.drop(columns=["ElectricityBill"])
        y = df["ElectricityBill"]

        # Split the data into training and test sets with a 75/25 split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

        # Create DataFrames for training and test sets
        train_df = pd.concat([X_train, y_train], axis=1)
        test_df = pd.concat([X_test, y_test], axis=1)

        # Save training and test sets to CSV files
        train_df.to_csv(os.path.join(self.config.root_dir, "train.csv"), index=False)
        test_df.to_csv(os.path.join(self.config.root_dir, "test.csv"), index=False)

        logging.info("Split data into training and test sets")
        logging.info(f"Training set shape: {train_df.shape}")
        logging.info(f"Test set shape: {test_df.shape}")

        print(f"Training set shape: {train_df.shape}")
        print(f"Test set shape: {test_df.shape}")

        return X_train, X_test, y_train, y_test
    
    # # Initiate data transformation
    def initiate_data_transformation(self, train_path, test_path):
        try:
            # Load the train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
            # If paths are not provided, construct them
            # if train_path is None:
            #     train_path = os.path.join(self.config.root_dir, "train.csv")
            # if test_path is None:
            #     test_path = os.path.join(self.config.root_dir, "test.csv")

            # Load the train and test data
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            # Check the structure of train_df
            print(train_df.head())

            # Check the column names
            print(train_df.columns)

            # Get the transformer object
            preprocessor_obj = self.get_transformer_obj()

            # Split the data into features (X) and target (y)
            X_train = train_df.drop(columns=["ElectricityBill"])
            y_train = train_df["ElectricityBill"]
            X_test = test_df.drop(columns=["ElectricityBill"])
            y_test = test_df["ElectricityBill"]


            # Get the transformer object
            #preprocessor_obj = self.get_transformer_obj()

            # Transform the training and test data
            X_train_transformed = preprocessor_obj.fit_transform(X_train)
            X_test_transformed = preprocessor_obj.transform(X_test)

            # Save the transformed training and test data
            pd.DataFrame(X_train_transformed).to_csv(os.path.join(self.config.root_dir, "train_transformed.csv"), index=False)
            pd.DataFrame(X_test_transformed).to_csv(os.path.join(self.config.root_dir, "test_transformed.csv"), index=False)

             # Save the preprocessing object
            #joblib.dump(preprocessor_obj, os.path.join(self.config.root_dir, "preprocessor_obj.joblib"))

            # Save the preprocessing object 
            save_object(
                obj = preprocessor_obj,
                file_path = os.path.join(self.config.root_dir, "preprocessor_obj.joblib")
            )


            logging.info("Data transformation completed")
            logging.info(f"Training set shape: {X_train_transformed.shape}")
            logging.info(f"Test set shape: {X_test_transformed.shape}")

            print(f"Training set shape: {X_train_transformed.shape}")
            print(f"Test set shape: {X_test_transformed.shape}")

            return X_train_transformed, X_test_transformed, y_train, y_test

        except Exception as e:
            logging.error(f"Error in initiate_data_transformation: {e}")
            raise e
        
if __name__ == "__main__":
    try:
        # Create a ConfigurationManager object
        config = ConfigurationManager()
        # Get the data transformation configuration
        data_transformation_config = config.get_data_transformation_config()
        # Initiate data transformation
        data_transformation = DataTransformation(config=data_transformation_config)
        # Perform train-test splitting
        X_train, X_test, y_train, y_test = data_transformation.train_test_splitting()

        # Get the file paths for the train and test data
        train_path = os.path.join(data_transformation_config.root_dir, "train.csv")
        test_path = os.path.join(data_transformation_config.root_dir, "test.csv")

        # Initiate data transformation with the file paths
        X_train_transformed, X_test_transformed, y_train, y_test = data_transformation.initiate_data_transformation(train_path, test_path)

    except Exception as e:
        raise e
