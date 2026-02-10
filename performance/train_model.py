import pandas as pd
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score


def train():
    """
    Train a RandomForest model on student performance data and save it
    
    The model predicts the Performance Index based on:
    - Hours Studied
    - Previous Scores
    - Extracurricular Activities
    - Sleep Hours
    - Sample Question Papers Practiced
    """
    # Path to dataset
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        print("Please ensure 'dataset.csv' is in the project root directory.")
        return
    
    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    
    print(f"Dataset shape: {df.shape}")
    print(f"\nColumns: {list(df.columns)}")
    
    # Encode categorical variable
    print("\nEncoding categorical variables...")
    df['Extracurricular Activities'] = LabelEncoder().fit_transform(
        df['Extracurricular Activities']
    )
    
    # Prepare features and target
    X = df.drop('Performance Index', axis=1)
    y = df['Performance Index']
    
    print(f"\nFeatures shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Split data
    print("\nSplitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    print(f"Training set size: {len(X_train)}")
    print(f"Test set size: {len(X_test)}")
    
    # Train model
    print("\nTraining RandomForest model...")
    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)
    
    # Evaluate model
    print("\nEvaluating model...")
    train_predictions = model.predict(X_train)
    test_predictions = model.predict(X_test)
    
    train_mse = mean_squared_error(y_train, train_predictions)
    test_mse = mean_squared_error(y_test, test_predictions)
    train_r2 = r2_score(y_train, train_predictions)
    test_r2 = r2_score(y_test, test_predictions)
    
    print(f"\nTraining MSE: {train_mse:.4f}")
    print(f"Test MSE: {test_mse:.4f}")
    print(f"Training R²: {train_r2:.4f}")
    print(f"Test R²: {test_r2:.4f}")
    
    # Save model
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    joblib.dump(model, model_path)
    print(f"\nModel trained and saved to {model_path}")
    
    # Display feature importances
    print("\nFeature Importances:")
    for feature, importance in zip(X.columns, model.feature_importances_):
        print(f"  {feature}: {importance:.4f}")


if __name__ == '__main__':
    train()
