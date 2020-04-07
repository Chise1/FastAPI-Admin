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

from .. import AdminDatabase
from ..auth.depends import get_current_active_user, create_current_active_user
from ..auth.models import User
from typing import List, Union, Set, Dict
from fastapi import Body, Depends

from ..publicDepends.paging_query import paging_query_depend

def get_View(schema, schema_noid, database, need_user=False, **kwargs):
    class View:
        """该类为抽象类，需要继承并实现相关功能"""
        list_display: Union[List[str], str] = "__all__"
        methods: Union[List[str], Set[str]] = ('GET', 'Retrieve', 'POST', 'PUT', 'DELETE')

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
            for k, v in kwargs.items():
                setattr(self, k, v)

        async def update(self, id, instance: schema = Body(..., ),
                         current_user: User = Depends(create_current_active_user(need_user))):
            print(current_user)
            query = self.table.update().where(self.model.id == id).values(**dict(instance))
            return await database.execute(query)

        async def create(self, instance: schema_noid = Body(..., ),
                         current_user: User = Depends(create_current_active_user(need_user))):
            print(current_user)
            query = self.table.insert().values(dict(instance))
            return await database.execute(query)

        def get_list_display(self) -> List[str]:
            """获取类对应要展示的数字,默认为list_display"""
            return self.list_display

        async def list(self, page: Dict[str, int] = Depends(paging_query_depend)):
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

        async def retrieve(self, id):
            """返回一个类型的详情"""
            query = self.table.select().where(self.model.id == id)
            return await self.database.fetch_one(query)

        async def delete(self, id):
            query = self.table.delete().where(self.model.id == id)
            return await self.database.execute(query)

    return View
def create_View(model, schema, schema_noid=None, database=None, need_user=False, **kwargs):
    """创建View的工厂方法"""
    if not schema_noid:
        schema_noid = schema
    return get_View(schema,schema_noid,database,need_user)(model, database, schema, schema_noid)


class BaseView:
    """该类为抽象类，需要继承并实现相关功能"""
    list_display: Union[List[str], str] = "__all__"
    methods: Union[List[str], Set[str]] = ('GET', 'Retrieve', 'POST', 'PUT', 'DELETE')

    def __init__(self, model, schema, database=None, need_user=False, **kwargs):
        """
        初始化基于类的视图,
            注意：可以先初始化，并实现所有的功能之后，在调用之前一定要将model、database、schema补齐
        :param model: 操作的sqlalchemy的Model
        :param database: 操作数据库的database
        :param schema: 用作数据验证的schema
        """
        print("注意，需要重构解决猴子修补的问题")
        self.model = model
        self.table = model.__table__
        self.database = database
        self.schema = schema
        for k, v in kwargs.items():
            setattr(self, k, v)
        if need_user:
            async def update(id, instance: schema = Body(..., ),
                             current_user: User = Depends(get_current_active_user)):
                query = self.table.update().where(self.model.id == id).values(**dict(instance))
                return await database.execute(query)
        else:
            async def update(id, instance: schema = Body(..., ), ):
                query = self.table.update().where(self.model.id == id).values(**dict(instance))
                return await database.execute(query)
        self.update = update
        if need_user:
            async def create(instance: schema = Body(..., ), current_user: User = Depends(get_current_active_user)):
                query = self.table.insert().values(dict(instance))
                return await database.execute(query)
        else:
            async def create(instance: schema = Body(..., )):
                query = self.table.insert().values(dict(instance))
                return await database.execute(query)
        self.create = create

    def get_list_display(self) -> List[str]:
        """获取类对应要展示的数字,默认为list_display"""
        return self.list_display

    async def list(self):
        """
        get
        :return:
        """
        if self.get_list_display() == "__all__":
            query = self.table.select()
        else:
            query = self.table.select(*self.get_list_display())
        return await self.database.fetch_all(query)

    async def retrieve(self, id):
        """返回一个类型的详情"""
        query = self.table.select().where(self.model.id == id)
        print(query)
        return await self.database.fetch_one(query)

    async def delete(self, id):
        query = self.table.delete().where(self.model.id == id)
        return await self.database.execute(query)
