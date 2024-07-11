# 名字：Pains
# 时间：2024/6/24 15:45
from django.utils.deprecation import MiddlewareMixin
from rest_framework.authentication import get_authorization_header
from rest_framework import exceptions
from django.conf import settings
import jwt
from apps.oaauth.models import OAUser
from jwt.exceptions import ExpiredSignatureError
from django.http.response import JsonResponse
from rest_framework import status
from django.contrib.auth.models import AnonymousUser


class LoginCheckMiddleware(MiddlewareMixin):

    keyword = 'JWT'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.white_list = ['/auth/login', '/staff/active']

    def process_view(self, request, callback, callback_args, callback_kwargs):
        # 1. 如果返回None，那么会正常执行（包括执行视图、执行其他中间件的代码）
        # 2. 如果返回一个HttpResponse对象，将不会执行时图，以及后面的中间件代码
        if request.path in self.white_list or request.path.startswith(settings.MEDIA_URL):
            request.user = AnonymousUser()
            request.auth = None
            return None

        try:
            auth = get_authorization_header(request).split()

            if not auth or auth[0].lower() != self.keyword.lower().encode():
                raise exceptions.ValidationError('请传入JWT')

            if len(auth) == 1:
                msg = '不可用的JWT请求头'
                raise exceptions.AuthenticationFailed(msg)
            elif len(auth) > 2:
                msg = '不可用的JWT请求头，JWT Token中间不应该有空格'
                raise exceptions.AuthenticationFailed(msg)

            try:
                # 解密的算法和key必须和加密的算法保持一致
                jwt_token = auth[1]
                jw_info = jwt.decode(jwt_token, key=settings.SECRET_KEY, algorithms='HS256')
                userid = jw_info.get('userid')
                try:
                    user = OAUser.objects.get(pk=userid)
                    # HttpRequest对象，是Django内置的
                    request.user = user
                    request.auth = jwt_token
                except Exception:
                    msg = '用户不存在'
                    raise exceptions.AuthenticationFailed(msg)
            except ExpiredSignatureError:
                msg = 'JWT token已过期'
                raise exceptions.AuthenticationFailed(msg)
        except Exception as e:
            return JsonResponse({'detail': '请先登录'}, status=status.HTTP_403_FORBIDDEN)