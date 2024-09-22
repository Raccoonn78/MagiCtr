from abc import ABC, abstractmethod
 
class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        print('data ',data)
        pass
 
class ConcreteStrategyA(Strategy):
    def execute(self, data):
        return sorted(data)
 
class ConcreteStrategyB(Strategy):
    def execute(self, data):
        return list(reversed(sorted(data)))
 
class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy
 
    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy
 
    def execute_strategy(self, data):
        return self._strategy.execute(data)
 
# data = [1, 2, 3, 4, 5]
 
# context = Context(ConcreteStrategyA())
# print(context.execute_strategy(data))  # Вывод: [1, 2, 3, 4, 5]
 
# context.set_strategy(ConcreteStrategyB())
# print(context.execute_strategy(data))  # Вывод: [5, 4, 3, 2, 1]



