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
from pydantic import BaseModel, Field
from sqlalchemy import Integer, Boolean

from .auth.views import login, create_create
from .databaseManage import AdminDatabase
from .views import BaseView
from typing import Optional
from .auth.models import User, Group, Permission
from .auth.schemas import Token


def create_schema(model, exclude: Optional[List[str]] = None, ):
    """
    通过读取model的信息，创建schema
    :param model:
    :param exclude:
    :return:
    """

    base_model: str = """
class {}(BaseModel):
{}
    """
    model_name = model.__name__
    # mappings为从model获取的相关配置
    __mappings__ = {}  # {'name':{'field':Field,'type':type,}}
    for filed in model.__table__.c:
        filed_name = str(filed).split('.')[-1]
        if exclude:
            if exclude.count(filed_name):
                continue

        if filed.default:
            if isinstance(filed.default.arg, str):
                default_value = '"' + filed.default.arg + '"'
            # elif isinstance(filed.default.arg,bool):
            #     default_value = str(filed.default.arg)
            else:
                default_value = str(filed.default.arg)
        elif filed.nullable:
            default_value = '...'
        else:
            default_value = 'None'
        # 生成的结构： id:int=Field(...,)大概这样的结构
        # res_field = Field(default_value, description=filed.description)  # Field参数
        res_field = 'Field({}, description="{}")'.format(default_value, filed.description)  # Field参数

        if isinstance(filed.type, Integer):
            tp = filed_name + ':int=' + res_field
        elif isinstance(filed.type, Boolean):
            tp = filed_name + ":bool =" + res_field
        else:
            tp = filed_name + ':str=' + res_field
        __mappings__[filed_name] = tp
    s_fields = ''
    for k, v in __mappings__.items():
        s_fields = s_fields + '    ' + v + '\n'
    base_model = base_model.format(model_name, s_fields)
    cls_dict = {"BaseModel": BaseModel, "Field": Field}
    exec(base_model, cls_dict)
    # 将schema绑定到model
    return cls_dict[model_name]


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
        router.post('/token', response_model=Token)(login)
        # 注册基础的model
        # self.register_Model(User, need_user=False)
        use_schema = create_schema(User)
        view = BaseView(model=User, database=self.database, schema=use_schema, need_user=False)
        view.create = create_create(User, self.database)
        self.register_view(view, prefix="/user")
        self.register_Model(Group, need_user=True)
        self.register_Model(Permission, need_user=True)

    def register_Model(self, model: Any, view=None,
                       methods: Union[List[str], Set[str]] = ('GET', 'Retrieve', 'POST', 'PUT', 'DELETE'),
                       fields: Union[str, List[str]] = "__all__",
                       list_display: Union[str, List[str]] = "__all__", put_fields: Optional[List[str]] = None,
                       need_user=False, depends=None) -> bool:
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
        res_schema = create_schema(model)
        print("类型：", isinstance(res_schema, BaseModel))
        if not view:
            view = BaseView(model=model, database=self.database, schema=res_schema, need_user=need_user)
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
            router.get(prefix, tags=tags)(view.list)
        if methods.count('Retrieve'):
            router.get(prefix + "/{id}", tags=tags)(view.retrieve)
        if methods.count('POST'):
            router.post(prefix, tags=tags)(view.create)
        if methods.count('PUT'):
            router.put(prefix + "/{id}", tags=tags)(view.update)
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
                self.__router.get(prefix, response_model=List[res_model])(func)
            else:
                self.__router.get(prefix,)(func)
        else:
            self.__router.post(prefix, )(func)
