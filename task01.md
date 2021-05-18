# 前言

本节课程，你将熟悉后端目录结构、数据库关系映射及API实现方式，并使用OpenAPI编写RESTful接口。

# 后端目录结构

后端使用Django开发，子目录为`backend`。该目录通过命令`django-admin startproject bluewhale`创建，
然后重命名为`backend`，Django项目由一个或多个应用组成。详细的目录结构如下：

```shell
├── Pipfile
├── Pipfile.lock
├── manage.py
├── bluewhale
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── blog
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── common
│   ├── __init__.py
│   └── utils.py
├── core
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── views.py
│   └── viewsets.py
```

其中
* `manage.py`是服务入口，通过该脚本可以与Django项目进行交互。通过运行`python manage.py`可以看到支持的命令，
常用的命令有
  - `runserver` 启动后端服务
  - `makemigrations` 生成数据库迁移脚本
  - `migrate` 更新数据库schema
* `bluewhale`为项目目录，主要包括配置及后端路由
  - `settings.py` 项目配置，包括应用配置、中间件、数据库、缓存、日志等
  - `urls.py` URL与View的关联配置，通过`urlpatterns`配置URL至处理函数或者类的映射关系
  - `wsgi.py`及`asgi.py` 使用WSGI或ASGI入口部署应用
* `blog` & `core` 应用目录，使用`python manage.py startapp <APP_NAME>`创建的应用，创建后的应用会在DB中有
独立的表前缀，如需加载应用，需在`bluewhale/settings.py`中的添加，参考目前的配置：
    ```python
    INSTALLED_APPS = [
        # ...
        'core',
        'blog'
    ]
    ```

    其中的关键文件如下：

    - `admin.py` - 注册model至`django admin`应用（本次课程不涉及）
    - `apps.py` - app级别配置文件
    - `models.py` - 数据库对象关系映射
    - `tests.py` - 测试
    - `views.py` - Views，展示相关
    - `migrations` - 自动生成的数据库表迁移脚本


# 服务及接口

当前基础代码包含两个App，`core`与`blog`。其中core为核心App，负责处理认证与权限相关功能；blog为博客应用，
负责文章管理等功能。对应的接口定义如下（在文件`bluewhale/urls.py`中定义）：

```python
urlpatterns = [
    path(f'{api_prefix}/login', BluewhaleLoginView.as_view(), name='rest_login'),
    path(f'{api_prefix}/logout', LogoutView.as_view(), name='rest_logout'),
    path(f'{api_prefix}/send-verification', send_verification_mail, name='send verification mail'),
    path(f'{api_prefix}/verify/<token>', verify_verification_token, name='verify verification token'),
    path(f'{api_prefix}/register', register, name='register'),
    path(f'{api_prefix}/me', get_user_info, name='user profile'),

    path(f'{api_prefix}/articles', ArticleListCreateView.as_view(), name='articles'),
    path(f'{api_prefix}/articles/<pk>', ArticleDetailView.as_view(), name='article'),
]
```

其中前6个接口为登录、登出及用户注册相关接口，后两个为文章管理相关接口。

