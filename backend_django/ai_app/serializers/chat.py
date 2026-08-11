from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    message = serializers.CharField(
        max_length=5000,
        allow_blank=False,
        trim_whitespace=True,
    )
