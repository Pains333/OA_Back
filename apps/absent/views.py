from rest_framework import viewsets
from rest_framework import mixins
from .models import Absent, AbsentType, AbsentStatusChoices
from .serializers import AbsentSerializer, AbsentTypeSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import get_responder
from apps.oaauth.serializers import UserSerializer

# Create your views here.
class AbsentViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        # 默认情况下，如果要修改某一条数据，那么要把这个数据的序列化中
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        who = request.query_params.get('who')
        if who and who == 'sub':
            result = queryset.filter(responder=request.user)
        else:
            result = queryset.filter(requester=request.user)

        page = self.paginate_queryset(result)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(result, many=True)
        return Response(data=serializer.data)

# 请假类型
class AbsentTypeView(APIView):
    def get(self, request):
        types = AbsentType.objects.all()
        serializer = AbsentTypeSerializer(types, many=True)
        return Response(data=serializer.data)

# 显示审批者
class ResponderView(APIView):
    def get(self, request):
        responder = get_responder(request)
        serializer = UserSerializer(responder)
        return Response(data=serializer.data)