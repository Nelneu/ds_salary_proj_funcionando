import streamlit as st
import requests
import pandas as pd
import os

# Define the base URL for the Flask API
# Ensure the Flask API (app/main.py) is running for this UI to work.
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:5000")

# --- Page Configuration ---
st.set_page_config(page_title="Salary Prediction ML App", layout="wide")
st.title("Salary Prediction ML Application")
st.markdown("""
    Welcome to the Salary Prediction ML App!
    Use the sidebar to navigate between training a new model or predicting salaries.
    **Note:** Ensure the backend Flask API is running for this application to function.
""")

# --- Navigation ---
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Choose a section:", ("Train Model", "Predict Salary"))

# --- Helper function for API requests ---
def handle_api_response(response, success_message="Success!", error_message="An error occurred."):
    """Helper function to display API responses."""
    if response.status_code == 200:
        st.success(success_message)
        try:
            st.json(response.json())
        except requests.exceptions.JSONDecodeError:
            st.info("Response was not in JSON format, but request was successful.")
            st.text(response.text)
    else:
        st.error(error_message)
        try:
            st.json(response.json())
        except requests.exceptions.JSONDecodeError:
            st.warning(f"Could not decode JSON response. Status Code: {response.status_code}")
            st.text(response.text)

# =========================
# === TRAIN MODEL SECTION ===
# =========================
if app_mode == "Train Model":
    st.header("Train a New Model")
    st.markdown("""
        Upload a CSV file containing salary data to train a new model.
        The backend will use this data to train and save a model named `user_trained_model.pkl`.
        Ensure your CSV has features (e.g., 'YearsExperience', 'EducationLevel') and a target ('Salary').
        The backend's `train_model.py` currently assumes the last column is the target.
    """)

    uploaded_file = st.file_uploader("Choose a CSV file for training", type="csv")

    if uploaded_file is not None:
        st.info(f"File '{uploaded_file.name}' uploaded. Size: {uploaded_file.size} bytes.")
        
        # Display first few rows of the uploaded CSV
        try:
            df_display = pd.read_csv(uploaded_file)
            st.write("Preview of uploaded data (first 5 rows):")
            st.dataframe(df_display.head())
            # Reset file pointer for sending to API
            uploaded_file.seek(0)
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            df_display = None


        if st.button("Start Model Training"):
            if uploaded_file is not None: # Ensure df_display was successfully created to proceed
                files = {'dataset': (uploaded_file.name, uploaded_file, 'text/csv')}
                st.info("Sending data to the training API... This might take a moment.")
                try:
                    response = requests.post(f"{API_BASE_URL}/train", files=files, timeout=60) # Added timeout
                    handle_api_response(response, 
                                        success_message="Training request sent. See details below.",
                                        error_message="Failed to train model. See error below.")
                except requests.exceptions.ConnectionError:
                    st.error(f"Connection Error: Could not connect to the API at {API_BASE_URL}. Is the Flask server running?")
                except requests.exceptions.Timeout:
                    st.error("Request timed out. The training process might be taking too long or the server is unresponsive.")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            else:
                st.warning("Please ensure the uploaded CSV file is valid before training.")

# ============================
# === PREDICT SALARY SECTION ===
# ============================
elif app_mode == "Predict Salary":
    st.header("Predict Salary")
    st.markdown("""
        Enter the features below to get a salary prediction.
        The prediction will be made using a pre-trained model.
        By default, it uses `trained_salary_model.pkl` (trained on `sample_salary_data.csv`).
        If that's not found, it tries `user_trained_model.pkl`.
    """)

    # Input fields based on sample_salary_data.csv columns
    # 'YearsExperience', 'EducationLevel'
    years_experience = st.number_input("Years of Experience:", min_value=0.0, max_value=50.0, value=5.0, step=0.1, format="%.1f")
    
    education_levels = ["Bachelor's", "Master's", "PhD", "High School", "Associate Degree", "Other"]
    education_level = st.selectbox("Education Level:", options=education_levels, index=0)

    if st.button("Predict Salary"):
        # Prepare input data for the API
        input_data = {
            "YearsExperience": years_experience,
            "EducationLevel": education_level
        }
        st.info(f"Sending data for prediction: {input_data}")

        try:
            response = requests.post(f"{API_BASE_URL}/predict", json=input_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                prediction = result.get('prediction')
                if prediction is not None:
                    st.success(f"Predicted Salary: ${prediction:,.2f}")
                else:
                    st.error("Prediction could not be retrieved from the API response.")
                    st.json(result) # Show the full response if prediction key is missing
            else:
                handle_api_response(response,
                                    error_message="Prediction failed. See error below.")
        except requests.exceptions.ConnectionError:
            st.error(f"Connection Error: Could not connect to the API at {API_BASE_URL}. Is the Flask server running?")
        except requests.exceptions.Timeout:
            st.error("Request timed out. The prediction server might be unresponsive.")
        except Exception as e:
            st.error(f"An unexpected error occurred during prediction: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("Developed for the AI Software Engineer Test Case")
st.markdown(f"API Base URL: `{API_BASE_URL}`")

# To run this Streamlit app:
# 1. Ensure the Flask API (app/main.py) is running.
# 2. Open your terminal in the repository root.
# 3. Execute: streamlit run app/app_ui.py
```
