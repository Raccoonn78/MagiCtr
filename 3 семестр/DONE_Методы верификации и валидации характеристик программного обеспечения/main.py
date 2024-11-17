# from app_test.test_1 import Context, ConcreteStrategyB, ConcreteStrategyA
# from test import *


from pyinstrument import Profiler
import time

def a():
    b()
    c()

def b():
    d()

def c():
    d()

def d():
    e()

def e():
    time.sleep(1)
    e()

profiler = Profiler()
profiler.start()

a()

profiler.stop()
print(profiler.output_text(unicode=True, color=True))
