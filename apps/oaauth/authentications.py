# 名字：Pains
# 时间：2024/6/18 17:53
import jwt
import time
from django.conf import settings
from rest_framework.authentication import BaseAuthentication, get_authorization_header
from rest_framework import exceptions
from jwt.exceptions import ExpiredSignatureError
from .models import OAUser

def generate_jwt(user):
    expire_time = time.time() + 60 * 60 * 24 * 7
    # exp是特殊的参数用于表示token过期的时间
    token = jwt.encode({'userid': user.pk, 'exp': expire_time}, key=settings.SECRET_KEY)
    return token

class UserTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        return request._request.user, request._request.auth

class JWTAuthentication(BaseAuthentication):
    """
    请求头中：
    Authorization: JWT 401f7ac837da42b97f613d789819ff93537bee6a
    """

    keyword = 'JWT'

    def authenticate(self, request):
        # 从请求头中获取Authorization
        # auth: ['JWT', '401f7ac837da42b97f613d789819ff93537bee6a']
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

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
                setattr(request, 'user', user)
                return user, jwt_token
            except Exception:
                msg = '用户不存在'
                raise exceptions.AuthenticationFailed(msg)
        except ExpiredSignatureError:
            msg = 'JWT token已过期'
            raise exceptions.AuthenticationFailed(msg)