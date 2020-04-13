# -*- encoding: utf-8 -*-
"""
@File    : models.py
@Time    : 2020/4/6 21:49
@Author  : chise
@Email   : chise123@live.com
@Software: PyCharm
@info    :
"""
import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime,  Text
from fastapi_admin.auth.models import Base


class AccountBookLog(Base):
    """账本日志"""
    __tablename__ = "adminmanager_accountbook_log"
    id = Column(Integer, primary_key=True, index=True)
    accountbook_id = Column(Integer, ForeignKey("adminmanager_accountbook.id"))
    accountbook = relationship("AccountBook", backref="account_book_logs", )
    before_money = Column(String(255), comment="操作前金额",default='0')
    after_money = Column(String(255), comment="操作后金额",default='0')
    operate_time = Column(DateTime, comment="操作时间")
    operate_status = Column(Integer, comment="(收⼊(充值)，⽀出(消费，冻结))")
    change_money = Column(Integer, comment="变动⾦额(余额，冻结⾦额，可提现⾦额)")


class Member(Base):
    """会员列表"""
    __tablename__ = "adminmanager_member"
    id = Column(Integer, primary_key=True, index=True)
    member_name = Column(String(64), comment="套餐名称")
    member_money = Column(String(255), comment="购买价格",default='0')
    member_rate_money = Column(String(255), comment="折扣价格",default='0')
    remark=Column(Text,comment="备注")
    member_time = Column(DateTime, comment="会员时间，有效时间",nullable=True)
    member_authory = Column(String(64), comment="会员权限(后期按项⽬定)")
    rate = Column(String(255), comment="费率",default='0')
class AccountBook(Base):
    """用户账本"""
    __tablename__ = "adminmanager_accountbook"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("fastapi_auth_user.id"))
    user = relationship("User", backref="user_logs", )
    money = Column(String(255), comment="余额(不可提现)",default='0')
    err_money = Column(String(255), comment=" 不可⽤余额(范指冻结⾦额，不可操作)",default='0')
    suc_money = Column(String(255), comment="可提现⾦额(指邀请返利的⾦额，或者其他七七⼋⼋的，反正可以提现)",default='0')
    create_time = Column(DateTime, comment="账本创建时间(⼀般同⽤户信息⼀块写⼊， 系统⾃动初始化)",default=datetime.datetime.now)
    rate = Column(String(255), comment="费率",default='0')
    member_id = Column(Integer, ForeignKey("adminmanager_member.id"), comment="会员ID",default='0')
    member = relationship("Member", backref="accountBooks", )
