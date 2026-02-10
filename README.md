# Student Performance Prediction System

A simple Django web application that predicts student performance using Machine Learning.

## Features

- Predict student performance based on study habits
- Web form interface for easy data entry
- REST API endpoint for programmatic access
- Automatic database storage
- ML Model: RandomForest with 98.61% accuracy

## Quick Start

### 1. Activate Virtual Environment
```bash
venv\Scripts\activate
```

### 2. Run Server
```bash
python manage.py runserver
```

### 3. Open Browser
Go to: `http://127.0.0.1:8000/`

## Usage

### Web Interface
1. Open `http://127.0.0.1:8000/`
2. Fill in the form:
   - Hours Studied (0-12)
   - Previous Scores (0-100)
   - Sleep Hours (4-12)
   - Sample Papers (0-20)
   - Extracurricular Activities (checkbox)
3. Click "Predict Performance"
4. View prediction and student details

### REST API
**Endpoint**: `POST http://127.0.0.1:8000/api/predict/`

**Request**:
```json
{
  "hours_studied": 7,
  "previous_scores": 85,
  "extracurricular": true,
  "sleep_hours": 7,
  "sample_papers": 3
}
```

**Response**:
```json
{
  "predicted_performance_index": 76.13
}
```

## Project Structure

```
djangomlprediction/
├── manage.py                  # Django management
├── dataset.csv                # Training data (10k records)
├── db.sqlite3                 # Database
├── requirements.txt           # Dependencies
│
├── student_ml/                # Main project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
└── performance/               # App
    ├── models.py              # StudentPerformance model
    ├── views.py               # Web + API views
    ├── urls.py                # URL routing
    ├── admin.py               # Admin config
    ├── train_model.py         # ML training script
    ├── load_data.py           # CSV loader
    ├── model.pkl              # Trained model
    └── templates/
        └── index.html         # Web interface
```

## Model Details

- **Algorithm**: RandomForest Regressor
- **Accuracy**: 98.61% (R² score)
- **Features**: hours_studied, previous_scores, extracurricular, sleep_hours, sample_papers
- **Target**: performance_index (0-100)

## Retrain Model

```bash
python performance/train_model.py
```

## Reload Data

```bash
python performance/load_data.py
```

## Admin Panel

1. Create superuser:
```bash
python manage.py createsuperuser
```

2. Access admin:
```
http://127.0.0.1:8000/admin/
```

## Requirements

- Python 3.12
- Django 5.0
- djangorestframework
- pandas
- scikit-learn
- joblib
- numpy

Install all: `pip install -r requirements.txt`

## Database

- SQLite database with 10,000+ student records
- Auto-saves every prediction from web form

## License

MIT
