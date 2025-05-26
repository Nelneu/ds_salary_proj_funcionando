import unittest
import pandas as pd
import os
import joblib
import sys

# Add the 'app' directory to the Python path to allow imports like 'from app.train_model import train_model'
# This is often necessary when running tests from the root directory or a 'tests' subdirectory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.train_model import train_model

class TestTrainModel(unittest.TestCase):

    def setUp(self):
        """Set up test environment before each test method."""
        self.test_data_dir = os.path.dirname(os.path.abspath(__file__)) # Should be 'tests/'
        self.test_dataset_path = os.path.join(self.test_data_dir, 'dummy_train_data.csv')
        self.test_model_output_path = os.path.join(self.test_data_dir, 'dummy_model.pkl')

        # Create a dummy CSV file for testing
        dummy_data = {
            'YearsExperience': [1.1, 1.3, 1.5, 2.0, None, 2.9, 3.0, 3.2, 3.2, 3.7],
            'EducationLevel': ["Bachelor's", "Master's", "PhD", "Bachelor's", "Master's", 
                               None, "Bachelor's", "Master's", "PhD", "Bachelor's"],
            'Salary': [39343, 46205, 37731, 43525, 39891, 56642, 60150, 54445, 64445, 57189]
        }
        df = pd.DataFrame(dummy_data)
        # Ensure the 'tests' directory exists for the dummy data and model
        os.makedirs(self.test_data_dir, exist_ok=True)
        df.to_csv(self.test_dataset_path, index=False)

    def test_train_model_runs_and_saves_model(self):
        """Test if train_model runs successfully and saves a model file."""
        # Call the train_model function
        # train_model expects paths relative to project root or absolute.
        # Our paths self.test_dataset_path and self.test_model_output_path are absolute.
        result = train_model(self.test_dataset_path, self.test_model_output_path)

        # Assert that the model file is created
        self.assertTrue(os.path.exists(self.test_model_output_path), "Model file was not created.")

        # Assert that the result is a dictionary containing success message and model path
        self.assertIsInstance(result, dict, "Result should be a dictionary.")
        self.assertIn("message", result, "Result dictionary should contain 'message'.")
        self.assertIn("model_path", result, "Result dictionary should contain 'model_path'.")
        self.assertEqual(result["message"], "Model trained successfully!", "Success message is incorrect.")
        self.assertEqual(result["model_path"], self.test_model_output_path, "Model path in result is incorrect.")

        # Optional: Load the model to ensure it's a valid joblib file (and a scikit-learn pipeline)
        try:
            loaded_model = joblib.load(self.test_model_output_path)
            self.assertIsNotNone(loaded_model, "Loaded model is None.")
            # Check if it's a pipeline (optional, but good check)
            from sklearn.pipeline import Pipeline
            self.assertIsInstance(loaded_model, Pipeline, "Saved model is not a scikit-learn Pipeline.")
        except Exception as e:
            self.fail(f"Failed to load the saved model: {e}")


    def tearDown(self):
        """Clean up created files after each test method."""
        if os.path.exists(self.test_dataset_path):
            os.remove(self.test_dataset_path)
        if os.path.exists(self.test_model_output_path):
            os.remove(self.test_model_output_path)

if __name__ == '__main__':
    unittest.main()
