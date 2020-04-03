# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/4/2 21:04
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
# -*- encoding: utf-8 -*-
"""
@File    : fastapi_admin.py
@Time    : 2020/4/2 21:04
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :主函数,
"""
from fastapi import APIRouter
from typing import Optional, Union, List, Any, Set
import databases

# __router = APIRouter()
from pydantic import BaseModel, Field
from sqlalchemy import Integer

from .views import BaseView


def create_schema(model):
    """通过读取model的信息，创建schema"""
    base_model: str = """
class {}(BaseModel):
{}
    class Config:
       orm_mode = True
"""
    model_name = model.__name__
    # mappings为从model获取的相关配置
    __mappings__ = {}  # {'name':{'field':Field,'type':type,}}

    for filed in model.__table__.c:
        filed_name = str(filed).split('.')[-1]

        if filed.default:
            if isinstance(filed.default.arg,str):
                default_value = '"'+ filed.default.arg+'"'
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
        res_field = 'Field({}, description="{}")'.format(default_value,filed.description)  # Field参数

        if isinstance(filed.type, Integer):
            tp = filed_name+':int='+res_field
        else:
            tp = filed_name+ ':str='+res_field
        __mappings__[filed_name] = tp
    s_fields=''
    for k,v in __mappings__.items():
        s_fields=s_fields+'    '+v+'\n'
    base_model=base_model.format(model_name,s_fields)
    cls_dict = {"BaseModel": BaseModel,"Field":Field}
    print(base_model)
    exec (base_model, cls_dict)
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

    def __init__(self, router: APIRouter, database_connectinfo: str):
        """
        创建的时候，注册__router,
        传递数据的链接方式，独立连接，使用异步方式。
         database_connectinfo数据库连接方式
        """
        # 注册
        # router.include_router(self.__router,prefix='/admin',tags=['admin'])
        self.__router=router
        self.database = databases.Database(database_connectinfo)

    def register_Model(self, model: Any, methods: Union[List[str], Set[str]] = ('GET', 'POST', 'PUT', 'DELETE'),
                       fields: Union[str, List[str]] = "__all__",
                       list_display: Union[str, List[str]] = "__all__", put_fields: Optional[List[str]] = None) -> bool:
        """
        注册model到路由,
        :param model: sqlalchemy的model
        :param methods: 允许访问的方法
        :param fields:  post的字段，默认为所有字段，如果需要
        :param list_display: 显示在列表的字段
        :param put_fields: put允许的字段，默认为fields相同
        :return:是否注册成功
        """
        res_schema=create_schema(model)
        print("类型：",isinstance(res_schema,BaseModel))
        view=BaseView(model,self.database,res_schema)
        #注册一个专门的蓝图
        router=APIRouter()
        router.on_event('startup')(view.startup)
        router.on_event('shutdown')(view.shutdown)
        router.get('/'+res_schema.__name__,response_model=List[res_schema])(view.list)
        router.post('/' + res_schema.__name__ )(view.create)
        router.put('/' + res_schema.__name__  )(view.update)
        router.delete('/' + res_schema.__name__ )(view.delete)
        self.__router.include_router(router, prefix='/admin', tags=['admin'])
    def register_Table(self):
        """注册Table到路由，功能和register_Model一致"""
        pass