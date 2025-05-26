# Salary Prediction ML Application

This application allows users to train a salary prediction model using their own dataset and then get salary predictions based on the trained model or a default model.

## Features
-   Train a custom salary prediction model by uploading a CSV file.
-   Predict salaries using the trained model.
-   Simple, modern, and friendly UI built with Streamlit.
-   Backend API built with Flask.

## Project Structure
```
.
├── app/
│   ├── main.py           # Flask API
│   ├── app_ui.py         # Streamlit UI
│   ├── train_model.py    # Model training script
│   ├── predict.py        # Prediction script
│   └── __init__.py
├── data/
│   └── sample_salary_data.csv # Sample data for training
├── models/                 # Trained models will be saved here
│   └── trained_salary_model.pkl # Default model
├── uploads/                # Uploaded datasets will be stored here
├── tests/                  # (Optional) Test scripts
├── requirements.txt        # Python dependencies
└── README.md
```

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd <your-repo-name>
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    Create a `requirements.txt` file with the following content:
    ```
    Flask>=2.0
    pandas>=1.3
    scikit-learn>=1.0
    streamlit>=1.0
    requests>=2.25
    joblib>=1.0
    werkzeug>=2.0 
    numpy>=1.20
    ```
    Then run:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Start the Backend (Flask API):**
    Open a terminal and run:
    ```bash
    python app/main.py
    ```
    The API will usually start on `http://localhost:5000`.

2.  **Start the Frontend (Streamlit UI):**
    Open another terminal and run:
    ```bash
    streamlit run app/app_ui.py
    ```
    The Streamlit app will usually open automatically in your browser or provide a URL like `http://localhost:8501`.

## Usage

### Training a Model
1.  Open the Streamlit application in your browser.
2.  Navigate to the "Train Model" section from the sidebar.
3.  Click "Choose a CSV file" and upload your dataset.
    *   **Dataset Format:** The CSV file should have features (e.g., 'YearsExperience', 'EducationLevel') and a target variable named 'Salary'. The backend currently attempts to automatically identify features and the target. Ensure your 'Salary' column is the last one for best results with the current auto-detection, or that it's clearly numerical if other columns are also numerical.
4.  Click "Start Model Training".
5.  The application will send the data to the backend, train a model, and display a success message along with the path where the model is saved (e.g., `models/user_trained_model.pkl`).

### Predicting Salary
1.  Open the Streamlit application.
2.  Navigate to the "Predict Salary" section.
3.  Enter the required features (e.g., Years of Experience, Education Level).
4.  Click "Predict Salary".
5.  The application will use the trained model (defaulting to `models/trained_salary_model.pkl` if no user model is trained via the UI, or if the user-trained model path logic in the backend is set up to use it) to make a prediction, which will then be displayed.

## Development Notes
- The backend API logs provide detailed information about requests, model loading, and errors. Check the terminal where `app/main.py` is running.
- The `train_model.py` script contains logic for data preprocessing. This includes mean imputation for numerical NaNs, mode imputation for categorical NaNs, one-hot encoding for categorical features, and standard scaling for numerical features.
