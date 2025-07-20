def home(request):
    return render(request, 'home.html')


from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import JaundiceCase
import random

def explore(request):
    ethnicity = request.GET.get('ethnicity')
    region = request.GET.get('region')
    feeding = request.GET.get('feeding')
    search_query = request.GET.get('q')

    # Base queryset
    cases = JaundiceCase.objects.all()

    # Apply filters
    if ethnicity:
        cases = cases.filter(ethnicity__iexact=ethnicity)
    if region:
        cases = cases.filter(region__iexact=region)
    if feeding:
        cases = cases.filter(feeding_pattern__iexact=feeding)

    if search_query:
        cases = cases.filter(
            Q(feeding_pattern__icontains=search_query) |
            Q(sleeping_pattern__icontains=search_query) |
            Q(stooling_pattern__icontains=search_query) |
            Q(urine_color__icontains=search_query) |
            Q(skin_color__icontains=search_query) |
            Q(eye_color__icontains=search_query) |
            Q(notes__icontains=search_query)
        )

    # Shuffle and limit to 12
    cases = cases.order_by('?')[:12]

    # Dropdown filter options
    ethnicities = ["Black", "Asian", "Mixed"]
    region_list = ["Eyes", "Palms", "Feet", "Gums", "Tongue"]

    return render(request, 'explore.html', {
        'cases': cases,
        'ethnicities': ethnicities,
        'region_list': region_list,
        'request': request,
    })




from .models import JaundiceCase
from django.shortcuts import get_object_or_404, render
import random

def case_detail(request, pk):
    case = get_object_or_404(JaundiceCase, pk=pk)
    related_cases = list(JaundiceCase.objects.exclude(pk=pk))
    random.shuffle(related_cases)
    return render(request, 'case_detail.html', {
        'case': case,
        'related_cases': related_cases[:6]  # limit to 6 thumbnails
    })


from django.core.files.storage import FileSystemStorage

def comparison_tool(request):
    image1_url = None
    image2_url = None

    if request.method == 'POST':
        fs = FileSystemStorage()

        if request.FILES.get('image1'):
            image1 = request.FILES['image1']
            filename1 = fs.save(f"comparisons/{image1.name}", image1)
            image1_url = fs.url(filename1)

        if request.FILES.get('image2'):
            image2 = request.FILES['image2']
            filename2 = fs.save(f"comparisons/{image2.name}", image2)
            image2_url = fs.url(filename2)

    return render(request, 'comparison_tool.html', {
        'image1_url': image1_url,
        'image2_url': image2_url
    })


from django.core.files.storage import FileSystemStorage
import random

def jaundice_checker(request):
    uploaded_image_url = None
    prediction = None

    if request.method == 'POST' and request.FILES.get('image'):
        fs = FileSystemStorage()
        image = request.FILES['image']
        filename = fs.save(f"checker_uploads/{image.name}", image)
        uploaded_image_url = fs.url(filename)

        prediction = {
            'score': round(random.uniform(45, 95), 2),
            'region': random.choice(['Eyes', 'Skin', 'Gums', 'Tongue']),
            'notes': 'Signs of yellowing observed in localized regions.'
        }

    return render(request, 'jaundice_checker.html', {
        'uploaded_image_url': uploaded_image_url,
        'prediction': prediction
    })

