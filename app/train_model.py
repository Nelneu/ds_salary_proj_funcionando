import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
import joblib
import os
import numpy as np # Will be needed for handling potential NaN in target

def train_model(dataset_path, model_output_path):
    """
    Trains a linear regression model on the given dataset and saves it.

    Args:
        dataset_path (str): Path to the CSV dataset.
        model_output_path (str): Path to save the trained model.

    Returns:
        dict: A dictionary containing a success message and the model path.
    """
    try:
        # Load the dataset
        df = pd.read_csv(dataset_path)

        # --- Placeholder: Assume the last column is the target variable ---
        # --- and all other columns are features. ---
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]

        # Handle potential NaN values in the target variable (e.g., by removing rows)
        # This is a common approach. Alternatively, imputation could be used if appropriate.
        if y.isnull().any():
            print(f"Warning: Target variable contains NaN values. Removing rows with NaN target.")
            nan_target_indices = y[y.isnull()].index
            X = X.drop(index=nan_target_indices)
            y = y.drop(index=nan_target_indices)
            # Reset index if you plan to concatenate or merge later, though not strictly necessary for model training itself
            X.reset_index(drop=True, inplace=True)
            y.reset_index(drop=True, inplace=True)


        # --- Placeholder: Basic preprocessing ---
        # Identify numerical and categorical features
        numerical_features = X.select_dtypes(include=np.number).columns.tolist()
        categorical_features = X.select_dtypes(exclude=np.number).columns.tolist()

        # Create preprocessing pipelines for numerical and categorical features
        numerical_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='mean')),  # Fill missing numerical values with mean
            ('scaler', StandardScaler())  # Scale numerical features
        ])

        categorical_pipeline = Pipeline([
            ('imputer', SimpleImputer(strategy='most_frequent')),  # Fill missing categorical values with mode
            ('onehot', OneHotEncoder(handle_unknown='ignore'))  # Apply one-hot encoding
        ])

        # Create a column transformer to apply different transformations to different columns
        preprocessor = ColumnTransformer([
            ('numerical', numerical_pipeline, numerical_features),
            ('categorical', categorical_pipeline, categorical_features)
        ])

        # Create the full model pipeline
        model_pipeline = Pipeline([
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ])

        # Train the model
        model_pipeline.fit(X, y)

        # Ensure the output directory exists
        os.makedirs(os.path.dirname(model_output_path), exist_ok=True)

        # Save the trained model
        joblib.dump(model_pipeline, model_output_path)

        return {
            "message": "Model trained successfully!",
            "model_path": model_output_path
        }

    except Exception as e:
        return {
            "message": f"Error during model training: {e}",
            "model_path": None
        }

if __name__ == '__main__':
    # Define paths
    # Assuming the script is in 'app/' and data is in 'data/' relative to the repo root
    repo_root = os.path.dirname(os.path.abspath(__file__))
    dataset_path = os.path.join(repo_root, '..', 'data', 'sample_salary_data.csv')
    model_output_path = os.path.join(repo_root, '..', 'models', 'trained_salary_model.pkl')
    
    # Check if sample data exists
    if not os.path.exists(dataset_path):
        print(f"Error: Sample dataset not found at {dataset_path}")
        print("Please ensure 'data/sample_salary_data.csv' exists.")
        # Create a dummy CSV for basic testing if it doesn't exist (as per original instructions)
        # This part of the original instruction seems to be covered by a previous step.
        # However, to make this script runnable independently for testing, we can add a check.
        # For this task, we'll assume the file is already created by the previous agent turn.
    else:
        # Call the training function
        training_result = train_model(dataset_path, model_output_path)

        # Print the result
        print(training_result)
