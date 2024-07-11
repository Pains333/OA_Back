# 名字：Pains
# 时间：2024/6/18 09:05

from django.core.management.base import BaseCommand
from apps.oaauth.models import OAUser, OADepartment

class Command(BaseCommand):
    def handle(self, *args, **options):
        boarder = OADepartment.objects.get(name='董事会')
        developer = OADepartment.objects.get(name='产品开发部')
        operator = OADepartment.objects.get(name='运营部')
        saler = OADepartment.objects.get(name='销售部')
        hr = OADepartment.objects.get(name='人事部')
        finance = OADepartment.objects.get(name='财务部')


        # 董事会的员工都是superuser
        dongdong = OAUser.objects.create_superuser(email='dongdong@qq.com', realname='东东', password='111111', department=boarder)
        duoduo = OAUser.objects.create_superuser(email='duoduo@qq.com', realname='多多', password='111111', department=boarder)
        zhangsan = OAUser.objects.create_user(email='zhangsan@qq.com', realname='张三', password='111111', department=developer)
        lisi = OAUser.objects.create_user(email='lisi@qq.com', realname='李四', password='111111', department=operator)
        wangwu = OAUser.objects.create_user(email='wangwu@qq.com', realname='王五', password='111111', department=saler)
        zhaoliu = OAUser.objects.create_user(email='zhaoliu@qq.com', realname='赵六', password='111111', department=hr)
        sunqi = OAUser.objects.create_user(email='sunqi@qq.com', realname='孙七', password='111111', department=finance)

        # 给部门指定leader和manager
        boarder.leader = dongdong
        boarder.manager = dongdong

        developer.leader = zhangsan
        developer.manager = dongdong

        operator.leader = lisi
        operator.manager = dongdong

        saler.leader = wangwu
        saler.manager = dongdong

        hr.leader = zhaoliu
        hr.manager = duoduo

        finance.leader = sunqi
        finance.manager = duoduo

        boarder.save()
        developer.save()
        operator.save()
        saler.save()
        hr.save()
        finance.save()

        self.stdout.write('初始用户创建成功')