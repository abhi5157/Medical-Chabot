import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

class MedicalMLModels:
    def __init__(self):
        self.models = {}
        self.feature_columns = ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing', 
                              'Age', 'Gender', 'Blood Pressure', 'Cholesterol Level']
        self.scaler = StandardScaler()
        
    def preprocess_data(self, df):
        """Preprocess the dataset."""
        X = df[self.feature_columns].copy()
        
        # Convert categorical variables to numeric
        X['Gender'] = (X['Gender'] == 'Male').astype(int)
        X['Blood Pressure'] = X['Blood Pressure'].map({'Low': 0, 'Normal': 1, 'High': 2})
        X['Cholesterol Level'] = X['Cholesterol Level'].map({'Low': 0, 'Normal': 1, 'High': 2})
        
        # Convert Yes/No to 1/0 for symptom columns
        for col in ['Fever', 'Cough', 'Fatigue', 'Difficulty Breathing']:
            X[col] = (X[col] == 'Yes').astype(int)
            
        return X

    def train_models(self, dataset_path):
        """we use multiple models and select the best ones."""
        # Load and preprocess data
        df = pd.read_csv(dataset_path)
        X = self.preprocess_data(df)
        y = df['Disease']
        
        # Scale numerical features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split the dataset
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)
        
        # Initialize models
        models_to_train = {
            'decision_tree': DecisionTreeClassifier(random_state=42),
            'random_forest': RandomForestClassifier(n_estimators=100, random_state=42),
            'svm': SVC(probability=True, random_state=42)
        }
        
        # Train and evaluate models
        model_accuracies = {}
        for name, model in models_to_train.items():
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            accuracy = accuracy_score(y_test, y_pred)
            model_accuracies[name] = accuracy
            self.models[name] = model
            
        # Sort models by accuracy
        self.model_accuracies = dict(sorted(model_accuracies.items(), key=lambda x: x[1], reverse=True))
        
        return self.model_accuracies
    
    def predict(self, features):
        """Make predictions using the best performing model."""
        if not self.models:
            return None
            
        # Preprocess input features
        feature_df = pd.DataFrame([features])[self.feature_columns]
        feature_scaled = self.scaler.transform(feature_df)
        
        # Get the best model (first one in sorted dictionary)
        best_model_name = next(iter(self.model_accuracies))
        best_model = self.models[best_model_name]
        
        try:
            prediction = best_model.predict(feature_scaled)[0]
            return prediction
        except Exception as e:
            print(f"Error making prediction: {e}")
            return None 