from django.contrib import admin
from django.utils.html import format_html
from .models import JaundiceCase

class JaundiceCaseAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'thumbnail', 'ethnicity', 'condition', 'region')

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" />', obj.image.url)
        return "No image"

    thumbnail.short_description = 'Image Preview'

admin.site.register(JaundiceCase, JaundiceCaseAdmin)
