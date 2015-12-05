# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

# Create your models here.
# class PermissionList(models.Model):
#     """
#       ===============================================================================
#       function：    权限Model
#       developer:
#       add-time
#       ===============================================================================
#     """
#     name = models.CharField(max_length=64)
#     url = models.CharField(max_length=255)
#
#     def __unicode__(self):
#         return '%s(%s)' %(self.name,self.url)
#
#     class Meta:
#         db_table = 'permissionlist'
#
#
# class RoleList(models.Model):
#     """
#       ===============================================================================
#       function：
#       developer:
#       add-time
#       Note:         和permisslist是多对多关心
#       ===============================================================================
#     """
#     name = models.CharField(max_length=64)
#     permission = models.ManyToManyField(PermissionList,null=True,blank=True)
#
#     def __unicode__(self):
#         return self.name
#
#     class Meta:
#         db_table = 'rolelist'

class UserManager(BaseUserManager):
    """
      ===============================================================================
      function：    自定义用户管理
      developer:
      add-time
      Note:         继承了Django的用户管理
      ===============================================================================
    """

    def create_user(self, email, username, password=None, type=None, **kwargs):
        if not email:
            raise ValueError(u'用户必须要有邮箱')

        user = self.model(
            email=UserManager.normalize_email(email),
            username=username,
            type=type if type else 0
        )
        user.set_password(password)
        if kwargs:
            if kwargs.get('sex', None): user.sex = kwargs['sex']
            if kwargs.get('phone', None): user.phone = kwargs['phone']
            if kwargs.get('is_active', None): user.is_active = kwargs['is_active']
            if kwargs.get('is_admin', None): user.is_admin = kwargs['is_admin']
            if kwargs.get('sys_org_id', None): user.sys_org_id = kwargs['sys_org_id']
            if kwargs.get('openid', None): user.openid = kwargs['openid']
            if kwargs.get('access_token', None): user.access_token = kwargs['access_token']
            if kwargs.get('url', None): user.url = kwargs['url']
            if kwargs.get('desc', None): user.desc = kwargs['desc']
            if kwargs.get('avatar', None): user.avatar = kwargs['avatar']
            if kwargs.get('role_id',None):user.role_id=kwargs['role_id']

        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(email,
                                password=password,
                                username=username,
                                )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    """
      ===============================================================================
      function：    扩展用户管理
      developer:    Rich.Chen
      add-time      2015/10/3
      Note:         加上自己需要的用户字段
      ===============================================================================
    """

    ADMIN_CHOICE = (
        (True, u'是'),
        (False, u'不是'),
    )

    ACTIVE_CHOICE = (
        (True, u'在用'),
        (False, u'停用'),
    )
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True, db_index=True)
    username = models.CharField(max_length=50, unique=True, db_index=True)
    # is_active = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True, choices=ACTIVE_CHOICE)
    # is_admin = models.BooleanField(default=False)  # 公司管理员
    is_admin = models.BooleanField(default=False, choices=ADMIN_CHOICE)
    is_superuser = models.BooleanField(default=False)  # 超级管理员
    #sys_orgid = models.CharField(verbose_name='机构代码', max_length=64, null=True, blank=True)
    type = models.IntegerField(default=0)  # 类型，0本站，1微信登录
    sex = models.IntegerField(default=0)  # sex 0是男,1是女
    phone = models.CharField(max_length=50, null=True, blank=True)  # 电话号码
    openid = models.CharField(max_length=50, null=True, blank=True)  # 微信的OPenID
    access_token = models.CharField(max_length=100, null=True, blank=True)  # 微信的 access_token
    url = models.URLField(null=True)  # 个人站点
    desc = models.CharField(max_length=2000, null=True, blank=True)  # 个人信息简介
    avatar = models.ImageField(upload_to='avatar/', default='avatar/1.jpg')# 头像
    # role = models.ForeignKey(RoleList,null=True,blank=True)#角色对象
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'user'


class CustomAuth(object):
    """
      ===============================================================================
      function：    自定义过滤和权限认证
      developer:
      add-time
      Note:         在settings.py的文件上加入
                    AUTH_USER_MODEL = 'systemmanager.MyUser'
                    AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',
                    'systemmanager.models.CustomAuth')
      ===============================================================================
    """

    def authenticate(self, email=None, password=None):
        try:
            user = MyUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = MyUser.objects.get(pk=user_id)
            if user.is_active:
                return user
            return None
        except MyUser.DoesNotExist:
            return None


class Signal(models.Model):
    """
      ===============================================================================
      function：    用户公告
      developer:
      add-time
      Note:
      ===============================================================================
    """

    TYPE_CHOICES = (
        (0, u'系统公告'),
        (1, u'评论'),
        (2, u'私信'),
        (3, u'关注'),
        (4, u'主题关注'),
    )

    STATUS_CHOICES = (
        (0, u'未读'),
        (1, u'已读'),
        (2, u'删除'),
    )
    type = models.IntegerField(default=0, choices=TYPE_CHOICES)  # 0,系统公告；1:评论;2:私信;3.关注;4.主题关注
    obj = models.IntegerField(default=0)  # 对象id
    user = models.ForeignKey(settings.AUTH_USER_MODEL)  # 发布者
    who = models.IntegerField(default=0)  # 接受者
    title = models.CharField(max_length=200, null=True)  # 标题
    content = models.CharField(max_length=1000, null=True)  # 内容
    status = models.IntegerField(default=0, choices=STATUS_CHOICES)  # 状态，0，未读；1已读，2.删除
    add_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_signal'




