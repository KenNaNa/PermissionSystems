from django.contrib import admin

from . import models

class PermissionCongfig(admin.ModelAdmin):
    list_display = ['title','url','group','code']

admin.site.register(models.Permission,PermissionCongfig)


admin.site.register(models.Role)
admin.site.register(models.UserInfo)
