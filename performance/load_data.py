import pandas as pd
import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_ml.settings')
django.setup()

from performance.models import StudentPerformance


def run():
    """
    Load student performance data from CSV file into the database
    
    Expected CSV columns:
    - Hours Studied
    - Previous Scores
    - Extracurricular Activities
    - Sleep Hours
    - Sample Question Papers Practiced
    - Performance Index
    """
    # Path to dataset
    csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'dataset.csv')
    
    if not os.path.exists(csv_path):
        print(f"Error: Dataset not found at {csv_path}")
        print("Please ensure 'dataset.csv' is in the project root directory.")
        return
    
    # Read CSV file
    df = pd.read_csv(csv_path)
    
    # Clear existing data (optional)
    print("Clearing existing data...")
    StudentPerformance.objects.all().delete()
    
    # Load data into database
    print(f"Loading {len(df)} records into database...")
    count = 0
    
    for _, row in df.iterrows():
        StudentPerformance.objects.create(
            hours_studied=int(row['Hours Studied']),
            previous_scores=int(row['Previous Scores']),
            extracurricular=row['Extracurricular Activities'] == 'Yes',
            sleep_hours=int(row['Sleep Hours']),
            sample_papers=int(row['Sample Question Papers Practiced']),
            performance_index=float(row['Performance Index']),
        )
        count += 1
    
    print(f"Successfully loaded {count} records!")


if __name__ == '__main__':
    run()
