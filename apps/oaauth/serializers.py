# 名字：Pains
# 时间：2024/6/18 17:20
from rest_framework import serializers, exceptions
from .models import OAUser, UserStatusChoices, OADepartment


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=20, min_length=6)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = OAUser.objects.filter(email=email).first()
            if not user:
                raise serializers.ValidationError('请输入正确邮箱')
            elif not user.check_password(password):
                raise serializers.ValidationError('请输入正确密码')
            elif user.status == UserStatusChoices.UNACTIVE:
                raise serializers.ValidationError('该用户尚未激活')
            elif user.status == UserStatusChoices.LOCKED:
                raise serializers.ValidationError('该用户已被锁定，请联系管理员')
            else:
                attrs['user'] = user
        else:
            raise serializers.ValidationError('请传入邮箱和密码')
        return attrs

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    class Meta:
        model = OAUser
        exclude = ('password', 'groups', 'user_permissions')

class ResetPwdSerializer(serializers.Serializer):
    oldpwd = serializers.CharField(min_length=6, max_length=20)
    newpwd1 = serializers.CharField(min_length=6, max_length=20)
    newpwd2 = serializers.CharField(min_length=6, max_length=20)

    def validate(self, attrs):
        oldpwd = attrs.get('oldpwd')
        newpwd1 = attrs.get('newpwd1')
        newpwd2 = attrs.get('newpwd2')

        user = self.context['request'].user
        if not user.check_password(oldpwd):
            raise exceptions.ValidationError('旧密码错误')

        if newpwd1 != newpwd2:
            raise exceptions.ValidationError('密码不一致')
        return attrs