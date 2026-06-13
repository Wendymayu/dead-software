# 事件驱动架构 (Event-Driven Architecture)

## 什么是事件驱动架构

事件驱动架构以**事件**为核心通信机制。当系统中发生重要变化时，产生一个事件；对该事件感兴趣的组件订阅并响应。发布者不知道谁会处理事件，订阅者也不知道事件从何而来。

## 核心思想

**解耦（Decoupling）**：组件之间不直接调用，而是通过事件总线间接通信。

```
发布者 ──→ [Event Bus] ──→ 订阅者A
                         ──→ 订阅者B
                         ──→ 订阅者C
```

关键特征：
- **发布者不关心谁接收** — 只管发出事件
- **订阅者不关心谁发出** — 只管处理事件
- **可随时增减订阅者** — 不影响发布者和其他订阅者

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **EventBus** — 中央事件路由器，维护 event_type → handlers 映射
2. **OrderService（发布者）** — 创建订单时发布 `"order_created"` 事件，不关心谁接收
3. **order_handler / inventory_handler / notification_handler（订阅者）** — 各自独立处理同一事件
4. **无人订阅的事件** — `payment_processed` 事件无人订阅，静默发布（不报错）

一个事件触发三个独立处理——这就是事件驱动的力量：新增处理逻辑只需订阅，不改发布者代码。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示两个实用特性：

1. **事件过滤** — `subscribe()` 可传入 `filter_fn`，只有符合条件的事件才传递给该订阅者（VIP处理只接收大额订单）
2. **链式处理** — 多个订阅者按注册顺序处理同一事件，形成处理链

## 优缺点

**优点**
- 极强的解耦——新增功能只需订阅事件
- 天然支持扩展——加订阅者不影响已有代码
- 异步友好——事件可排队、延迟处理
- 可回溯——事件可存储和重放

**缺点**
- 流程不直观——很难从代码看出"一个事件最终导致了什么"
- 调试困难——事件链可能很长，排查问题需要追踪整条链路
- 顺序问题——订阅者处理顺序可能影响结果
- 事件风暴——大量事件同时触发可能造成系统过载

## 真实项目中的应用

- **Node.js (EventEmitter)** — Node 的核心就是事件驱动
- **Spring Event** — Spring Framework 的应用事件机制
- **Kafka / RabbitMQ** — 分布式事件流平台，企业级事件驱动的基础设施
- **Vue.js** — 组件间通过 `$emit` / `$on` 通信（小型事件总线）

## 进一步阅读

- Martin Fowler — [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- 《软件架构模式》 (Mark Richards) — 事件驱动架构的详细分析
- 《Designing Event-Driven Systems》 (Ben Stopford) — Kafka 事件驱动设计
