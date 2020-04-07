# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/4/6 21:49
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""

from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime, DECIMAL

from fastapi_admin.auth.models import Base


class AccountBook(Base):
    """用户账本"""
    __tablename__ = "adminmanager_accountbook"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("fastapi_auth_user.id"))
    user = relationship("User", backref="user_logs", )
    money = Column(DECIMAL, comment="余额(不可提现)")
    err_money = Column(DECIMAL, comment=" 不可⽤余额(范指冻结⾦额，不可操作)")
    suc_money = Column(DECIMAL, comment="可提现⾦额(指邀请返利的⾦额，或者其他七七⼋⼋的，反正可以提现)")
    create_time = Column(DateTime, comment="账本创建时间(⼀般同⽤户信息⼀块写⼊， 系统⾃动初始化)")
    rate = Column(DECIMAL, comment="费率")


class AccountBookLog(Base):
    """账本日志"""
    __tablename__ = "adminmanager_accountbook_log"
    id = Column(Integer, primary_key=True, index=True)
    accountbook_id = Column(Integer, ForeignKey("adminmanager_accountbook.id"))
    accountbook = relationship("AccountBook", backref="account_book_logs", )
    before_money = Column(DECIMAL, comment="操作前金额")
    after_money = Column(DECIMAL, comment="操作后金额")
    operate_time = Column(DateTime, comment="操作时间")
    operate_status = Column(Integer, comment="(收⼊(充值)，⽀出(消费，冻结))")
    change_money = Column(Integer, comment="变动⾦额(余额，冻结⾦额，可提现⾦额)")


class Member(Base):
    """会员"""
    __tablename__ = "adminmanager_member"
    id = Column(Integer, primary_key=True, index=True)
    member_name = Column(String(64), comment="会员名称")
    member_money = Column(DECIMAL, comment="会员金额")
    member_time = Column(DateTime, comment="会员时间，有效时间")
    member_authory = Column(String(64), comment="会员权限(后期按项⽬定)")
    rate = Column(DECIMAL, comment="费率")
