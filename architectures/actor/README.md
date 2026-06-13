# Actor 架构 (Actor Model)

## 什么是 Actor 模型

Actor 模型将并发计算的基本单元定义为 Actor：每个 Actor 拥有独立的私有状态和邮箱，只能通过异步消息与其他 Actor 通信，绝不共享状态。这是 Carl Hewitt 于 1973 年提出的并发计算模型。

### 历史背景

Actor 模型由 MIT 的 Carl Hewitt、Peter Bishop 和 Richard Steiger 在 1973 年的论文"A Universal Modular ACTOR Formalism for Artificial Intelligence"中首次提出。最初的目标是为人工智能系统设计一种并发计算模型——Hewitt 认为，AI 系统需要大量独立的知识处理模块并行协作，共享状态的线程模型不适合这种场景。1980 年代，Gul Agha 在《ACTORS: A Model of Concurrent Computation in Distributed Systems》中扩展了 Hewitt 的工作，将 Actor 模型从理论框架发展为可实现的编程模型。1986 年，Joe Armstrong 和 Robert Virding 在 Ericsson 开始开发 Erlang——他们虽然没有直接引用 Hewitt 的论文，但 Erlang 的进程+消息传递模型与 Actor 模型的核心思想完全一致。Erlang 在电信交换机中实现了 99.9999999% 可用性（每年停机不到 31.55 秒），成为 Actor 模型在工业界的传奇验证。2000 年代，Akka 框架将 Actor 模型带到 JVM 世界，Scala 和 Java 开发者可以像 Erlang 一样使用 Actor 构建高并发系统。

### 与相关模式的比较

| 模式 | 关键区别 |
|------|---------|
| **线程/锁模型** | 线程共享内存，靠锁同步访问共享状态，竞态条件是常态；Actor 不共享状态，靠消息通信，天然避免竞态条件 |
| **黑板架构** | 黑板架构中多个专家共享一个中央数据空间；Actor 之间绝不共享状态，每个 Actor 有独立邮箱 |
| **微服务** | 微服务强调独立部署和服务边界；Actor 强调并发计算模型和消息通信，Actor 可以在同一进程内 |
| **事件驱动架构** | 事件驱动是广播式（发布者不知道谁会消费）；Actor 是定向式（消息发送给特定 Actor） |

Actor 模型与线程/锁模型的对比是最关键的——前者用"不共享+消息"替代了"共享+锁"，从根本上消除了竞态条件的可能性。

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

### 什么时候该用

- **高并发场景** — 系统需要同时处理大量独立请求，每个请求有自己的状态
- **分布式计算** — 计算需要跨多台机器，位置透明性让 Actor 可以在任意节点上运行
- **需要容错隔离** — 一个组件的故障不能波及其他组件，Actor 的独立邮箱和状态天然隔离
- **复杂并发逻辑** — 共享状态+锁的模型让并发代码难以正确编写，Actor 的无共享模型简化了并发推理

### 什么时候不该用

- **简单顺序逻辑** — 单线程顺序执行的代码不需要 Actor 的消息调度开销
- **强同步交互** — 需要等待对方立即回复的场景，Actor 的异步消息模型增加了复杂度
- **大量共享数据** — 数据需要频繁在多个处理单元之间共享时，强制使用 Actor 会导致消息通信量暴增
- **低延迟要求** — 消息经过邮箱调度有额外延迟，微秒级响应时间不适合 Actor 模型

### 常见误解

- **误解：Actor 模型就是线程池** — 事实：线程池中的线程共享内存、通过锁协调访问共享数据；Actor 不共享任何状态，每个 Actor 有独立的私有状态和邮箱。线程池解决的是"任务调度"问题，Actor 解决的是"并发计算模型"问题——两者本质不同。
- **误解：Actor 消息保证顺序** — 事实：Actor 模型只保证同一个 Actor 发送给同一个目标 Actor 的消息顺序不变（FIFO），但不同 Actor 发给同一目标的消息顺序不确定。如果需要因果一致性，必须在消息中携带序列号或使用专门的协议。
- **误解：Actor 模型没有死锁** — 事实：Actor 模型确实没有锁导致的死锁，但消息等待循环仍可造成逻辑死锁——Actor A 等待 Actor B 的回复，Actor B 等待 Actor A 的回复，两者都不会继续处理。Erlang 的"超时机制"就是为了解决这个问题。

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **Actor** — 基类：mailbox（消息队列）+ state（私有状态）+ send/process_messages
   > **要点提示**：mailbox 是一个队列，所有发给这个 Actor 的消息都排队等待处理。state 是 Actor 的私有数据——外部无法直接访问，只能通过消息间接影响。这两个成员是 Actor 模型的核心结构。

2. **CounterActor** — 维护 count 状态，收到 INCREMENT 时自增并回发 COUNT_UPDATE
   > **要点提示**：count 状态只存在于 CounterActor 内部——PrinterActor 不能直接读取 count，必须发送 GET_COUNT 消息请求 CounterActor 告知当前值。这正是"无共享状态"的直接体现：状态私有化，只通过消息暴露。

