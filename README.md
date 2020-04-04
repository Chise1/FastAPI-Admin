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

### V20200404
完成引入异步database功能
新增register_Model方法对methods的支持(支持retrieve)
引入默认表:User、Group、Permission
下阶段：引入权限控制机制