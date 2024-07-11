# 名字：Pains
# 时间：2024/7/4 17:10
from rest_framework import serializers
from django.core.validators import FileExtensionValidator, get_available_image_extensions

class UploadImageSerializer(serializers.Serializer):
    # ImageField：会校验上传的文件是否为图片
    image = serializers.ImageField(
        validators=[FileExtensionValidator(['png', 'jpg', 'jpeg', 'gif'])],
        error_messages={'required': '请上传图片', 'invalid_image': '请上传正确格式的图片'}
    )

    def validate_image(self, value):
        max_size = 0.5 * 1024 * 1024
        size = value.size
        if size > max_size:
            raise serializers.ValidationError('图片最大不能超过0.5MB')
        return value