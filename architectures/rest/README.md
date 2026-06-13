# REST架构 (Representational State Transfer)

## 什么是REST架构

REST（Representational State Transfer）是一种分布式系统架构风格，由Roy Fielding在2000年提出。REST定义了六项约束：资源通过URI标识、统一接口、无状态通信、可缓存、分层系统、按需代码。满足全部约束的系统称为"RESTful"。REST不只是"HTTP API"——它是一套架构约束，而非协议或实现。

## 核心思想

**统一接口 + 无状态（Uniform Interface + Stateless）**：将系统建模为一组资源，通过统一的GET/POST/PUT/DELETE操作，每次请求自带全部上下文。

```
客户端                    服务端
  │  GET /users         │
  │ ─────────────────→ │  [Resource: 用户集合]
  │  ← 200 + 数据       │
  │                     │
  │  POST /users        │  请求自带全部信息
  │ ─────────────────→ │  (无状态：不依赖之前的请求)
  │  ← 201 + 新资源     │
```

关键约束：
- **资源标识** — 每个资源有唯一URI，如 `/users/1`
- **统一接口** — GET读、POST创、PUT改、DELETE删，操作语义固定
- **无状态** — 每次请求必须包含理解该请求所需的全部信息

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **resources字典** — 模拟资源存储，URI(`/users`, `/orders`)标识不同资源集合
2. **handle_request(method, uri, body)** — 统一接口：同一函数处理所有HTTP方法，语义由method决定
3. **无状态验证** — PUT请求必须传完整对象（不能只传变更字段），DELETE必须传资源ID——请求自足
4. **GET/POST/PUT/DELETE演示** — 四种操作依次执行，最终GET验证无状态累积效果

注意`handle_request`不保存任何会话状态——两次GET返回相同结果，不依赖之前的操作历史。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示**HATEOAS（Hypermedia as the Engine of Application State）**——REST最被忽视的约束：

- 响应包含`_links`，列出当前状态下可用的后续操作
- 客户端跟随链接导航（`rel=pay` → `rel=ship`），无需硬编码URL
- 状态流转由服务端控制：`pending` → `paid` → `shipped` → `completed`

效果：客户端只需知道入口URL和媒体类型，所有业务流程通过超媒体链接动态发现。

## 优缺点

**优点**
- 简单直观——与HTTP天然契合，上手成本低
- 无状态利于缓存和水平扩展——每个请求独立处理
- 统一接口降低学习成本——一套方法操作所有资源
- 与现有Web基础设施兼容（代理、缓存、负载均衡）

**缺点**
- 纯REST难以满足复杂业务——HATEOAS在实践中极少完整实现
- 无状态不适合长事务——多步操作需要客户端自行管理状态
- 过度依赖HTTP——非HTTP场景（消息队列、RPC）不适用
- 资源建模有时不自然——某些业务操作难以映射为资源CRUD

## 真实项目中的应用

- **GitHub API** — 典型RESTful API，资源（repo/issue/pr）通过URI标识，统一接口操作
- **Stripe API** — 优秀的REST设计，严格遵循资源命名和HTTP语义
- **Spring Boot REST** — Java生态最流行的REST框架，`@RestController` + 资源映射
- **Django REST Framework** — Python生态标准REST工具，Serializer + ViewSet

## 进一步阅读

- Roy Fielding — [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)（REST原始论文，2000）
- 《REST API Design Rulebook》 (Mark Masse) — REST API设计规则与实践
- Martin Fowler — [RESTful](https://martinfowler.com/articles/richardsonMaturityModel.html) — Richardson成熟度模型
