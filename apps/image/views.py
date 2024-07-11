from .serializers import UploadImageSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from shortuuid import uuid
import os
from django.conf import settings

# Create your views here.
class ImageListView(APIView):
    def post(self, request):
        serializer = UploadImageSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data.get('image')
            filename = uuid() + os.path.splitext(file.name)[-1]
            path = settings.MEDIA_ROOT / filename
            try:
                with open(path, 'wb') as fp:
                    for chunk in file.chunks():
                        fp.write(chunk)
            except Exception:
                return Response({
                    'errno': 1,
                    'message': '图片保存失败'
                })
            file_url = settings.MEDIA_URL + filename
            return Response({
                'errno': 0,
                'data': {
                    'url': file_url,
                    'alt': '',
                    'href': file_url,
                }
            })
        else:
            return Response({
                'errno': 1,
                'message': list(serializer.errors.values())[0][0]
            })
