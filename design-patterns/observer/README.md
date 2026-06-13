# 观察者模式 (Observer Pattern)

## 什么是观察者模式

观察者模式定义了对象间一对多的依赖关系：当一个对象（被观察者/Subject）的状态发生变化时，所有依赖于它的对象（观察者/Observer）都会自动收到通知并更新。也叫"发布-订阅"模式。

## 核心思想

**被动通知取代主动查询**：观察者不需要不停地问"数据变了吗"，而是在订阅后自动收到变化通知。

```
Subject ──notify──→ Observer A
                  → Observer B
                  → Observer C
```

关键机制：
- **attach/detach** — 动态增减观察者
- **notify** — 状态变化时统一推送
- **update** — 每个观察者自行决定如何响应

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Subject** — 维护 `_observers` 列表，`set_state()` 改状态后自动调用 `notify()`
2. **三个 Observer** — EmailNotifier（发邮件）、Logger（记日志）、AlertSystem（高温警报），各自对同一事件做不同反应
3. **条件响应** — AlertSystem 根据 state 值决定是否发警报——观察者可以选择性响应
4. **动态性** — 可以随时 `attach` 新观察者而不改 Subject 代码

注意 AlertSystem 的条件判断：同一事件触发通知，但不同观察者可以有不同的响应策略——这是观察者模式的灵活性所在。

## 优缺点

**优点**
- 解耦——Subject 和 Observer 不需要知道彼此的具体实现
- 动态订阅——可随时增减观察者
- 广播通信——一次通知，多个响应
- 符合开闭原则——新增观察者无需修改 Subject

**缺点**
- 通知顺序不可控——观察者收到通知的顺序不确定
- 性能风险——大量观察者同时响应可能造成性能问题
- 级联更新——观察者的更新可能触发新的通知，形成循环
- 调试困难——"这个更新是谁触发的？"可能难以追踪

## 真实项目中的应用

- **Vue.js / React** — 组件响应数据变化（Vue 的响应式系统本质就是观察者模式）
- **Python asyncio** — `asyncio.Event` 和回调机制
- **Java Observable** — 标准库中的 Observable/Observer（已弃用，推荐用 PropertyChangeListener）
- **RxJS** — Reactive Extensions，观察者模式的流式扩展

## 进一步阅读

- 《设计模式》 (GoF) — 观察者模式的经典定义
- 《Head First 设计模式》 — 观察者模式的生动讲解
- RxJS — [ReactiveX](http://reactivex.io/) — 观察者模式进化为响应式编程
