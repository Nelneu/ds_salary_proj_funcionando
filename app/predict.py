import joblib
import pandas as pd
import os

def predict_salary(input_features, model_path='models/trained_salary_model.pkl'):
    """
    Predicts salary based on input features using a trained model.

    Args:
        input_features (dict): A dictionary containing the features for prediction.
                               Example: {'YearsExperience': 5, 'EducationLevel': "Bachelor's"}
        model_path (str): Path to the trained model file.

    Returns:
        float or None: The predicted salary, or None if an error occurs.
    """
    try:
        # Load the trained model (pipeline)
        # The model file should be relative to the repository root if not an absolute path.
        # For consistency with train_model.py, we'll construct the path from the script's location.
        if not os.path.isabs(model_path):
            script_dir = os.path.dirname(os.path.abspath(__file__))
            model_path = os.path.join(script_dir, '..', model_path)
            
        if not os.path.exists(model_path):
            print(f"Error: Model file not found at {model_path}")
            return None
            
        model = joblib.load(model_path)

        # Convert input_features dictionary to a pandas DataFrame
        # The column names and order must match the training data X (features)
        # For this model, the features used during training were 'YearsExperience' and 'EducationLevel'.
        # The order matters for the preprocessor if it was trained with a specific column order.
        # It's generally safer to create the DataFrame with explicit column order.
        
        # Expected columns based on sample_salary_data.csv (excluding target 'Salary')
        # The order should ideally be derived from the training script or stored metadata,
        # but for this example, we'll hardcode it based on our knowledge of sample_salary_data.csv
        # and the assumption that X = df.iloc[:, :-1] was used.
        feature_columns = ['YearsExperience', 'EducationLevel'] 
        
        input_df = pd.DataFrame([input_features], columns=feature_columns)

        # --- Ensure data types match training data if necessary ---
        # For instance, 'YearsExperience' should be float/int, 'EducationLevel' should be object/str.
        # Pandas DataFrame creation from dict usually handles this well, but explicit conversion
        # might be needed for more complex scenarios (e.g., ensuring specific float precision).
        # For this example, default behavior should be fine.
        # Example: input_df['YearsExperience'] = pd.to_numeric(input_df['YearsExperience'])
        #          input_df['EducationLevel'] = input_df['EducationLevel'].astype(str)


        # Use the loaded model (pipeline) to make a prediction
        # The pipeline will handle preprocessing (scaling, one-hot encoding) automatically.
        prediction = model.predict(input_df)

        return prediction[0]  # predict() returns an array, get the first element

    except FileNotFoundError:
        print(f"Error: Model file not found at {model_path}")
        return None
    except Exception as e:
        print(f"Error during prediction: {e}")
        return None

if __name__ == '__main__':
    # Define the path to the model
    # This assumes the script is run from the repository root or 'app/' directory
    # and the model is in 'models/' relative to the repo root.
    repo_root_or_app_dir = os.getcwd() # Get current working directory
    
    # Construct model path relative to the script's location for robustness
    script_dir = os.path.dirname(os.path.abspath(__file__))
    default_model_path = os.path.join(script_dir, '..', 'models', 'trained_salary_model.pkl')

    # Sample input features for testing
    # These should match the feature names used during training.
    sample_features = {'YearsExperience': 5.0, 'EducationLevel': "Bachelor's"}
    # Test with another example, including a PhD
    sample_features_phd = {'YearsExperience': 10.0, 'EducationLevel': 'PhD'}
    # Test with a missing value (if the model's preprocessor handles it)
    # The current preprocessor in train_model.py uses SimpleImputer, so this should work.
    sample_features_missing_exp = {'YearsExperience': None, 'EducationLevel': "Master's"}


    print(f"Attempting to load model from: {default_model_path}")

    if not os.path.exists(default_model_path):
        print(f"Error: The model file '{default_model_path}' does not exist.")
        print("Please run `app/train_model.py` first to train and save the model.")
    else:
        # Call the prediction function with sample features
        predicted_salary = predict_salary(sample_features, model_path=default_model_path)
        if predicted_salary is not None:
            print(f"Prediction for {sample_features}: Salary = {predicted_salary:.2f}")

        predicted_salary_phd = predict_salary(sample_features_phd, model_path=default_model_path)
        if predicted_salary_phd is not None:
            print(f"Prediction for {sample_features_phd}: Salary = {predicted_salary_phd:.2f}")
        
        predicted_salary_missing = predict_salary(sample_features_missing_exp, model_path=default_model_path)
        if predicted_salary_missing is not None:
            print(f"Prediction for {sample_features_missing_exp} (with missing experience): Salary = {predicted_salary_missing:.2f}")

        # Example with a value that might not have been in one-hot encoder's training categories
        # 'handle_unknown='ignore'' in OneHotEncoder should handle this by outputting all zeros for that category.
        sample_features_unknown_edu = {'YearsExperience': 6.0, 'EducationLevel': 'Associate Degree'}
        predicted_salary_unknown_edu = predict_salary(sample_features_unknown_edu, model_path=default_model_path)
        if predicted_salary_unknown_edu is not None:
            print(f"Prediction for {sample_features_unknown_edu} (unknown EducationLevel): Salary = {predicted_salary_unknown_edu:.2f}")
