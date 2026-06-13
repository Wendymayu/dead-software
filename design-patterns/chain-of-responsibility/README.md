# 责任链模式 (Chain of Responsibility Pattern)

## 什么是责任链模式

责任链模式让请求沿着处理器链传递，直到有一个处理器能够处理它。就像客服系统——简单问题由一级客服解决，中等问题升级到二级，复杂问题由三级专家处理。发送者无需知道谁最终处理了请求。

## 核心思想

**请求沿链传递，直到被处理**：每个处理器判断能否处理当前请求，能则处理，不能则传给链上的下一个处理器。发送者只与链头交互，不关心最终由谁处理。

```
Client ──→ Level1Handler ──能处理？──→ 处理并返回
                    │ 不能
                    └──→ Level2Handler ──能处理？──→ 处理并返回
                              │ 不能
                              └──→ Level3Handler ──能处理？──→ 处理并返回
                                        │ 不能
                                        └──→ 无人处理
```

关键机制：
- **处理器链** — 每个处理器持有下一个处理者的引用
- **判断与传递** — _can_handle() 判断，不能则传递给 _next
- **灵活组装** — 链的顺序和组成可运行时调整

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Handler** — 基类，handle() 是模板方法：先 _can_handle() 判断，能则 _do_handle()，不能则传递给 _next
2. **Level1Handler** — 处理 level ≤ 1 的简单问题，超出范围则传递
3. **Level2Handler** — 处理 level ≤ 2 的中等问题，一级已过滤简单问题，这里只处理中等
4. **链构建** — `Level1Handler(Level2Handler(Level3Handler()))` 嵌套构造，形成链式传递

注意 Handler.handle() 方法的模板结构：`if self._can_handle(request)` → 处理 → `elif self._next` → 传递 → `else` → 无人处理。这个骨架复用了责任链的核心逻辑，子类只需定义 _can_handle 和 _do_handle 两个差异步骤。

## 优缺点

**优点**
- 解耦发送者与处理者——发送者不知道哪个处理器最终处理
- 灵活组链——可运行时调整链的顺序和成员
- 开闭原则——新增处理器只需新增类并插入链中
- 责任分担——每个处理器只关注自己能处理的请求

**缺点**
- 请求可能无人处理——如果链末端无法处理，请求会"掉链"
- 调试困难——请求经过多个处理器，追踪"谁处理了"需要遍历链
- 性能开销——请求可能经过多个处理器才被处理
- 链顺序敏感——处理器顺序不当可能导致错误处理

## 真实项目中的应用

- **Servlet Filter** — Java Web 中的 FilterChain，请求依次通过认证→日志→权限过滤器
- **Express middleware** — Node.js 的中间件链，请求依次通过 body-parser→auth→router
- **Python logging** — Logger 的 Handler 链，日志依次传递给 StreamHandler→FileHandler→SMTPHandler
- **异常处理** — try/except 嵌套结构本质就是责任链——异常沿调用栈传递直到被捕获

## 进一步阅读

- 《设计模式》 (GoF) — 责任链模式的经典定义
- 《Head First 设计模式》 — 责任链模式的直观讲解
- Node.js Express — [Middleware 文档](https://expressjs.com/en/guide/using-middleware.html) — 责任链在 Web 框架中的经典应用
