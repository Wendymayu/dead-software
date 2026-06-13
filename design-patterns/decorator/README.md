# 装饰器模式 (Decorator Pattern)

## 什么是装饰器模式

装饰器模式动态地给对象添加额外职责，而不修改原始对象的代码。装饰器和被装饰对象实现同一接口，装饰器包裹原对象——就像层层套上衣服，每件衣服增加一个功能。

## 核心思想

**包裹式增强（Wrapping Enhancement）**：不通过继承扩展功能，而是通过包裹旧对象添加新行为。每层装饰器持有被装饰对象的引用，先添加自己的行为，再转发给内部对象。

```
WhipDecorator
  ├─ 自己的行为: cost + 5, description + "奶泡"
  └─ 转发 → SugarDecorator
              ├─ 自己的行为: cost + 2, description + "糖"
              └─ 转发 → MilkDecorator
                          ├─ 自己的行为: cost + 3, description + "牛奶"
                          └─ 转发 → SimpleCoffee
                                      └─ 基础值: cost=10, description="咖啡"
```

关键机制：
- **同接口** — 装饰器和原对象实现同一接口，对外透明
- **持有引用** — 装饰器构造时接收被装饰对象
- **先加后转** — 先添加自己的行为，再调用内部对象的同名方法

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Coffee (ABC)** — 抽象接口，`cost()` 和 `description()` 是所有咖啡和装饰器共有的方法
2. **SimpleCoffee** — 基础对象，提供最基础的咖啡（¥10）
3. **MilkDecorator / SugarDecorator / WhipDecorator** — 三个装饰器，各自添加一种配料
4. **层层包裹** — `coffee = WhipDecorator(SugarDecorator(MilkDecorator(SimpleCoffee())))`——每层添加自己的行为后转发

注意每个装饰器的 `cost()` 方法：`self._coffee.cost() + 3`——它不是自己计算总价，而是把内部对象的 cost 加上自己的增量。这样嵌套多层时，cost 会自然累加。

## 优缺点

**优点**
- 动态增强——运行时决定添加哪些功能
- 避免继承膨胀——不需要为每种功能组合创建子类
- 可撤销——去掉装饰器就恢复原功能
- 符合开闭原则——新增装饰器不影响已有代码

**缺点**
- 装饰链长——多层装饰时调试和追踪变复杂
- 对象标识问题——装饰后的对象与原对象类型相同但不是同一个实例
- 排序敏感——某些装饰器的顺序会影响最终行为

## 真实项目中的应用

- **Python 装饰器语法** — `@decorator` 是装饰器模式的语法糖（尽管实现机制不同）
- **Java I/O 流** — `BufferedInputStream(FileInputStream(...))` 是经典的装饰器链
- **Django middleware** — 请求经过多个中间件层层包裹处理
- **Express.js middleware** — 每个中间件包裹请求处理链

**注意**：Python 的 `@decorator` 语法（函数装饰器）和 GoF 的装饰器模式有关联但机制不同。Python 函数装饰器在定义时包裹函数，GoF 装饰器在运行时包裹对象。本示例展示的是 GoF 装饰器模式。

## 进一步阅读

- 《设计模式》 (GoF) — 装饰器模式的经典定义
- 《Head First 设计模式》 — 星巴克咖啡的装饰器例子
- Python `@decorator` — [PEP 318](https://peps.python.org/pep-0318/) — Python 函数装饰器语法
