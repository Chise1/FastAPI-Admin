# -*- encoding: utf-8 -*-
"""
@File    : views.py
@Time    : 2020/4/7 20:36
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from fastapi import Depends, Body
from .schemas import BaseConfig,EmailConfig
from .models import Config
from ..auth.depends import create_current_active_user
from ..databaseManage import AdminDatabase
from ..auth.models import User
fastapi_database=AdminDatabase()

async def config_update(instance: BaseConfig = Body(..., ),
                 current_user: User = Depends(create_current_active_user(True))):
    assert current_user.is_superuser,"没有超级用户权限"
    model=Config
    table=Config.__table__
    query = table.update().where(model.id == 0).values(**dict(instance))
    return await fastapi_database.execute(query)
async def email_config_update(instance:EmailConfig,current_user: User = Depends(create_current_active_user(True))):
    model = Config
    table = Config.__table__
    assert current_user.is_superuser, "没有超级用户权限"
    query = table.update().where(model.id == 0).values(**dict(instance))
    return await fastapi_database.execute(query)
# class ConfigView:
#     """该类为抽象类，需要继承并实现相关功能"""
#     list_display: Union[List[str], str] = "__all__"
#     methods: Union[List[str], Set[str]] = ('GET', 'Retrieve', 'POST', 'PUT', 'DELETE')
#
#     def __init__(self, model, database, schema, schema_noid, **kwargs):
#         """
#         初始化基于类的视图,
#             注意：可以先初始化，并实现所有的功能之后，在调用之前一定要将model、database、schema补齐
#         :param model: 操作的sqlalchemy的Model
#         :param database: 操作数据库的database
#         :param schema: 用作数据验证的schema
#         """
#         self.model = model
#         self.table = model.__table__
#         self.database = database
#         self.schema = schema
#         self.schema_noid = schema_noid
#         for k, v in kwargs.items():
#             setattr(self, k, v)
#
#
#
#     async def create(self, instance: schema_noid = Body(..., ),
#                      current_user: User = Depends(create_current_active_user(need_user))):
#         print(current_user)
#         query = self.table.insert().values(dict(instance))
#         return await database.execute(query)
#
#     def get_list_display(self) -> List[str]:
#         """获取类对应要展示的数字,默认为list_display"""
#         return self.list_display
#
#     async def list(self, page: Dict[str, int] = Depends(paging_query_depend)):
#         """
#         get
#         :return:
#         """
#         if self.get_list_display() == "__all__":
#             query = self.table.select().offset((page['page_number'] - 1) * page['page_size']).limit(
#                 page['page_size'])  # 第一页，每页20条数据。 默认第一页。
#         else:
#             query = self.table.select(*self.get_list_display())
#         paginate_obj = await self.database.fetch_all(query)
#         query2 = select([func.count(self.table.c.id)])
#         total_page = await AdminDatabase().database.fetch_val(query2)
#         print("注意需要考虑查询两次的两倍代价")
#         return {
#             "page_count": int(math.ceil(total_page * 1.0 / page['page_size'])),
#             "rows_total": total_page,
#             "page_number": page['page_number'],
#             "page_size": page['page_size'],
#             "data": paginate_obj
#         }
#
#     async def retrieve(self, id):
#         """返回一个类型的详情"""
#         query = self.table.select().where(self.model.id == id)
#         return await self.database.fetch_one(query)
#
#     async def delete(self, id):
#         query = self.table.delete().where(self.model.id == id)
#         return await self.database.execute(query)