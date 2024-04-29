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
from src.ElectricityBill.entity.config_entity import DataTransformationConfig

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