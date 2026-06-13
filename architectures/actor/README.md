# Actor 架构 (Actor Model)

## 什么是 Actor 模型

Actor 模型将并发计算的基本单元定义为 Actor：每个 Actor 拥有独立的私有状态和邮箱，只能通过异步消息与其他 Actor 通信，绝不共享状态。这是 Carl Hewitt 于 1973 年提出的并发计算模型。

## 核心思想

**独立状态 + 邙箱通信 + 无共享状态**：Actor 之间只能发消息，绝不直接访问彼此的状态。

```
  CounterActor          PrinterActor
  ┌──────────┐          ┌──────────┐
  │ state: 3 │          │ state:{} │
  │ mailbox: │←──消息──→│ mailbox: │
  └──────────┘          └──────────┘
       ↑ 发消息              ↑ 发消息
       └─────异步 ───────────┘
         Actor 之间绝不共享状态
```

关键约束：
- **私有状态** — Actor 的状态只有自己能访问，其他 Actor 无法直接读写
- **异步消息** — 唯一的通信方式，发送消息后不等回复
- **邮箱队列** — 消息进入邮箱排队，Actor 逐条处理
- **无共享状态** — 与线程模型的关键区别：不靠锁同步，靠消息通信

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **Actor** — 基类：mailbox（消息队列）+ state（私有状态）+ send/process_messages
2. **CounterActor** — 维护 count 状态，收到 INCREMENT 时自增并回发 COUNT_UPDATE
3. **PrinterActor** — 收到 COUNT_UPDATE 时打印，也可主动发送 GET_COUNT 查询
4. **send()** — 唯一通信方式：消息放入目标邮箱，异步不阻塞

Actor 之间绝不共享状态——所有交互必须通过消息，这是与线程/锁模型的根本区别。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示 Actor 的进阶能力：**ActorSystem + 多 Actor 协作**。

- `ActorSystem` — 管理所有 Actor 的创建和消息调度
- `OrderActor → InventoryActor → PaymentActor` — 下单流程通过消息链完成
- `run_all()` — 多轮调度，每轮所有 Actor 处理邮箱消息，模拟异步系统

## 优缺点

**优点**
- 无共享状态——天然避免竞态条件，不需要锁
- 位置透明——Actor 可在本地或远程，消息通信方式不变
- 天然并发——每个 Actor 独立处理消息，并行度高
- 容错隔离——一个 Actor 故障不影响其他 Actor

**缺点**
- 异步复杂——消息发送后不等回复，调试和推理比同步代码困难
- 消息顺序——邮箱消息顺序不保证因果一致性（除非特殊处理）
- 性能开销——每条消息经过邮箱调度，比直接调用慢
- 死锁可能——虽然无锁，但消息等待循环仍可造成逻辑死锁

## 眜实项目中的应用

- **Akka (Scala/Java)** — JVM 上最成熟的 Actor 框架，灵感来自 Erlang
- **Erlang/OTP** — 电信级 Actor 系统，99.9999999% 可用性的行业传奇
- **Ray (Python)** — 分布式 Actor 模型，用于 ML 训练和推理的并行调度

## 进一步阅读

- Carl Hewitt — Actor 模型原始论文 (1973)
- 《Akka in Action》 — JVM Actor 框架实战
- Erlang/OTP 文档 — [erlang.org](https://www.erlang.org/) 电信级 Actor 系统参考
