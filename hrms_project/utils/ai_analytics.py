import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

def train_attrition_model():
    """Demo AI model for attrition prediction"""
    # Sample data
    data = pd.DataFrame({
        'tenure': np.random.randint(1, 10, 100),
        'salary': np.random.randint(30000, 150000, 100),
        'performance': np.random.randint(1, 5, 100),
        'attrition': np.random.choice([0,1], 100, p=[0.8, 0.2])
    })
    X = data[['tenure', 'salary', 'performance']]
    y = data['attrition']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    return model

def predict_attrition(model, employee_data):
    """Predict for single employee"""
    pred = model.predict([employee_data])
    return "High Risk" if pred[0] == 1 else "Low Risk"