# 💰 Salary Prediction ML Application

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.3+-green.svg)](https://flask.palletsprojects.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A machine learning web application that predicts salaries based on user input features using trained ML models.

## 🎯 Features

- **Interactive Web Interface**: Clean, user-friendly Streamlit application
- **Machine Learning Models**: Multiple trained models for accurate salary predictions
- **RESTful API**: Flask-based API for programmatic access
- **Data Processing Pipeline**: Automated data cleaning and feature engineering
- **Model Persistence**: Trained models saved and ready for inference

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/leomatias/ds_salary_proj.git
   cd ds_salary_proj
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Streamlit Web App
```bash
streamlit run app/main.py
```
The application will be available at `http://localhost:8501`

#### Option 2: Flask API
```bash
python app/flask_api.py
```
API will be available at `http://localhost:5000`

## 📊 Usage

### Web Application
1. Open your browser to `http://localhost:8501`
2. Navigate to the "Train Model" section
3. Upload your CSV dataset or use the sample data
4. Select features and target variables
5. Train the model and view results
6. Go to "Predict Salary" section
7. Enter required features and get salary predictions

### API Endpoints

#### Train Model
```bash
POST /api/train
Content-Type: application/json

{
  "features": ["experience", "education", "location"],
  "target": "salary"
}
```

#### Predict Salary
```bash
POST /api/predict
Content-Type: application/json

{
  "experience": 5,
  "education": "Bachelor's",
  "location": "New York"
}
```

## 🏗️ Project Structure

```
ds_salary_proj/
├── app/
│   ├── main.py              # Streamlit web application
│   ├── flask_api.py         # Flask REST API
│   └── utils.py             # Utility functions
├── data/
│   ├── salary_data.csv      # Sample dataset
│   └── processed/           # Processed data files
├── models/                  # Trained ML models
├── notebooks/               # Jupyter notebooks for analysis
├── tests/                   # Unit tests
├── requirements.txt         # Python dependencies
├── .gitignore              # Git ignore file
└── README.md               # This file
```

## 🤖 Machine Learning Pipeline

1. **Data Ingestion**: Load and validate input data
2. **Data Preprocessing**: Handle missing values, encode categorical variables
3. **Feature Engineering**: Create relevant features for prediction
4. **Model Training**: Train multiple algorithms (Linear Regression, Random Forest, etc.)
5. **Model Evaluation**: Cross-validation and performance metrics
6. **Model Persistence**: Save trained models for deployment

## 🧪 Testing

Run the test suite:
```bash
pytest tests/
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 🔧 Development

### Code Formatting
```bash
black app/
isort app/
flake8 app/
```

### Pre-commit Hooks
```bash
pre-commit install
```

## 📈 Model Performance

| Model | MAE | RMSE | R² Score |
|-------|-----|------|----------|
| Linear Regression | 5,420 | 8,230 | 0.847 |
| Random Forest | 4,890 | 7,650 | 0.878 |
| Gradient Boosting | 4,720 | 7,420 | 0.889 |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👤 Author

**Nelson Pullella**
- GitHub: [@Nelneu](https://github.com/Nelneu)

⭐ **Star this repository if you found it helpful!**
