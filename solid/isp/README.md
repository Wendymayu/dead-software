# 接口隔离原则 (Interface Segregation Principle)

## 什么是接口隔离原则

接口隔离原则（ISP）要求客户端不应被迫依赖它不使用的方法。胖接口强迫所有实现者提供不需要的方法，应该将胖接口拆分为多个精简的、职责聚焦的接口。

## 核心思想

**客户端只依赖它需要的接口**：机器人不需要 `eat()` 方法，但胖接口 FatWorker 强迫 RobotWorker 实现 `eat()`。拆分为 Workable 和 Eatable 后，机器人只需实现 Workable。

```
┌──────────────────┐
│   FatWorker      │ ← 胖接口：work() + eat()
│  ┌──Human──┐     │    所有实现者被迫实现全部方法
│  │work+eat │     │
│  └─────────┘     │
│  ┌──Robot──┐     │
│  │work+eat?│     │    机器人不吃饭但被迫实现！
│  └─────────┘     │
└──────────────────┘

        vs

┌─────────┐ ┌─────────┐
│Workable │ │Eatable  │ ← 精简接口：各只一个方法
│  work() │ │  eat()  │
└────┬────┘ └────┬────┘
     │            │
┌────┴────┐ ┌────┴────┐
│GoodHuman│ │GoodHuman│ ← 人类实现两个
│work+eat │ │work+eat │
└─────────┘ └─────────┘
┌─────────┐
│GoodRobot│ ← 机器人只实现 Workable
│  work() │    不需要实现 eat()！
└─────────┘
```

关键机制：
- **接口拆分** — 大接口拆为多个小接口
- **按需实现** — 客户端只实现它使用的接口
- **多接口组合** — 一个类可以实现多个精简接口

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **FatWorker** — 胖接口，包含 `work()` 和 `eat()`，所有实现者被迫实现全部方法
2. **RobotWorker** — 被迫实现 `eat()`，只能抛出 `NotImplementedError`
3. **Workable / Eatable** — 两个精简接口，各只包含一个方法
4. **GoodRobot** — 只实现 Workable，无需关心 eat()

## 优缺点

**优点**
- 接口干净——客户端只看到它需要的方法
- 实现灵活——类可以选择实现哪些接口
- 解耦——接口变更只影响使用该接口的客户端
- 可测试——小接口更容易编写 Mock

**缺点**
- 接口数量增多——拆分带来更多接口定义
- 设计判断难——如何拆分、拆到什么粒度需要经验
- 过度拆分——接口太小反而增加组合复杂度

## 真实项目中的应用

- **Java Spring** — `Repository`, `CrudRepository`, `PagingAndSortingRepository` 层层细化
- **Python Protocol** — `typing.Protocol` 定义精简接口，按需组合
- **Go 接口** — Go 语言鼓励小接口（io.Reader 只有一个 Read 方法）
- **REST API** — 精简的 API 端点 vs 胖 API 返回所有数据

## 进一步阅读

- 《架构整洁之道》 (Robert C. Martin) — ISP 的深入讨论与架构影响
- 《Clean Code》 (Robert C. Martin) — 接口设计的实践指南
- Go 语言设计哲学 — 小接口理念的极致体现