3. **PrinterActor** — 收到 COUNT_UPDATE 时打印，也可主动发送 GET_COUNT 查询
   > **要点提示**：PrinterActor 处理 COUNT_UPDATE 和 GET_COUNT 两种消息。它不知道 count 的当前值——它只能请求 CounterActor 告知。两个 Actor 之间的所有交互都通过消息完成。

4. **send()** — 唯一通信方式：消息放入目标邮箱，异步不阻塞
   > **要点提示**：send() 的行为是"放入对方邮箱后立即返回"——不等待对方处理完成，不等待回复。这与线程模型中"调用对方方法并等待返回"的同步模式截然不同。异步是 Actor 模型的核心语义：发送即忘（fire-and-forget）。

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
- 无共享状态——天然避免竞态条件，不需要锁，并发代码的正确性更容易保证
- 位置透明——Actor 可在本地或远程，消息通信方式不变，分布式部署无需修改代码逻辑
- 天然并发——每个 Actor 独立处理消息，并行度高，多个 Actor 可以在不同线程甚至不同机器上运行
- 容错隔离——一个 Actor 故障不影响其他 Actor，Erlang 的"Let it crash"哲学正是基于 Actor 的隔离特性

**缺点**
- 异步复杂——消息发送后不等回复，调试和推理比同步代码困难，需要理解消息流转的全链路
- 消息顺序——邮箱消息顺序不保证因果一致性（除非特殊处理），多 Actor 发送的消息到达顺序不确定
- 性能开销——每条消息经过邮箱调度，比直接方法调用慢，高频交互路径上开销累积
- 死锁可能——虽然无锁，但消息等待循环仍可造成逻辑死锁，Actor A 等待 B 的回复而 B 等待 A 的回复

### 适用场景

- 电信系统——Erlang/OTP 在交换机中实现了极高可用性，Actor 天然匹配"大量独立通话需要并行处理"
- 分布式计算——Ray 用 Actor 模型调度 ML 训练任务，Actor 可以在不同 GPU 节点上运行
- 游戏服务器——每个玩家或 NPC 是一个 Actor，玩家之间的交互通过消息完成
- IoT 系统——大量传感器节点独立运行，每个传感器可以用 Actor 表示

### 不适用场景

- 简单 CRUD 应用——请求/响应式的 Web 应用，Actor 的异步消息模型增加了不必要的复杂度
- 批处理数据处理——MapReduce 等批处理模型更适合大数据场景，Actor 的逐条消息处理效率低
- 强事务要求——需要跨多个数据项的原子事务保证，Actor 的无共享模型无法直接支持 ACID 事务

## 真实项目中的应用

- **Akka (Scala/Java)** — JVM 上最成熟的 Actor 框架，灵感来自 Erlang。Akka 提供了 ActorSystem、Actor 生命周期管理、消息路由和集群支持。Akka 的位置透明性让 Actor 可以在本地线程或远程节点上运行，开发者不需要修改消息通信代码。Akka Streams 基于 Actor 模型构建了背压感知的流处理框架——每个处理步骤是一个 Actor，数据通过 Actor 间消息传递流动。
- **Erlang/OTP** — 电信级 Actor 系统，99.9999999% 可用性的行业传奇。Ericsson 的 AXD 301 ATM 交换机使用 Erlang/OTP 运行，9 年运行时间内仅停机 31.55 秒。Erlang 的"Let it crash"哲学：Actor（进程）崩溃时 supervisor Actor 自动重启它，不影响其他进程运行。这种容错模型只在 Actor 的隔离特性下才可行——共享状态的线程崩溃会影响整个进程。
- **Ray (Python)** — 分布式 Actor 模型，用于 ML 训练和推理的并行调度。Ray 将每个 ML 任务（参数服务器、训练 worker、推理服务）封装为 Actor，Actor 之间通过异步消息协调训练流程。参数服务器 Actor 汇聚梯度，训练 worker Actor 发送梯度消息，推理 Actor 接收模型更新消息——整个训练流程通过 Actor 消息链完成。
- **Discord** — 在 2020 年从 Go 微服务迁移到 Elixir（基于 Erlang VM）来处理消息分发。Discord 的每个用户会话是一个 Elixir Actor（GenServer），用户之间的消息传递通过 Actor 间消息完成。Elixir/Erlang VM 的 Actor 模型让 Discord 用 5 台服务器替代了之前的数百台 Go 微服务实例——Actor 的轻量级进程（每个占用约 2KB 内存）让单机可以运行数百万并发连接。

## 进一步阅读

- Carl Hewitt — Actor 模型原始论文 (1973) — "A Universal Modular ACTOR Formalism for Artificial Intelligence"，定义了 Actor 的基本语义和计算模型
- 《Akka in Action》 — JVM Actor 框架实战，从基础 Actor 到集群、流处理和容错的完整指南
- Erlang/OTP 文档 — [erlang.org](https://www.erlang.org/) 电信级 Actor 系统参考，OTP 的 supervisor 和 application 模式是 Actor 容错的最佳实践
- Gul Agha — 《ACTORS: A Model of Concurrent Computation in Distributed Systems》 (1986) — 将 Hewitt 的理论发展为可实现的编程模型，定义了 Actor 的接收规则和消息语义
