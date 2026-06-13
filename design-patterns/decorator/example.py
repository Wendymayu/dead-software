"""装饰器模式 (Decorator Pattern) 最小化示例

演示动态给对象添加职责：
- 装饰器和被装饰对象实现同一接口
- 装饰器包裹原对象，添加新行为后转发调用
- 可以层层嵌套装饰
"""

from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self): ...

    @abstractmethod
    def description(self): ...


class SimpleCoffee(Coffee):
    def cost(self):
        return 10

    def description(self):
        return "普通咖啡"


class MilkDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 3

    def description(self):
        return self._coffee.description() + " + 牛奶"


class SugarDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 2

    def description(self):
        return self._coffee.description() + " + 糖"


class WhipDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 5

    def description(self):
        return self._coffee.description() + " + 奶泡"


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("装饰器模式演示：层层添加职责")
    print("=" * 40 + "\n")

    coffee = SimpleCoffee()
    print(f"  {coffee.description()} -- {coffee.cost()}元")

    coffee = MilkDecorator(coffee)
    print(f"  {coffee.description()} -- {coffee.cost()}元")

    coffee = SugarDecorator(coffee)
    print(f"  {coffee.description()} -- {coffee.cost()}元")

    coffee = WhipDecorator(coffee)
    print(f"  {coffee.description()} -- {coffee.cost()}元")

    print("\n装饰链: Whip → Sugar → Milk → SimpleCoffee")
