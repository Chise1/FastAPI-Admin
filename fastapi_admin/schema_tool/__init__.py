# -*- encoding: utf-8 -*-
"""
@File    : __init__.py.py
@Time    : 2020/4/11 22:31
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from datetime import datetime, date
from typing import List, Union
from pydantic import BaseModel, Field
from sqlalchemy import Integer, Boolean, String, Float, DateTime, Text, DATE, Date, DECIMAL
from typing import Optional
from datetime import datetime

__all__ = ["create_page_schema", "create_schema"]


def get_field_default_value(filed) -> str:
    """判断field的默认值"""
    if filed.default is not None:
        if isinstance(filed.default.arg, str):
            default_value = '"' + filed.default.arg + '"'
        elif callable(filed.default.arg):
            default_value = '"' + str(filed.default.arg(filed)) + '"'
        else:
            default_value = str(filed.default.arg)
    elif filed.nullable:
        default_value = 'None'
    else:
        default_value = '...'
    return default_value


def get_field_type_and_maxlength(filed, ):
    """
    判断对应field的字段类型
    :param field:
    :return:返回默认类型和最大值
    """
    if isinstance(filed.type, Integer):
        return 'int', None
    elif isinstance(filed.type, Float):
        return 'float', None
    elif isinstance(filed.type, Boolean):
        return 'bool', None
    elif isinstance(filed.type, String):
        max_length = filed.type.length
        return 'str', max_length
        # tp = filed_name + ':str=' + 'Field({}, description="{}",max_length={})'.format(default_value,
        #                                                                                filed.comment,
        #                                                                                max_length)
    elif isinstance(filed.type, DateTime):
        return 'datetime', None
    elif isinstance(filed.type, Date):
        return 'date', None
    # elif isinstance(filed.type, ChoiceType):
    #     return 'int',None
    else:
        return 'str', None


def get_field_comment(field):
    return field.comment


def combine_field(field_type, filed_name, default_value,comment, max_length, ) -> str:
    """
    将获取的字段组合成一个完整的schema字段
    :param field_type:
    :param filed_name:
    :param default_value:
    :param max_length:
    :param comment:
    :return:
    """
    if max_length:
        res_field = 'Field({}, description="{}",max_length={})'.format(default_value, comment, max_length)  # Field参数
    else:
        res_field = 'Field({}, description="{}")'.format(default_value, comment)  # Field参数
    return filed_name + ":" + field_type + " =" + res_field


def get_model_str(model, need_fields_all: Union[str, list,dict] = '__all__', fields_params: dict = None,
                  exclude: Optional[List[str]] = None):
    """
    得到model的字符串格式，注意，如果need_fields和exclude都有，则默认会被排除掉
    :param model: sqlalchemy的model
    :param need_fields: 需要的字段默认为全部
    :param fields_params: 对一些特殊字段进行过滤
    :param exclude: 排除某些字段
    :return:
    """
    # mappings为从model获取的相关配置
    __mappings__ = {}  # {'name':{'field':Field,'type':type,}}
    if not isinstance(model,list):
        need_fields=need_fields_all or "__all__"
        for field in model.__table__.c:
            field_name = str(field).split('.')[-1]
            if exclude and exclude.count(field_name):
                continue
            if need_fields != '__all__':
                if not need_fields.count(field_name):
                    continue
            if fields_params:
                for index in fields_params:
                    if isinstance(fields_params[index],str) and fields_params[index] !=field_name:
                        continue
                    if isinstance(fields_params[index],dict):
                        input_field=fields_params[index].get(field_name)
                        if not input_field:
                            continue
                        else:
                            if input_field.get('default'):
                                default_value = input_field.get('default')
                            elif input_field.get('nullable'):
                                default_value = 'None'
                            else:
                                default_value = get_field_default_value(field)
                            if input_field.get("description"):
                                comment = input_field.get("description")
                            else:
                                comment = get_field_comment(field)
                            if input_field.get('type'):
                                if input_field.get('type') == 'str':
                                    field_type = 'str'
                                    max_length = input_field.get('max_length')
                                else:
                                    field_type, max_length = get_field_type_and_maxlength(field)
                            else:
                                field_type, max_length = get_field_type_and_maxlength(field)
                            break
                else:
                    default_value = get_field_default_value(field)
                    comment = get_field_comment(field)
                    field_type, max_length = get_field_type_and_maxlength(field)
            else:
                default_value = get_field_default_value(field)
                comment = get_field_comment(field)
                field_type, max_length = get_field_type_and_maxlength(field)
            __mappings__[field_name] = combine_field(field_type, field_name, default_value, comment,
                                                     max_length)
        # s_fields = ''
        # for k, v in __mappings__.items():
        #     s_fields = s_fields + '    ' + v + '\n'
    else:
        for sigle_model in model:
            need_fields=need_fields_all.get(str(sigle_model.__table__)) or "__all__"
            for field in sigle_model.__table__.c:
                res_filed_name = str(sigle_model.__table__)+'_'+ str(field).split('.')[-1]
                field_name=str(field).split('.')[-1]
                if exclude and exclude.count(field_name):  # 如果存在这个字段则直接跳过
                    continue
                if need_fields != '__all__':
                    if not need_fields.count(field_name):
                        continue
                if not fields_params:
                    default_value = get_field_default_value(field)
                    comment = get_field_comment(field)
                    field_type, max_length = get_field_type_and_maxlength(field)
                else:
                    for index in fields_params:
                        if isinstance(fields_params[index], str) and fields_params[index] != field_name:
                            continue
                        if isinstance(fields_params[index], dict):
                            input_field = fields_params[index].get(field_name)
                            if not input_field:
                                continue
                            else:
                                if input_field.get('default'):
                                    default_value = input_field.get('default')
                                elif input_field.get('nullable'):
                                    default_value = 'None'
                                else:
                                    default_value = get_field_default_value(field)
                                if input_field.get("description"):
                                    comment = input_field.get("description")
                                else:
                                    comment = get_field_comment(field)
                                if input_field.get('type'):
                                    if input_field.get('type') == 'str':
                                        field_type = 'str'
                                        max_length = input_field.get('max_length')
                                    else:
                                        field_type=input_field.get('type')
                                        max_length=None
                                else:
                                    field_type, max_length = get_field_type_and_maxlength(field)
                                break
                    else:
                        default_value = get_field_default_value(field)
                        comment = get_field_comment(field)
                        field_type, max_length = get_field_type_and_maxlength(field)
                __mappings__[res_filed_name] = combine_field(field_type, res_filed_name, default_value, comment, max_length)
    s_fields = ''
    for k, v in __mappings__.items():
        s_fields = s_fields + '    ' + v + '\n'
    return s_fields

def __base_create_schema(model, schema_name, need_fields, fields_params, exclude, base_schema=None,
                         res_schema_name=None) -> BaseModel:
    """
    通过读取model的信息，创建schema
    :param model:
    :param schema_name: 要自定义的schema名字，每个schema不能重复
    :param need_fields: 需要显示的字段，如果同时存在于exclude，则默认exclude更高
    :param fields_params: 需要自定义的字段类型
    :param exclude: 需要排除的字段
    :param base_schema: schema生成模板
    :param res_schema_name: 返回的schema名字，用户不要使用这个字段
    :return:
    """
    if not base_schema:
        base_schema: str = """
