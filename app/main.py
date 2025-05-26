import os
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

# Attempt to import local modules
try:
    import train_model
    import predict
except ImportError:
    # This is to handle cases where the script might be run directly
    # and Python doesn't automatically recognize 'app' as a package.
    # If run as 'python app/main.py', this might be needed.
    # If run as 'flask run' or 'python -m app.main', it should be fine.
    from . import train_model
    from . import predict


app = Flask(__name__)

# Configuration
# Define the root path of the application
# app.root_path is the 'app' directory if 'python -m app.main' or flask run is used
# If 'python app/main.py' is used, then app.root_path is also 'app'
# We need one level up for 'models' and 'uploads' directory
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(APP_ROOT)

UPLOAD_FOLDER = os.path.join(REPO_ROOT, 'uploads')
MODEL_FOLDER = os.path.join(REPO_ROOT, 'models')
DEFAULT_MODEL_PATH = os.path.join(MODEL_FOLDER, 'trained_salary_model.pkl')
USER_TRAINED_MODEL_FILENAME = 'user_trained_model.pkl' # Name for user-trained model

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL_FOLDER'] = MODEL_FOLDER
app.config['DEFAULT_MODEL_PATH'] = DEFAULT_MODEL_PATH

# Ensure upload and model directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['MODEL_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET'])
def home():
    """Root endpoint returning a welcome message."""
    return jsonify({"message": "Salary Prediction API"})


@app.route('/train', methods=['POST'])
def train_endpoint():
    """
    Endpoint to train a model.
    Expects a CSV file named 'dataset' in the request.
    """
    if 'dataset' not in request.files:
        return jsonify({"error": "No dataset file provided"}), 400

    file = request.files['dataset']

    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename) # Sanitize filename
        # Save dataset to a consistent name to avoid clutter, or use filename
        uploaded_file_path = os.path.join(app.config['UPLOAD_FOLDER'], "user_dataset.csv") # filename
        file.save(uploaded_file_path)

        # Define path for the newly trained model
        model_output_path = os.path.join(app.config['MODEL_FOLDER'], USER_TRAINED_MODEL_FILENAME)

        try:
            # Call the train_model function from train_model.py
            # train_model function expects paths relative to repo root or absolute
            result = train_model.train_model(uploaded_file_path, model_output_path)
            
            if result.get("model_path"):
                return jsonify({
                    "message": "Model training initiated successfully.",
                    "training_result": result
                }), 200
            else:
                return jsonify({
                    "error": "Model training failed.",
                    "details": result.get("message", "Unknown error")
                }), 500
        except Exception as e:
            return jsonify({"error": f"An error occurred during training: {str(e)}"}), 500
    else:
        return jsonify({"error": "Invalid file type. Please upload a CSV file."}), 400


@app.route('/predict', methods=['POST'])
def predict_endpoint():
    """
    Endpoint to make predictions.
    Expects JSON input with features.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    input_data = request.get_json()
    if not input_data:
        return jsonify({"error": "No input data provided"}), 400

    # For now, always use the default model.
    # Later, this could be extended to choose a user-trained model.
    model_path_to_use = app.config['DEFAULT_MODEL_PATH']
    
    # Check if the default model exists (trained from sample_salary_data.csv)
    if not os.path.exists(model_path_to_use):
        # Fallback or check for user trained model if default is missing
        user_model_path = os.path.join(app.config['MODEL_FOLDER'], USER_TRAINED_MODEL_FILENAME)
        if os.path.exists(user_model_path):
            model_path_to_use = user_model_path
            app.logger.info(f"Default model not found. Using user-trained model: {model_path_to_use}")
        else:
            return jsonify({"error": f"Model file not found at {model_path_to_use} or {user_model_path}. Please train a model first."}), 500
    
    try:
        # Call the predict_salary function from predict.py
        # predict_salary expects features as dict and model_path
        prediction_result = predict.predict_salary(input_features=input_data, model_path=model_path_to_use)

        if prediction_result is not None:
            return jsonify({"prediction": prediction_result}), 200
        else:
            # predict_salary might return None if there was an internal error (e.g. model file not found, caught by predict.py)
            return jsonify({"error": "Failed to get prediction. Model might not be available or input data is invalid."}), 500
    except Exception as e:
        app.logger.error(f"Error during prediction: {str(e)}")
        return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500


if __name__ == '__main__':
    # Note: Running with `python app/main.py` will make Flask's dev server
    # available on http://127.0.0.1:5000/ by default.
    # The host '0.0.0.0' makes it accessible from network if needed.
    app.run(host='0.0.0.0', port=5000, debug=True)
