import os
import csv
import django
from django.core.files import File

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'neolens_project.settings')  # Change if your project name is different
django.setup()

from cases.models import JaundiceCase  # Replace with your app name

# File paths
csv_path = 'full_jaundice_metadata.csv'
image_base_dir = os.path.join('media', 'jaundice_dataset')

created_count = 0
missing_files = []

with open(csv_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        image_rel_path = row['File_Path'].replace('\\', '/')
        image_abs_path = os.path.join(image_base_dir, image_rel_path)

        if not os.path.isfile(image_abs_path):
            missing_files.append(image_abs_path)
            print(f"[WARNING] Missing image: {image_abs_path}")
            continue

        with open(image_abs_path, 'rb') as img_file:
            django_file = File(img_file)

            case = JaundiceCase(
                image_id=row['Image_ID'],
                ethnicity=row['Ethnicity'],
                condition=row['Condition'],
                region=row['Region'],
                feeding_pattern=row['Feeding_Pattern'],
                sleeping_pattern=row['Sleeping_Pattern'],
                stooling_pattern=row['Stooling_Pattern'],
                urine_color=row['Urine_Color'],
                skin_color=row['Skin_Color'],
                eye_color=row['Eye_Color'],
                notes=row['Notes'],
            )

            case.image.save(image_rel_path, django_file, save=True)
            print(f"[INFO] Imported: {row['Image_ID']}")
            created_count += 1

print(f"\n✔️ Done. {created_count} cases added.")
if missing_files:
    print(f"⚠️ {len(missing_files)} images were missing.")
