# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/4/4 18:40
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import math

from sqlalchemy import select, func

from .methods_get import model_get_list_func
from .. import AdminDatabase
from ..auth.depends import get_current_active_user, create_current_active_user
from ..auth.models import User
from typing import List, Union, Set, Dict
from fastapi import Body, Depends, APIRouter

from ..publicDepends.paging_query import paging_query_depend, page_query
from ..schema_tool import create_page_schema, create_schema
from ..schema_tools import create_get_page_schema


def get_View(schema, schema_noid, database, need_user=False, get_need_user=False, **kwargs):
    class View:
        """该类为抽象类，需要继承并实现相关功能"""
        list_display: Union[List[str], str] = "__all__"
        methods: Union[List[str], Set[str]] = kwargs['methods']

        def __init__(self, model, database, schema, schema_noid, **kwargs):
            """
            初始化基于类的视图,
                注意：可以先初始化，并实现所有的功能之后，在调用之前一定要将model、database、schema补齐
            :param model: 操作的sqlalchemy的Model
            :param database: 操作数据库的database
            :param schema: 用作数据验证的schema
            """
            self.model = model
            self.table = model.__table__
            self.database = database
            self.schema = schema
            self.schema_noid = schema_noid
            self.page_list_schema = create_get_page_schema(model, )
            for k, v in kwargs.items():
                setattr(self, k, v)

        async def update(self, instance: schema = Body(..., ),
                         current_user: User = Depends(create_current_active_user(need_user))):

            query = self.table.update().where(self.model.id == instance.id).values(**dict(instance))
            print(query)
            await database.execute(query)
            return instance

        async def create(self, instance: schema_noid = Body(..., ),
                         current_user: User = Depends(create_current_active_user(need_user))):

            query = self.table.insert().values(dict(instance))
            res_id = await database.execute(query)
            res = dict(instance)
            res.update({'id': res_id})
            return res

        def get_list_display(self) -> List[str]:
            """获取类对应要展示的数字,默认为list_display"""
            return self.list_display

        async def list(self, page: Dict[str, int] = Depends(paging_query_depend),
                       current_user: User = Depends(create_current_active_user(get_need_user))):
            """
            get
            :return:
            """
            if self.get_list_display() == "__all__":
                query = self.table.select().offset((page['page_number'] - 1) * page['page_size']).limit(
                    page['page_size'])  # 第一页，每页20条数据。 默认第一页。
            else:
                query = self.table.select(*self.get_list_display())
            paginate_obj = await self.database.fetch_all(query)
            query2 = select([func.count(self.table.c.id)])
            total_page = await AdminDatabase().database.fetch_val(query2)
            print("注意需要考虑查询两次的两倍代价")
            return {
                "page_count": int(math.ceil(total_page * 1.0 / page['page_size'])),
                "rows_total": total_page,
                "page_number": page['page_number'],
                "page_size": page['page_size'],
                "data": paginate_obj
            }

        async def retrieve(self, id, current_user: User = Depends(create_current_active_user(need_user))):
            """返回一个类型的详情"""
            query = self.table.select().where(self.model.id == id)
            return await self.database.fetch_one(query)

        async def delete(self, id, current_user: User = Depends(create_current_active_user(need_user))):
            query = self.table.delete().where(self.model.id == id)
            return await self.database.execute(query)

    return View


def create_View(model, schema, schema_noid=None, methods: Set[str] = ("GET", "PUT", "POST", "DELETE", "Retrieve"),
                database=None, need_user=False, get_need_user=False, **kwargs):
    """创建View的工厂方法"""
    if not schema_noid:
        schema_noid = schema
    return get_View(schema, schema_noid, database, need_user, methods=methods, get_need_user=get_need_user)(model,
                                                                                                            database,
                                                                                                            schema,
                                                                                                            schema_noid)


def method_get_func(model, fields="__all__", need_user=False, **kwargs):
    """生成一个model的get访问"""

    async def list(page: Dict[str, int] = Depends(paging_query_depend),
                   user: User = Depends(create_current_active_user(need_user))):
        """
        get
        :return:
        """
        table = model.__table__
        if fields == "__all__":
            query = table.select().offset((page['page_number'] - 1) * page['page_size']).limit(
                page['page_size'])  # 第一页，每页20条数据。 默认第一页。
        else:
            query = table.select([getattr(model.__table__.c, i) for i in fields]).offset(
                (page['page_number'] - 1) * page['page_size']).limit(
                page['page_size'])  # 第一页，每页20条数据。 默认第一页。
        paginate_obj = await AdminDatabase().database.fetch_all(query)
        query2 = select([func.count(table.c.id)])
        total_page = await AdminDatabase().database.fetch_val(query2)
        print("注意需要考虑查询两次的两倍代价")
        return {
            "page_count": int(math.ceil(total_page * 1.0 / page['page_size'])),
            "rows_total": total_page,
            "page_number": page['page_number'],
            "page_size": page['page_size'],
            "data": paginate_obj
        }

    return list


import uuid


    # params_dict = {
    #     "GET": {
    #         "description": "",  # 接口描述
    #         "prefix":"",
    #         "name": "接口名称",
    #         "schema_name": "cc",
    #         "need_user": False,
    #         "fields": {
    #             "id": {
    #                 "nullable": True,
    #                 "description": "abc",  # 自带描述
    #                 "type": "",  # schema的默认类型
    #                 "default": object,  # 也可以是None
    #                 "max_length": "",  # 只有type为str时有效
    #             }
    #         },
    #         'need_fields': [],  # 如果是多表查询，则必须为存储字典，分别为{表名:[字段列表]或__all__}
    #         "exclude": [],
    #         "sql": object,  # 也可以是字符串,也可以是sqlalchemy.sql，默认为fetchall，
    #         "use_page": True,  # 是否启动page分页功能，如果启动分页功能按照分页功能的方式显示，如果不是，则会获取第一条，所以一定要自己写sql
    #     }
    # }

    # for method in params_dict:
    #     if method == 'GET':
    #         config = params_dict['GET']
    #         method_description = config.get('description', None)
    #         method_name = config.get('name', None)
    #         method_need_user = config.get('need_user', False)
    #         for key,values in config.get('fields').items():