在开发模式下，直接访问[http://127.0.0.1:8000/](http://127.0.0.1:8000/)可以通过页面看到支持的接口列表：

![api list](./images/task01-api-list.png)

## 用户相关Model及数据表

### User Model

我们使用自定义的用户Model来处理用户相关属性（参考`settings.py`中的`AUTH_USER_MODEL = 'core.User'`）。具体定义如下：

```python
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone'), max_length=30, blank=True, unique=True, null=True)
    nickname = models.CharField(_('nickname'), max_length=150, blank=True)
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as active. '
                    'Unselect this instead of deleting accounts.'),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    description = models.TextField(_('description'), blank=True)
    last_login_ip = models.CharField(_('last login ip'), max_length=64, blank=True)
```

该Model类继承了两个父类，其中`AbstractBaseUser`定义了如下用户属性：
* `password` - 密码
* `last_login` - 上次登录时间

`PermissionsMixin`定了如下属性及映射关系：
* `is_superuser` - 是否为超级管理员
* `groups` - User与Group的关系（多对多）
* `user_permissions` - User与Permission的关系（多对多）

User本身定义了如下属性：
* `email` - 邮箱，登录凭证
* `phone` - 手机号
* `nickname` - 昵称
* `is_active` - 是否可用
* `date_joined` - 加入时间
* `description` - 描述
* `last_login_ip` - 上次登录IP地址

最终在数据库中的呈现如下：

```
MariaDB bluewhale@(none):bluewhale> desc core_user;
+---------------+--------------+------+-----+---------+----------------+
| Field         | Type         | Null | Key | Default | Extra          |
+---------------+--------------+------+-----+---------+----------------+
| id            | int(11)      | NO   | PRI | <null>  | auto_increment |
| password      | varchar(128) | NO   |     | <null>  |                |
| last_login    | datetime(6)  | YES  |     | <null>  |                |
| is_superuser  | tinyint(1)   | NO   |     | <null>  |                |
| email         | varchar(254) | NO   | UNI | <null>  |                |
| phone         | varchar(30)  | YES  | UNI | <null>  |                |
| nickname      | varchar(150) | NO   |     | <null>  |                |
| is_active     | tinyint(1)   | NO   |     | <null>  |                |
| date_joined   | datetime(6)  | NO   |     | <null>  |                |
| description   | longtext     | NO   |     | <null>  |                |
| last_login_ip | varchar(64)  | NO   |     | <null>  |                |
+---------------+--------------+------+-----+---------+----------------+
```

你可以在该表中找到上个课程中创建的初始超级管理员。

![db superuser](./images/task01-db-superuser.png)

### 数据表

用户、组及权限相关的数据表如下：

```
+----------------------------+
| Tables_in_bluewhale        |
+----------------------------+
| auth_group                 |
| auth_group_permissions     |
| auth_permission            |
| core_user                  |
| core_user_groups           |
| core_user_user_permissions |
+----------------------------+
```

其中`auth_`前缀的对应Django自带的auth应用，`core_`前缀的对应之前提及的core应用。
该6个表中，`core_user`, `auth_group`, `auth_permission`为基础表，
`auth_group_permissions`, `core_user_groups`, `core_user_user_permissions`为基础表的关联关系表。

在后续的课程中，你需要对User的属性进行扩展，并使用`migrate`命令处理数据库相关的操作。

# OpenAPI接口编写

## 查看已有接口

Django REST Framework 本身提供方便的工具可以查看已有接口的返回内容。如请求
[http://127.0.0.1:8000/api/v1/me](http://127.0.0.1:8000/api/v1/me)你将看到如下界面

![DRF api page](./images/task01-drf-api-page.png)

该界面展示了`/api/v1/me`接口的返回信息，包括返回的状态码，允许的HTTP Method，Content-Type，
返回的JSON内容等。

在上个课程中，我们简单介绍了OpenAPI相关规范。在我们的初始项目中，已经添加了初始的接口规范：[openapi.yaml](./openapi.yaml)

我们可以通过如下几种方式对该接口规范文档进行编辑：

### VS Code插件（推荐）
在VS Code插件面板中搜索*swagger*，安装*OpenAPI(Swagger)Editor*。

在VS Code编辑器中打开`openapi.yaml`，点击左侧API图标，会展示当前API规范的大纲。点击右上角预览按钮，可以对API规范文档
进行预览。入下图所示

![VS Code Swagger Editor](./images/task01-vscode-swagger.png)

### 官方编辑器

我们可以使用官方提供的工具[swagger-editor](https://github.com/swagger-api/swagger-editor)对文档进行编辑。

* 首先下载docker镜像`docker pull swaggerapi/swagger-editor`
* 在本地仓库根目录运行镜像：

`docker run -d -p 80:8080 -v $(pwd):/tmp -e SWAGGER_FILE=/tmp/openapi.yaml swaggerapi/swagger-editor`

该命令表示以80端口启动swagger editor，并将当前目录映射至镜像中的`/tmp`目录，`-e`参数表示设置环境变量。

镜像启动后，打开浏览器[http://127.0.0.1/](http://127.0.0.1/)，我们将看到如下页面：

![Swagger Editor UI](./images/task01-swagger-editor-ui.png)

页面左边为`openapi.yaml`的内容，右边为解析后的接口呈现。可以看到目前已经定义了5个API接口，包括其HTTP方法、URL Path、
返回格式等内容。
### 编辑示例
编写openapi 文档涉及以下步骤：

1、明确接口需求，如 我们需要查询文章列表，在最近文章页面里展示

2、设计请求url、请求参数、响应内容，这里为了让小伙伴们先熟悉openapi已经做好了接口设计，大家可以在此基础上修改调整（开发中需要前后端根据需求协商确定url、属性名、类型等接口信息）

> 可以在前端浏览器，如chrome 快捷键F12打开web调试器 查看已提供的接口请求和响应信息

![Swagger Editor openapi01](./images/task01-openapi-edit01.png)

![Swagger Editor openapi02](./images/task01-openapi-edit02.png)

3、打开编辑器，如swagger editor,编辑器或者插件提供了一些便捷操作辅助我们编写，这里我们先插入path
![Swagger Editor openapi03](./images/task01-openapi-edit03.png)

4、再添加操作
![Swagger Editor openapi04](./images/task01-openapi-edit04.png)

5、添加响应信息
![Swagger Editor openapi05](./images/task01-openapi-edit05.png)
> 为了结构清晰和数据复用（相同的内容可以用$ref引用）,我们在 components.schemas 下创建 响应对象

![Swagger Editor openapi07](./images/task01-openapi-edit07.png)

6、参考其他接口或者openapi规范 手动调整一下接口，如添加参数等
![Swagger Editor openapi06](./images/task01-openapi-edit06.png)
> 编写时注意yaml语法、tab空格对齐

7、尝试执行，如果响应如期正常返回就编写完成了(需要启动运行 mock server 加载编写好的openapi.yaml，运行mock server的方法下面有讲到)
![Swagger Editor openapi08](./images/task01-openapi-edit08.png)

### 其他

对于已有的接口如`/api/v1/send-verification`，本身不存在增删改查的概念，只是纯粹的接口。我们可以通过
查看代码确认请求路径、HTTP方法、请求体、返回值等数据。

其URL路径在`backend/bluewhale/urls.py`中定义：

```Python
path(f'{api_prefix}/send-verification', send_verification_mail, name='send verification mail'),
```

对应调用函数为`backend/core/views_auth.py`中的函数`send_verification_mail`：

```Python
@api_view(['POST'])
def send_verification_mail(request):
    data = request.data
    email = data.get('email')
    # Method BODY
    return Response({"data": result, "code": 0})
```

其中装饰器`api_view`是Django REST Framework提供的函数，参数`POST`表示该函数只接受`HTTP POST`方法，
对应`openapi.yaml`中的`post`入口。

函数实现中先获取请求体中的`email`属性，对应`openapi.yaml`中的`SendVerificationForm`结构体。

发送邮件后返回`Response({"data": result, "code": 0})`实例，对应`openapi.yaml`中的`responses`结构体。

具体映射如图：

![API vs openapi.yaml](./images/task01-api-request-response.png)

在task00中搭建的环境里面，我们可以通过界面来观察浏览器发送的请求和接收的数据：

![API in browser](./images/task01-api-send-verification.png)

## 运行mock server

当我们完成OpenAPI的接口规范编写后，我们可以通过工具将接口规范文档转成mock server提供给前端开发使用。

将目录切换至client目录（前端目录），运行命令`npm run mock`，可以看到如下输出：

![mock server](./images/task01-mock-server.png)

该图表明我们在`http://127.0.0.1:4010`地址启动了mock server，并且列出了我们已经编写的5个API接口。

在之前的Swagger Editor页面中，点击其中一个接口（如`/api/v1/me`），点击**Try it out** - **Execute**，Swagger Editor
将请求mock server接口，展示mock server的请求返回信息等，如下：

![swagger server access](./images/task01-swagger-server-access.png)

除此之外，我们还可以通过命令行工具`curl`或者应用[Postman](https://www.postman.com/)模拟HTTP请求进行验证。


# 任务

本期课程任务为完成剩余已实现的接口文档的编写：

* ~~`api/v1/verify/<token> [name='verify verification token']`~~ (涉及邮件发送，取消)
* ~~`api/v1/register [name='register']`~~ （涉及邮件发送，取消）
* `api/v1/articles [name='articles']`
* `api/v1/articles/<pk> [name='article']`

完成接口规范文档的编写后，重启mock server。并可以通过运行下面命令，使前端项目以mock server为接口进行启动：

`API_PORT=4010 npm run serve`

## 参考结果

要编写的数据接口，涉及两种类型，一种为单路径的纯API（注册相关），另外一种为RESTful风格API（article相关）。

注册相关接口涉及邮件发送等环节，不做要求，在openapi.yaml中给出了参考的API写法。

article相关接口涉及RESTful中的资源的概念，这里资源指的是类似用户、组、文章等实体，在一般的web场景中，我们一般
会对这些资源进行**增删改查**的操作。

比如在文章article的场景中，我们有如下几种操作：
* 获取当前文章列表 - 查
* 写一篇新文章 - 增
* 获取单个文章内容 - 查
* 编辑一篇文章 - 改
* 移除一篇文章 - 删

我们把article当做一个集合，前两个动作针对的是集合（向集合中新增元素、查询集合所有元素），后三个动作针对的是集合中的
个体（获取集合中的某个元素、修改某个元素、删除某个元素）。所以我们在定义相关RESTful接口时，需要两种资源（对应两种URL PATH）：
* `artitles` - 集合
* `artitles/<primary_key>` - 集合中的元素

对应的，我们可以在后端URL设置代码`bluewhale/urls.py`中找到相关的资源定义：

```python
    path(f'{api_prefix}/articles', ArticleListCreateView.as_view(), name='articles'),
    path(f'{api_prefix}/articles/<pk>', ArticleDetailView.as_view(), name='article'),
```

具体代码的实现细节可以参考代码`backend/core/generics.py`中的两个类及其父类`ListCreateAPIView` & `RetrieveUpdateDestroyAPIView`

针对这两种资源，我们可以在`openapi.yaml`文档中新增两个入口path：
* `/api/v1/articles`
* `/api/v1/articles/{pk}`

在集合的资源下面，新增两类方法`get` & `post`用来表示获取列表及向集合中新增元素，
在单元素的资源下面，新增三类方法`get` & `put` & `delete`，表示对单个资源的读取、修改与删除。

> 这里有个很常见的误区，就是将对资源的操作比如增删改写到URL路径中，如`/api/v1/articles/get`及`/api/v1/articles/delete`，
> 正确的做法是只在PATH中定义资源，而把对资源的操作方式通过HTTP Method来表达（参考task00中关于REST的描述及介绍：
>[https://github.com/datawhalechina/whale-web/blob/master/task00.md#rest%E7%AE%80%E4%BB%8B](REST简介)）。

具体API的定义请参考`openapi.yaml`中对应的article相关入口。