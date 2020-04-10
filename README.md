# FastAPI-Admin
实现fastapi的前后端分离的后台管理系统

## 安装
```shell script
python setup.py install
```
注册model和router
在main注册
```python
#创建并注册admin类
from fastapi_admin import FastAPIAdmin
from fastapi import  FastAPI

app = FastAPI()
#连接数据库的url
SQLALCHEMY_DATABASE_URL:str="mysql+pymysql://root:admin@localhost/fastapiadmin?charset=utf8mb4"
admin=FastAPIAdmin(app,SQLALCHEMY_DATABASE_URL)

#注册所有需要创建基本方法的Model,注册类型
admin.register_Model(User)

```
会生成这样的接口
![avatar](doc/1585901894(1).jpg)
## update
### v20200410
新增patch的view生成功能，目前相关功能正在完善，之后考虑根据此重构view类实现更好的操作。
另，app启动速度好像变慢了，注意测试运行速度是否受影响。
### v20200409
解决默认值为函数时候的漏判
修改部分表格和结构
### v20200408
新增针对model设置的get方法
对view的list增加了全局分页控制
### v20200408
解决无法重复注释basemodel的问题
优化文档结构
### v20200407
优化view，完成分页功能，去掉了post创建时候需要主键的问题。
接下来新增权限管理。
### v20200407
增加分页基础功能，但是还没有在view里面增加分页功能
明天优化view，并增加分页功能，考虑增加分页功能的返回依赖。做一个工厂函数，封装list函数为分页功能的list函数
### v20200405
完成权限控制---登录功能
完成User表的增删改查
考虑重构BaseView解决猴子修补的问题

### V20200404
完成引入异步database功能
新增register_Model方法对methods的支持(支持retrieve)
引入默认表:User、Group、Permission
下阶段：引入权限控制机制