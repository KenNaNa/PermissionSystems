from django.db import models
from rbac import models as rbac_model


class DepartMent(models.Model):
    """
    部门
    """
    title = models.CharField(max_length=32)


class User(models.Model):
    user_info = models.OneToOneField(to=rbac_model.UserInfo)
    nickname = models.CharField(max_length=32)
    momo = models.CharField(max_length=32)
    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(choices=gender_choices)