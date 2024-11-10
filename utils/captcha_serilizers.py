from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class CaptchaSerializers(serializers.Serializer):
    captcha = serializers.CharField(max_length=100)
    key = serializers.CharField(max_length=255)

    class Meta:
        fields = (
            'captcha',
            'key'
        )

    def create(self, validated_data, obj):
        if validated_data.get('captcha'):
            del validated_data['captcha']
        if validated_data.get('key'):
            del validated_data['key']
        message: obj = obj.objects.create(**validated_data)
        return message
