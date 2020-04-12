# -*- encoding: utf-8 -*-
"""
@File    : schema_tools.py
@Time    : 2020/4/7 20:48
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
from datetime import datetime, date
from typing import List
from pydantic import BaseModel, Field
from sqlalchemy import Integer, Boolean, String, Float, DateTime, Text, DATE, Date, DECIMAL
from typing import Optional

def get_model_str(model, exclude: Optional[List[str]] = None,
                  fields: Optional[List[str]] = None):
    # mappings为从model获取的相关配置
    __mappings__ = {}  # {'name':{'field':Field,'type':type,}}
    for filed in model.__table__.c:
        filed_name = str(filed).split('.')[-1]
        if exclude:
            if exclude.count(filed_name):
                continue
        if fields:
            if not fields.count(filed_name):
                continue

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
        # 生成的结构： id:int=Field(...,)大概这样的结构
        # res_field = Field(default_value, description=filed.description)  # Field参数
        res_field = 'Field({}, description="{}")'.format(default_value, filed.comment)  # Field参数
        if isinstance(filed.type, Integer):
            tp = filed_name + ':int=' + res_field
        elif isinstance(filed.type, Float):
            tp = filed_name + ':float=' + res_field
        elif isinstance(filed.type, Boolean):
            tp = filed_name + ":bool =" + res_field
        elif isinstance(filed.type, String):
            max_length = filed.type.length
            tp = filed_name + ':str=' + 'Field({}, description="{}",max_length={})'.format(default_value, filed.comment,
                                                                                           max_length)
        elif isinstance(filed.type, DateTime):
            tp = filed_name + ':datetime=' + 'Field({}, description="{}")'.format(default_value, filed.comment)
        elif isinstance(filed.type, Date):
            tp = filed_name + ':date=' + 'Field({}, description="{}")'.format(default_value, filed.comment)
        else:
            tp = filed_name + ':str=' + res_field
        __mappings__[filed_name] = tp
    s_fields = ''
    for k, v in __mappings__.items():
        s_fields = s_fields + '    ' + v + '\n'
    return s_fields


def __create_one_schema(model, default_model_name=None, exclude: Optional[List[str]] = None,
                        fields: Optional[List[str]] = None, base_model: str = None) -> BaseModel:
    """
    通过读取model的信息，创建schema
    :param model:
    :param exclude:
    :return:
    """
    if not base_model:
        base_model: str = """
class {}(BaseModel):
{}
    """
    if not default_model_name:
        model_name = model.__name__
    else:
        model_name = default_model_name
    # mappings为从model获取的相关配置
    s_fields = get_model_str(model, exclude, fields)
    base_model = base_model.format(model_name, s_fields)
    cls_dict = {"BaseModel": BaseModel, "Field": Field, "datetime": datetime, "date": date}
    exec(base_model, cls_dict)
    # 将schema绑定到model
    print(base_model)
    schema = cls_dict[model_name]
    return schema


def create_schema(model, default_model_name=None, exclude: Optional[List[str]] = None,
                  fields: Optional[List[str]] = None) -> (
        BaseModel, BaseModel):
    """
    通过读取model的信息，创建schema
    :param model:
    :param exclude:
    :return:
    """
    assert not (exclude and fields), "不能两个都填写"
    if not default_model_name:
        model_name = model.__name__
    else:
        model_name = default_model_name
    schema = create_get_schema(model, model_name, exclude, fields)
    schema_noid = create_post_schema(model, model_name + "Noid", exclude, fields)
    return schema, schema_noid


def create_get_schema(model, default_model_name=None, exclude: Optional[List[str]] = None,
                      fields: Optional[List[str]] = None) -> BaseModel:
    return __create_one_schema(model, default_model_name, exclude, fields)


def create_post_schema(model, default_model_name=None, exclude: Optional[List[str]] = None,
                       fields: Optional[List[str]] = None) -> BaseModel:
    if fields:
        if not fields.count("id"):
            fields.append("id")
    elif exclude:
        if not exclude.count("id"):
            exclude.append("id")
    else:
        exclude = ["id"]
    return __create_one_schema(model, default_model_name, exclude, fields)


def create_get_page_schema(model, default_model_name=None, exclude: Optional[List[str]] = None,
                           fields: Optional[List[str]] = None) -> BaseModel:
    """
    通过读取model的信息，创建schema列表
    :param model:
    :param exclude:
    :return:
    """
    base_model: str = """
from typing import List
from pydantic import BaseModel,Field
class {0}BASEPAGE(BaseModel):
{1}
class {0}PagingModel(BaseModel):
    page_count: int
    rows_total: int
    page_number: int
    page_size: int
    data: List[{0}BASEPAGE]
    """
    if not default_model_name:
        model_name = model.__name__
    else:
        model_name = default_model_name
    s_fields = get_model_str(model, exclude, fields)
    base_model = base_model.format(model_name, s_fields)
    cls_dict = {"datetime": datetime, "date": date,}
    exec(base_model, cls_dict)
    # 将schema绑定到model
    print(base_model)
    schema = cls_dict[model_name + "PagingModel"]
    return schema
