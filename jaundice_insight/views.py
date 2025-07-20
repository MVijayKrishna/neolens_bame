# jaundice_insight/views.py

# jaundice_insight/views.py

import os
import random
from django.conf import settings
from django.shortcuts import render, redirect
from .utils import predict_jaundice
from .models import JaundicePrediction

def jaundice_check(request):
    context = {}

    if request.method == 'POST':
        form_data = {
            'ethnicity': request.POST['ethnicity'],
            'region': request.POST['region'],
            'feeding_pattern': request.POST['feeding_pattern'],
            'sleeping_pattern': request.POST['sleeping_pattern'],
            'stooling_pattern': request.POST['stooling_pattern'],
            'urine_color': request.POST['urine_color'],
            'skin_color': request.POST['skin_color'],
            'eye_color': request.POST['eye_color'],
        }

        # Run model prediction
        result, confidence = predict_jaundice(form_data)

        # Save prediction to DB
        JaundicePrediction.objects.create(
            prediction=result,
            confidence=confidence,
            **form_data
        )

        # Attempt fallback image lookup
        ethnicity = form_data['ethnicity'].lower()
        region = form_data['region'].lower()
        condition = result.lower()  # 'jaundiced' or 'normal'

        image_url = None
        case_notes = None

        folder_path = os.path.join(settings.MEDIA_ROOT, 'jaundice_dataset', ethnicity, condition, region)

        if os.path.exists(folder_path):
            image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if image_files:
                chosen_file = random.choice(image_files)
                image_url = os.path.join(settings.MEDIA_URL, 'jaundice_dataset', ethnicity, condition, region, chosen_file)
                case_notes = "Representative case from dataset"
            else:
                case_notes = "No images found in folder."
        else:
            case_notes = "No matching image folder found."

        # Add data to context
        context.update({
            'submitted': True,
            'result': result,
            'confidence': round(confidence * 100, 2),
            'image_url': image_url,
            'case_notes': case_notes
        })

    return render(request, 'check.html', context)






from django.shortcuts import render
from .models import JaundicePrediction

def prediction_history(request):
    history = JaundicePrediction.objects.order_by('-timestamp')[:50]
    return render(request, 'history.html', {'history': history})

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

def prediction_history(request):
    history = JaundicePrediction.objects.all().order_by('-timestamp')
    return render(request, 'history.html', {'history': history})

@csrf_exempt
def clear_prediction_history(request):
    if request.method == "POST":
        JaundicePrediction.objects.all().delete()
        return redirect('prediction_history')

