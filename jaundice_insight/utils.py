import joblib
import numpy as np
import os
from django.conf import settings

# Load model assets
BASE_DIR = os.path.join(settings.BASE_DIR, 'jaundice_insight', 'model')
model = joblib.load(os.path.join(BASE_DIR, 'xgboost_jaundice_model.pkl'))
scaler = joblib.load(os.path.join(BASE_DIR, 'scaler.pkl'))
label_encoders = joblib.load(os.path.join(BASE_DIR, 'label_encoders.pkl'))

def preprocess_input(data_dict):
    encoded_features = []

    for col in label_encoders:
        val = data_dict.get(col, '')  # No lower()
        le = label_encoders[col]

    
        if val not in le.classes_:
            encoded = 0  
        else:
            encoded = le.transform([val])[0]

        encoded_features.append(encoded)

    scaled = scaler.transform([encoded_features])
    return scaled


def predict_jaundice(data_dict):
    X = preprocess_input(data_dict)
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0][1] if prediction == 1 else model.predict_proba(X)[0][0]
    return ('Jaundiced' if prediction == 1 else 'Normal', float(proba))
