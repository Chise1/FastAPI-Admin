# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/4/2 21:04
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import APIRouter
from typing import Union, List, Any, Set
from .auth.views import login, create_create, create_superuser
from .databaseManage import AdminDatabase
from .publicDepends.paging_query import get_res_schema, page_query
from .views import create_View, method_get_func
from typing import Optional
from .auth.models import User, Group, Permission, UserLog
from .auth.schemas import Token
from .schema_tools import create_schema
from .config.schemas import BaseConfig
from .config.models import Config
from .views.methods_get import model_get_func_fetch_one


class FastAPIAdmin:
    """
    该类为核心类，主要功能是注册Model或者Table，生成对应的schema和路由
    组装View，Model和schema
    """
    _instance = None
    # 单例模式的路由，所有的方法都会在这个路由注册，这个路由在初始化的时候注册到app
    __router = None
    # 存储已经注册了的Table
    table = []
    # 注册的所有schema，保证不要重复注册
    schema = []
    # 暂时这么命名，存储生成的类视图，
    api_class = []

    def __new__(cls, *args, **kwargs):
        """要求这个类是单例模式，保证只注册一次"""
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_database(self):
        """创建数据库"""
        self.admin_database.create_all()

    def __init__(self, router: APIRouter, database_url: str):
        """
        创建的时候，注册__router,
        传递数据的链接方式，独立连接，使用异步方式。
         database_connectinfo数据库连接方式
        """
        # 注册
        # router.include_router(self.__router,prefix='/admin',tags=['admin'])
        self.__router = router
        self.admin_database = AdminDatabase(database_url=database_url)
        # 需要创建数据库的时候
        # self.admin_database.create_all()
        self.database = self.admin_database.database
        router.on_event('startup')(self.admin_database.startup)
        router.on_event('shutdown')(self.admin_database.shutdown)
        # 注册login
        self.default_registe()

    def register_Model(self, model: Any, view=None,
                       methods: Union[List[str], Set[str]] = ('GET', 'Retrieve', 'POST', 'PUT', 'DELETE'),
                       schema=None,
                       schema_noid=None,
                       fields: Union[str, List[str]] = "__all__",
                       list_display: Union[str, List[str]] = "__all__", put_fields: Optional[List[str]] = None,
                       need_user=False, get_need_user=False, depends=None) -> bool:
        """
        注册model到路由,
        :param model: sqlalchemy的model
        :param view: 自定义View类
        :param methods: 允许访问的方法
        :param fields:  post的字段，默认为所有字段，如果需要
        :param list_display: 显示在列表的字段
        :param put_fields: put允许的字段，默认为fields相同
        :return:是否注册成功
        """

        __schema, __schema_noid = create_schema(model)
        if not schema:
            schema = __schema
        if not schema_noid:
            schema_noid = __schema_noid
        if not view:
            view = create_View(model=model, database=self.database, schema=schema, schema_noid=schema_noid,
                               need_user=need_user, get_need_user=get_need_user)
        else:
            view.database = self.database
        # 注册一个专门的蓝图
        self.register_view(view, "/" + model.__name__, methods=methods, depends=depends)
        return True

    def register_view(self, view, prefix=None,
                      methods: Union[List[str], Set[str]] = ('GET', 'Retrieve', 'POST', 'PUT', 'DELETE'), tags=None,
                      depends=None):
        """
        如果不使用自定义的，则需要methods为None
        :param view:
        :param prefix:
        :param methods:
        :param tags:
        :return:
        """
        router = APIRouter()
        if not prefix:
            prefix = "/" + view.__class__.__name__
        if not tags:
            tags = [prefix[1:]]
        if not methods:
            methods = view.methods
        if methods.count('GET'):
            # print("注意，可能需要设置返回model")
            # get_res_model = get_res_schema(view.schema)
            router.get(prefix, tags=tags, )(view.list)
        if methods.count('Retrieve'):
            router.get(prefix + "/{id}", tags=tags, )(view.retrieve)
        if methods.count('POST'):
            router.post(prefix, tags=tags, )(view.create)
        if methods.count('PUT'):
            router.put(prefix, tags=tags, )(view.update)
        if methods.count('DELETE'):
            router.delete(prefix + "/{id}", tags=tags)(view.delete)
        self.__router.include_router(router, prefix='/admin')

    def register_router(self, func, method, prefix, res_model=None, tags=None, ):
        """
        注册路由
        :param func:函数
        :param method: method方法
        :param prefix: 路由
        :param res_model: 模型
        :param tags: 标签
        :return:
        """
        if method == 'GET':
            if res_model:
                self.__router.get(prefix, response_model=res_model)(func)
            else:
                self.__router.get(prefix, )(func)
        else:
            if res_model:
                self.__router.post(prefix, response_model=res_model)(func)
            else:
                self.__router.post(prefix, )(func)

    def default_registe(self):
        """
        默认需要注释的
        :return:
        """
        # 注册login
        self.__router.post('/user/login', response_model=Token)(login)
        schema, schema_noid = create_schema(User)
        view = create_View(model=User, database=self.database, schema=schema, schema_noid=schema_noid, need_user=True,
                           get_need_user=True)
        view.create = create_create(User, self.database)
        # user_list,user_list model_get_func_fetch_one
        # view.delete=
        # self.register_view(view, prefix="/user", methods=['GET', "Retrieve", "PUT", "POST",'DELETE'])
        self.register_Model(Group, need_user=True, get_need_user=True)
        self.register_Model(Permission, need_user=True, get_need_user=True)
        self.register_Model(UserLog, methods=['GET'], need_user=True, get_need_user=True)
        from .config.views import config_update, BaseConfig, email_config_update, EmailConfig
        # self.register_router(create_create,method="POST",prefix="/user/createUser",)
        self.register_router(config_update, method="PUT", prefix="/config/baseconfig", )
        self.register_router(email_config_update, method="PUT", prefix="/config/emailconfig", )
        baseconfig_func, baseconfig_schema = model_get_func_fetch_one(Config, "BaseConfig", need_user=False)
        emailconfig_func, email_config_schema = model_get_func_fetch_one(Config, "EmailConfig",
                                                                         fields=["smtp_host", "smtp_port", "smtp_email",
                                                                                 "smtp_email_password"], need_user=True)
        self.register_router(baseconfig_func, method="GET", prefix="/config/baseconfig", res_model=BaseConfig, )
        self.register_router(emailconfig_func, method="GET", prefix="/config/emailconfig", res_model=EmailConfig)
