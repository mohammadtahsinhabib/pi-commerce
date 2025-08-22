from rest_framework import serializers
from .models import ProductImage

def validate_file_extension(value):
    valid_extensions = ['jpg', 'jpeg', 'png']
    if not value.name.split('.')[-1].lower() in valid_extensions:
        raise serializers.ValidationError(f"File type not supported. Supported types: {', '.join(valid_extensions)}")
    return value   