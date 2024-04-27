from rest_framework import serializers

from apps.files.models import File


class FileDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = [
            'name',
            'size',
            'path',
        ]
