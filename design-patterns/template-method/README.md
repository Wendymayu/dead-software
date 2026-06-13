# 模板方法模式 (Template Method Pattern)

## 什么是模板方法模式

模板方法模式在父类中定义算法的骨架（固定步骤顺序），将某些步骤延迟到子类实现。就像做菜——炒菜的步骤（备料→下锅→调味→装盘）是固定的，但每道菜的具体做法不同，子类只需填充差异步骤。

## 核心思想

**骨架复用，步骤定制**：模板方法 `mine()` 固定调用顺序（read→process→analyze），子类只需实现这三个抽象步骤，不需要重复编写流程控制代码。

```
DataMiner (抽象类)
  │ mine() ─── 模板方法，固定步骤顺序
  │   read_data()     ── 抽象步骤（子类实现）
  │   process()       ── 抽象步骤（子类实现）
  │   analyze()       ── 抽象步骤（子类实现）
  │
  ├── CSVMiner  ── 填充 CSV 的每步实现
  └── JSONMiner ── 填充 JSON 的每步实现
```

关键机制：
- **模板方法** — mine() 定义步骤顺序，子类不能改变流程
- **抽象步骤** — @abstractmethod 让子类必须实现差异部分
- **钩子方法** — 可选：父类提供默认实现，子类可选择性覆盖

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **DataMiner (ABC)** — 抽象类，mine() 是模板方法，按顺序调用 read→process→analyze
2. **mine()** — 固定步骤顺序，所有子类共享同一流程，无需重复编写
3. **CSVMiner** — 填充 CSV 的具体实现：读CSV→拆分逗号→统计频次
4. **JSONMiner** — 填充 JSON 的具体实现：读JSON→解析键值→提取字段

注意 mine() 方法中 `data = self.read_data()` → `processed = self.process(data)` → `result = self.analyze(processed)`：这个调用顺序是固定的，子类无法改变流程——这是模板方法模式的核心约束，保证算法骨架的一致性。

## 优缺点

**优点**
- 流程复用——子类共享算法骨架，无需重复编写步骤编排
- 一致性——所有子类遵循相同步骤顺序，减少错误
- 开闭原则——新增子类只需实现抽象步骤，不修改模板方法
- 控制反转——父类调用子类方法（而非子类调用父类）

**缺点**
- 限制灵活性——子类不能改变步骤顺序或跳过步骤
- 类数量增多——每种变体都需要一个子类
- 调试困难——执行流程分散在父类和多个子类之间
- 继承耦合——子类依赖父类的模板方法实现细节

## 真实项目中的应用

- **Python unittest** — TestCase.run() 是模板方法，固定 setUp→test→tearDown 流程
- **Spring AbstractView** — renderMergedOutputModel() 固定渲染流程，子类只实现内容渲染
- **Apache Camel** — RouteBuilder 固定路由编排流程，子类定义具体路由步骤
- **C++ STL 算法** — sort() 固定比较-交换骨架，子类提供比较策略

## 进一步阅读

- 《设计模式》 (GoF) — 模板方法模式的经典定义
- 《Head First 设计模式》 — 以咖啡/茶冲泡为例的生动讲解
- 《Effective Java》 (Joshua Bloch) — 模板方法在框架设计中的应用
