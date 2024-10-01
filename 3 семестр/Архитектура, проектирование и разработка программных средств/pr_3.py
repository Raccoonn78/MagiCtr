import copy

class Prototype:
    def __init__(self, value):
        self.value = value

    def clone(self):
        return copy.deepcopy(self)

# Использование:
original = Prototype(42)
clone = original.clone()

print(original.value)  # 42
print(clone.value)     # 42
print(original is clone)  # False, это разные объекты
