import unittest
import pandas as pd
import os
import joblib
import sys
import numpy as np # For checking float types

# Add the 'app' directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.predict import predict_salary
from app.train_model import train_model # To create a model for testing predictions

class TestPredictModel(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test method."""
        self.test_data_dir = os.path.dirname(os.path.abspath(__file__)) # Should be 'tests/'
        self.test_train_dataset_path = os.path.join(self.test_data_dir, 'dummy_predict_train_data.csv')
        self.test_model_path = os.path.join(self.test_data_dir, 'dummy_test_model.pkl')

        # Create a dummy CSV file for training a temporary model
        dummy_data = {
            'YearsExperience': [1.1, 1.3, 1.5, 2.0, 2.2, 2.9, 3.0, 3.2, 3.2, 3.7],
            'EducationLevel': ["Bachelor's", "Master's", "PhD", "Bachelor's", "Master's", 
                               "PhD", "Bachelor's", "Master's", "PhD", "Bachelor's"],
            'Salary': [39343, 46205, 37731, 43525, 39891, 56642, 60150, 54445, 64445, 57189]
        }
        df = pd.DataFrame(dummy_data)
        # Ensure the 'tests' directory exists for the dummy data and model
        os.makedirs(self.test_data_dir, exist_ok=True)
        df.to_csv(self.test_train_dataset_path, index=False)

        # Train a dummy model for prediction tests
        # train_model expects paths relative to project root or absolute.
        # Our paths self.test_train_dataset_path and self.test_model_path are absolute.
        train_model(self.test_train_dataset_path, self.test_model_path)
        
        self.sample_input_features = {'YearsExperience': 5.0, 'EducationLevel': "Bachelor's"}


    def test_predict_salary_returns_prediction(self):
        """Test if predict_salary returns a valid prediction."""
        # Ensure the model was created in setUp
        self.assertTrue(os.path.exists(self.test_model_path), "Model for testing prediction was not created in setUp.")

        prediction = predict_salary(self.sample_input_features, self.test_model_path)

        # Assert that the prediction is not None
        self.assertIsNotNone(prediction, "Prediction should not be None for valid input.")

        # Assert that the prediction is a float or numpy float
        self.assertIsInstance(prediction, (float, np.floating), 
                              f"Prediction should be a float, but got {type(prediction)}.")

    def test_predict_salary_no_model_file(self):
        """Test predict_salary behavior when the model file is missing."""
        non_existent_model_path = os.path.join(self.test_data_dir, 'non_existent_model.pkl')
        
        # Ensure the non_existent_model_path indeed does not exist
        if os.path.exists(non_existent_model_path):
            os.remove(non_existent_model_path) 
            
        prediction = predict_salary(self.sample_input_features, non_existent_model_path)

        # predict_salary is expected to return None and print an error if model file not found
        self.assertIsNone(prediction, 
                          "Prediction should be None when the model file does not exist.")

    def tearDown(self):
        """Clean up created files after each test method."""
        if os.path.exists(self.test_train_dataset_path):
            os.remove(self.test_train_dataset_path)
        if os.path.exists(self.test_model_path):
            os.remove(self.test_model_path)

if __name__ == '__main__':
    unittest.main()