class {}(BaseModel):
{}
    """
        res_schema_name = schema_name
    s_fields = get_model_str(model, need_fields, fields_params, exclude)
    base_schema = base_schema.format(schema_name, s_fields)
    print(base_schema)
    cls_dict = {"BaseModel": BaseModel, "Field": Field, "datetime": datetime, "date": date}
    exec(base_schema, cls_dict)
    # 将schema绑定到model
    schema = cls_dict[res_schema_name]
    return schema


def create_schema(model, schema_name, need_fields: Union[str, list] = '__all__', fields_params=None, exclude=None) -> BaseModel:
    """
    通过读取model的信息，创建schema
    :param model:
    :param schema_name: 要自定义的schema名字，每个schema不能重复
    :param need_fields: 需要显示的字段，如果同时存在于exclude，则默认exclude更高
    :param fields_params: 需要自定义的字段类型
    :param exclude: 需要排除的字段
    :return:
    """
    if not need_fields:
        need_fields="__all__"
    return __base_create_schema(model, schema_name, need_fields, fields_params, exclude)


def create_page_schema(model, schema_name: str, need_fields: Union[str, list] = '__all__', fields_params=None, exclude=None) -> BaseModel:
    """
    通过读取model的信息，创建分页的schema
    :param model:
    :param exclude:
    :return:
    """
    base_model: str = """
from typing import List
from pydantic import BaseModel,Field
class {0}_Page(BaseModel):
{1}
class {0}PagingModel(BaseModel):
    page_count: int
    rows_total: int
    page_number: int
    page_size: int
    data: List[{0}_Page]
"""
    res_model_name = schema_name + "PagingModel"
    return __base_create_schema(model, schema_name, need_fields, fields_params, exclude, base_model, res_model_name)
