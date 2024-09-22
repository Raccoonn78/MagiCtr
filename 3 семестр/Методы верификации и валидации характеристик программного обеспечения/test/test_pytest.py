
# from pprint import pprint
import sys
# pprint(sys.path)
sys.path.append('C:\\Users\\Дмитрий\\Desktop\\МАГИСТР\\MagiCtr\\3 семестр\\Методы верификации и валидации характеристик программного обеспечения\\app_test\\')
from app_test.test_1 import Context, ConcreteStrategyA, ConcreteStrategyB
# import app_test.test_1

import pytest 
@pytest.fixture()
def get_data():
    return [1,2,3,4,5,6]


def sorted_list(get_data):
    data=get_data
    context = Context(ConcreteStrategyA())

    assert context.execute_strategy(data) == [1,2,3,4,5,6]


def sorted_reverse_list(get_data):
    data=get_data
    context = Context(ConcreteStrategyB())

    assert context.execute_strategy(data) == [6,5,4,3,2,1]


