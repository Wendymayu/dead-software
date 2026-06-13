# Reactor 模式 (Reactor Pattern)

## 什么是 Reactor 模式

Reactor 模式是一种单线程事件驱动并发模型。事件循环（EventLoop）注册多个事件处理器（Handler），通过事件多路分离（Demultiplexing）将事件分发给对应的处理器，实现单线程处理多个并发 I/O 源而不阻塞。

## 核心思想

**单线程事件循环 + Handler 分发**：不用多线程，而是用一个事件循环监听所有事件源，事件到来时分发给对应的 Handler 处理。

```
┌──────────────────────────────────────┐
│           EventLoop (Reactor)        │
│  ┌──────────┐                        │
│  │ 事件队列   │ ← 事件多路分离          │
│  │  type     │                        │
│  └──────────┘                        │
│       ↓ 分发                          │
│  ┌───┴────────────────────────┐      │
│  │  handlers 注册表            │      │
│  │  "read"  → ReadHandler     │      │
│  │  "write" → WriteHandler    │      │
│  └────────────────────────────┘      │
└──────────────────────────────────────┘
```

关键机制：
- **事件循环** — 循环取出事件并分发，永不阻塞
- **Handler 注册** — 注册事件类型与处理器映射
- **多路分离** — 根据事件类型找到对应 Handler
- **非阻塞** — Handler 忄须快速处理，不能阻塞循环

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Handler / ReadHandler / WriteHandler** — 不同事件类型的处理器
2. **EventLoop** — 核心类，包含 `_handlers`（注册表）和 `_events`（事件队列）
3. **register()** — 注册事件类型与 Handler 的映射
4. **post()** — 将事件放入队列
5. **run()** — 循环取出事件，根据类型分发给对应 Handler

## 优缺点

**优点**
- 单线程简化——不需要线程同步，避免竞态条件
- 高吞吐——I/O 密集场景下单线程处理并发更高效
- 可扩展——新增 Handler 只需注册，不修改事件循环

**缺点**
- CPU 密集瓶颈——长时间计算会阻塞整个事件循环
- Handler 必须快速——任何阻塞操作都会拖慢所有事件处理
- 调试困难——异步事件流比同步调用链更难追踪

## 真实项目中的应用

- **Node.js** — 整个运行时基于 Reactor 模式（libuv 事件循环）
- **Nginx** — 单线程事件驱动处理高并发 HTTP 请求
- **Python asyncio** — 事件循环 + 协程的 Reactor 实现
- **Redis** — 单线程事件驱动处理网络请求和命令
- **Netty (Java)** — Reactor 模式的高性能网络框架

## 进一步阅读

- 《POSIX 网络编程》 (Douglas C. Schmidt) — Reactor 模式的原始定义
- 《Node.js 设计模式》 — Reactor 模式在 JavaScript 中的实践
- Python `asyncio` 模块文档 — 事件循环和协程的实现细节
- 《C10K 问题》 — 为什么 Reactor 模式比多线程更适合高并发 I/O
