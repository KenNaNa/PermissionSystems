1. 清空rbac/migrations目录下的文件（除__init__.py以外）

2. 业务的用户表和权限的用户表OneToOne关联(扩展rbac里的用户表)，如：
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
                (1,'男'),
                (2,'女'),
            )
            gender = models.IntegerField(choices=gender_choices)


记得要生存数据库表之前要配置settings.py注册app
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01.apps.App01Config',
    'rbac.apps.RbacConfig',
]
生产数据库表
python manage.py makemigrations
python manage.py migrate

2.5. 录入权限信息



3. 用户登录成功之后，初始化权限和菜单信息
    init_permission(权限的用户表对象,request)

    settings.py加入权限相关的配置：
        PERMISSION_SESSION_KEY = "xxxxxxxxx"
        MENU_SESSION_KEY = "sdf3sdfsdfsad"

4. 对用户请求的url进行权限的验证
    应用中间件：
        MIDDLEWARE = [
            'django.middleware.security.SecurityMiddleware',
             ...
            'rbac.middlewares.rbac.RbacMiddleware',
        ]

    PS： 只要通过验证，在视图函数的request中 permission_codes字段： [list,add,edit,del....]
         如果想要面向对象方式，需要
            from rbac.permission.base import BasePermission


            def users(request):
                # 增删改查
                per = BasePermission(request.permission_codes)
                return render(request,'users.html',{'per':per})


            users.html
                {% if per.add %}
                    <a>添加</a>
                {% endif %}

                <table border="1">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>姓名</th>
                            <th>操作</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>六五</td>
                            <td>
                                {% if per.edit %}
                                    <a>编辑</a>
                                {% endif %}
                                 {% if per.delete %}
                                    <a>删除</a>
                                {% endif %}

                            </td>
                        </tr>

                    </tbody>

                </table>


5. 动态菜单
    在Html模板中引入：

        {% load rbac %}

        引入样式
        <link rel='stylesheet' href='/static/rbac/rbac.css' />
        <script src='/static/rbac/rbac.js' />

        {% menu request %}

    推荐：放到母板中。


6. 白名单
    setting.py

        PERMISSION_VALID_URL = [
            '/login/',
            '/admin/.*',
        ]











