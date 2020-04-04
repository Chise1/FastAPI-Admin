import time
from typing import Iterable
class A():
    def name(self):
        print("a")
class B(A):
    def __getattr__(self, item):
        # print(self.__dir__())
        print("getattr:", item)
        return "None111111111111111111"
    # x=10
    @property
    def name1(self):
        return 213
    def name(self):
        return "sfag"
    def __getattribute__(self, item):
        print("use getattribute")
        x = super().__getattribute__(item)#重点：如果父类调用找不到会直接在父类那里面调用__getattr__，如果还没找到就会直接返回了，这一行下面的代码不会执行。这里有点扯，我觉得是python的bug。。。
        print(isinstance(x,classmethod))
        print(type(x))
        print(str(type(x))=="<class 'method'>")#判断是否为类的方法属性或函数，具体分析请看下面
        print(item + ":" + str(x))
        return x

    def __dir__(self) -> Iterable[str]:
        print("dir")#本来以为上面两个方法会调用，但是实际上没有调用
        return super().__dir__()

b = B()
print(0)
print(hasattr(b,'nnnn'))
print("1")
print(b.x)
print(2)
print(b.name())