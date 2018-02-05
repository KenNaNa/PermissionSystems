from django.db import models

class Menu(models.Model):
    """
    菜单
    """
    title = models.CharField(max_length=32)


class PermissionGroup(models.Model):
    """
    权限组
    反向： permission_set
    反向： xx
    """
    caption = models.CharField(max_length=32)
    menu = models.ForeignKey(to='Menu',default=1)


    def __str__(self):
        return self.caption

class Permission(models.Model):
    """
    权限表
    """
    title = models.CharField(max_length=32)
    url = models.CharField(max_length=128)
    code = models.CharField(max_length=16,default='list')
    group = models.ForeignKey(to='PermissionGroup',default=1)
    # is_menu = models.BooleanField(default=False) # 权限是否可以在菜单中显示
    parent = models.ForeignKey(verbose_name='组内可以作为菜单的权限',to='Permission', null=True,related_name='xx')

    def __str__(self):
        return self.title

class Role(models.Model):
    """
    角色
    """
    title = models.CharField(max_length=32)
    permissions = models.ManyToManyField(to='Permission',blank=True)

    def __str__(self):
        return self.title

class UserInfo(models.Model):
    """
    用户表
    """
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=32)
    roles = models.ManyToManyField(to='Role')

    def __str__(self):
        return self.name


