# Django+bootstrap+极验验证码实现登陆注册的动态认证+用户名可以为邮箱/手机号登多层认证

## 功能实现效果
**登陆+滑动验证码**  
![登陆验证.gif](https://i.loli.net/2019/01/28/5c4e87ec13baf.gif)  
**注册+动态验证**  
![注册验证.gif](https://i.loli.net/2019/01/28/5c4e88135c45c.gif)  


## 组件使用方法
### 0.去极验验证码官网注册账号，获取ID和KEY
### 1.拷贝该users文件夹到你的Django根目录下或存放所有APP文件夹下
### 2.修改配置文件settings.py，把该app注册到INSTALLED_APPS中
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'web.apps.WebConfig',
    # 步骤一：注册users
    'users',
]
```  
### 3.settings.py配置组件必备的设置
```
############步骤二：配置文件################
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# 如果要使用该组件自带的用户表，则配置AUTH_USER_MODEL
AUTH_USER_MODEL = "users.UserInfo"

############后台认证顺序及自定义方法###############
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # 自带User的username和password认证
    'users.backends.LoginBackend',  # 自定义认证(添加邮箱/手机号认证)
)

###########极验滑动验证码自行去官网注册################
PC_GEETEST_ID = "66xxxxxxxxxxxxxxxxxxxxxxxxxxx8093"  # ID
PC_GEETEST_KEY = "828xxxxxxxxxxxxxxxxxxxxxxxxxea41"  # KEY
```
### 4.给组件设置路由
在项目根urls设置  
```
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    # 步骤三：生成路由
    re_path('users/', include('users.urls'))
]
```  
### 5.根据自身情况设置UserInfo模型，可以使用我给你提供的
```
# 步骤四：可自定义用户字段，也可以直接使用，需去掉abstract=True，avatar需自行在settings.py中配置MEDIA路径
class UserInfo(AbstractUser):
    gender_choices = (
        (1, "未知"),
        (2, "男"),
        (3, "女"),
    )

    nickname = models.CharField(verbose_name="昵称", max_length=32, blank=True, null=True)
    # avatar = models.ImageField(verbose_name="头像", upload_to="avatars/", default="/avatars/default.png")
    tel = models.IntegerField(verbose_name="电话", unique=True, blank=True, null=True)
    gender = models.IntegerField(verbose_name="性别", choices=gender_choices, default=1)
    email = models.EmailField('邮箱', unique=True, error_messages={'unique': "该邮箱地址已被占用。", }, )  # 重写auth_user的email
    departs = models.ForeignKey(to=Depart, on_delete=models.CASCADE, blank=True, null=True)  # 设置外键一定要设置, blank=True, null=True



    def __str__(self):
        return self.username

    class Meta:
        ordering = ['-id']
        # abstract = True  #可自行修改该模型用来继承还是直接使用自行修改字段
```  

