from django.shortcuts import render
import os
import joblib
import pandas as pd
from django.conf import settings
from sklearn.preprocessing import LabelEncoder

MODEL_PATH = os.path.join(settings.BASE_DIR, 'jaundice_screening/model/jaundice_xgb_model.pkl')
model = joblib.load(MODEL_PATH)

encoders = {
    'ethnicity': LabelEncoder().fit(["Black", "Asian", "Hispanic", "White", "Mixed"]),
    'region': LabelEncoder().fit(["West Africa", "East Africa", "South Asia", "Southeast Asia", "Latin America"]),
    'eye_color_severity': LabelEncoder().fit(["None", "Mild", "Moderate", "Severe"]),
    'skin_color_severity': LabelEncoder().fit(["None", "Mild", "Moderate", "Severe"]),
    'urine_color_severity': LabelEncoder().fit(["None", "Mild", "Moderate", "Severe"]),
    'feeding_pattern': LabelEncoder().fit(["Normal", "Reduced", "Absent"]),
    'sleeping_pattern': LabelEncoder().fit(["Normal", "Reduced", "Absent"]),
    'stooling_pattern': LabelEncoder().fit(["Normal", "Reduced", "Absent"]),
}

# ✅ Add this at the top of screening_view:
filters = [
    {
        'name': 'ethnicity',
        'label': 'Ethnicity',
        'options': ["Black", "Asian", "Hispanic", "White", "Mixed"],
        'tooltip': "Infant's self-identified or family-identified ethnicity."
    },
    {
        'name': 'region',
        'label': 'Region',
        'options': ["West Africa", "East Africa", "South Asia", "Southeast Asia", "Latin America"],
        'tooltip': "Geographic region where the infant is from."
    },
    {
        'name': 'eye_color',
        'label': 'Eye Color Severity',
        'options': ["None", "Mild", "Moderate", "Severe"],
        'tooltip': "Yellowing of the whites of the eyes."
    },
    {
        'name': 'skin_color',
        'label': 'Skin Color Severity',
        'options': ["None", "Mild", "Moderate", "Severe"],
        'tooltip': "Change in skin tone (yellowish tint)."
    },
    {
        'name': 'urine_color',
        'label': 'Urine Color Severity',
        'options': ["None", "Mild", "Moderate", "Severe"],
        'tooltip': "Darker or yellow-colored urine may indicate jaundice."
    },
    {
        'name': 'feeding',
        'label': 'Feeding Pattern',
        'options': ["Normal", "Reduced", "Absent"],
        'tooltip': "Feeding behavior (reduction may indicate illness)."
    },
    {
        'name': 'sleeping',
        'label': 'Sleeping Pattern',
        'options': ["Normal", "Reduced", "Absent"],
        'tooltip': "Amount and frequency of sleep."
    },
    {
        'name': 'stooling',
        'label': 'Stooling Pattern',
        'options': ["Normal", "Reduced", "Absent"],
        'tooltip': "Change in stool color or frequency."
    },
]

def screening_view(request):
    result = None
    confidence = None

    if request.method == 'POST':
        input_data = {
            'Ethnicity': request.POST.get('ethnicity'),
            'Region': request.POST.get('region'),
            'Eye_Color_Severity': request.POST.get('eye_color'),
            'Skin_Color_Severity': request.POST.get('skin_color'),
            'Urine_Color_Severity': request.POST.get('urine_color'),
            'Feeding_Pattern': request.POST.get('feeding'),
            'Sleeping_Pattern': request.POST.get('sleeping'),
            'Stooling_Pattern': request.POST.get('stooling'),
        }

        try:
            sclera_flag = 1 if input_data['Eye_Color_Severity'] in ['Moderate', 'Severe'] else 0

            abnormal_count = sum([
                input_data['Eye_Color_Severity'] != 'None',
                input_data['Skin_Color_Severity'] != 'None',
                input_data['Urine_Color_Severity'] != 'None',
                input_data['Feeding_Pattern'] != 'Normal',
                input_data['Sleeping_Pattern'] != 'Normal',
                input_data['Stooling_Pattern'] != 'Normal',
                sclera_flag
            ])

            refer_flag = 1 if abnormal_count >= 3 and sclera_flag == 1 else 0

            input_data['Sclera_Yellowing_Flag'] = sclera_flag
            input_data['Abnormal_Feature_Count'] = abnormal_count
            input_data['Refer_Flag'] = refer_flag

            encoder_map = {
                'Ethnicity': 'ethnicity',
                'Region': 'region',
                'Eye_Color_Severity': 'eye_color_severity',
                'Skin_Color_Severity': 'skin_color_severity',
                'Urine_Color_Severity': 'urine_color_severity',
                'Feeding_Pattern': 'feeding_pattern',
                'Sleeping_Pattern': 'sleeping_pattern',
                'Stooling_Pattern': 'stooling_pattern',
            }

            encoded = {
                key: encoders[encoder_map[key]].transform([value])[0]
                for key, value in input_data.items()
                if key in encoder_map
            }

            encoded['Sclera_Yellowing_Flag'] = sclera_flag
            encoded['Abnormal_Feature_Count'] = abnormal_count
            encoded['Refer_Flag'] = refer_flag

            df = pd.DataFrame([encoded])[[  # Ensure same order
                'Ethnicity', 'Region', 'Eye_Color_Severity', 'Skin_Color_Severity', 'Urine_Color_Severity',
                'Feeding_Pattern', 'Sleeping_Pattern', 'Stooling_Pattern',
                'Sclera_Yellowing_Flag', 'Abnormal_Feature_Count', 'Refer_Flag'
            ]]

            proba = model.predict_proba(df)[0]
            prediction = proba.argmax()
            confidence = round(proba[prediction] * 100)

            if prediction == 1:
                result = f"⚠️ Likely Jaundiced (confidence: {confidence}%)"
            else:
                result = f"✅ Appears Normal (confidence: {confidence}%)"

        except Exception as e:
            result = f"Error: {str(e)}"

    return render(request, 'screening.html', {'result': result, 'confidence': confidence if result else None, 'filters': filters})

    
