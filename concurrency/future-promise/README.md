# Future/Promise 模式 (Future/Promise Pattern)

## 什么是 Future/Promise 模式

Future/Promise 是异步计算的占位符模式。Future 开始时为空（结果尚未计算），调用方通过 `.get()` 阻塞等待直到异步计算完成并设置结果。Promise（生产方）负责设置结果，Future（消费方）负责获取结果。

## 核心思想

**异步结果的占位符**：发起异步计算后立即拿到一个 Future，不需要等待计算完成。需要结果时调用 `.get()`，如果计算已完成则立即返回，否则阻塞等待。

```
┌──────────┐                    ┌──────────┐
│ 主线程    │                    │ 工作线程  │
│          │                    │          │
│ future ← │ ←─ 创建Future ──→ │          │
│ future   │                    │ 计算中... │
│ .get()?  │ ←── 阻塞等待 ──→ │          │
│ future   │ ←─── set结果 ─── │ 完成！    │
│ .get() ✓ │ ←─── 立即返回 ─── │          │
└──────────┘                    └──────────┘
```

关键机制：
- **Future** — 结果的占位符，`get()` 阻塞等待，`is_done()` 查询状态
- **Event 同步** — `threading.Event` 实现阻塞/唤醒机制
- **set()** — 生产方（Promise）设置结果并唤醒等待者
- **get()** — 消费方等待 Event 触发后返回结果

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Future.__init__()** — `_result` 为 None，`_done` 为 Event（未触发）
2. **Future.set()** — 设置 `_result` 并 `_done.set()` 唤醒所有等待者
3. **Future.get()** — `_done.wait()` 阻塞直到 set() 被调用，然后返回结果
4. **async_compute()** — 在子线程中模拟耗时计算，完成后调用 `future.set()`

## 优缺点

**优点**
- 异步执行——发起计算后不阻塞主线程
- 简洁接口——`get()` 一步获取结果，无需复杂回调
- 可组合——多个 Future 可组合为更复杂的异步流程

**缺点**
- 阻塞等待——`get()` 会阻塞调用线程
- 无回调——不如回调模式灵活，无法在结果就绪时自动触发后续操作
- 异常处理——计算失败时的异常传递需要额外设计

## 真实项目中的应用

- **Python asyncio** — `asyncio.Future` 是协程异步结果的标准占位符
- **Java CompletableFuture** — 支持 thenApply/thenCompose 等链式操作
- **JavaScript Promise** — 浏览器和 Node.js 的异步编程基础
- **C++ std::future** — C++11 标准库的异步结果占位符
- **Go channel** — 虽非 Future 模式，但 channel 可以实现类似效果

## 进一步阅读

- 《Java 并发编程实践》 — Future 的线程安全实现与异常处理
- Python `concurrent.futures` 模块文档 — Future 的标准库实现
- 《异步编程设计模式》 — Future/Promise/回调/协程的对比与选择
- JavaScript Promise 规范 (Promises/A+) — Promise 的标准化定义
