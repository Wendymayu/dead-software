# REST架构 (Representational State Transfer)

## 什么是REST架构

REST（Representational State Transfer）是一种分布式系统架构风格，由Roy Fielding在2000年提出。REST定义了六项约束：资源通过URI标识、统一接口、无状态通信、可缓存、分层系统、按需代码。满足全部约束的系统称为"RESTful"。REST不只是"HTTP API"——它是一套架构约束，而非协议或实现。

**历史背景**：REST 由 Roy Fielding 在其 2000 年的博士论文 "Architectural Styles and the Design of Network-based Software Architectures" 中正式定义。Fielding 是 HTTP/1.0 和 HTTP/1.1 规范的主要作者之一（也是 Apache HTTP Server 的联合创始人），他在论文中系统化地分析了多种网络架构风格（管道与过滤器、客户端-服务器、分层系统、缓存、无状态、统一接口等），然后将这些风格组合为 REST。REST 的六项约束不是凭空发明——每一项约束都对应 Fielding 在 Web 基础协议设计中的实践经验。例如"无状态"约束来自 HTTP 最初设计的经验教训：早期 HTTP 实验中加入会话状态导致服务器内存消耗和扩展困难，去除状态后 HTTP 的水平扩展和缓存能力显著提升。"统一接口"约束来自 URI 和 HTTP 方法的标准化实践：统一的资源标识和操作语义让中间组件（代理、缓存）无需理解应用语义即可正确处理请求。REST 论文的核心贡献是将 Web 的成功经验（HTTP、URI、HTML）抽象为可复用的架构约束集合——不是"发明新架构"，而是"总结 Web 为什么能成功"。RESTful API 的实践推广则在 2010 年前后加速，随着移动端和微服务兴起，REST 成为 HTTP API 的主流风格。

**与相关模式的比较**：
- **SOAP/XML-RPC** — SOAP 是基于 XML 的协议，强调严格的接口契约（WSDL）、强类型、标准化错误处理。REST 是架构风格而非协议，强调统一接口（HTTP 方法）、资源导向、轻量级。SOAP 适合企业内部需要严格契约的场景，REST 适合开放 API 和轻量级集成。
- **GraphQL** — GraphQL 让客户端声明需要什么数据（精确查询），一次请求获取多个资源。REST 的统一接口固定返回资源的完整或预定义表示，客户端可能需要多次请求获取关联数据。GraphQL 解决了 REST 的"过度获取/获取不足"问题，但放弃了统一接口约束——每个查询都是自定义的。
- **gRPC** — gRPC 基于 Protocol Buffers 和 HTTP/2，强调高性能二进制通信、严格接口契约、双向流。REST 基于 JSON/HTTP/1.1，强调人类可读性、统一接口、与 Web 生态兼容。gRPC 适合服务间高性能内部通信，REST 适合面向外部开发者的公开 API。

## 核心思想

**统一接口 + 无状态（Uniform Interface + Stateless）**：将系统建模为一组资源，通过统一的GET/POST/PUT/DELETE操作，每次请求自带全部上下文。

这一原则的深层含义是：**系统应该对中间组件友好**。统一接口让代理、缓存、负载均衡器无需理解应用语义即可正确处理请求——代理看到 `GET /users` 知道这是读操作可以缓存，看到 `DELETE /users/1` 知道这是写操作需要转发。无状态让每个请求自足，服务器不需要维护会话——任何服务器实例都能处理任何请求，水平扩展变得简单。REST 的六项约束不是为开发者设计的，而是为整个网络生态设计的——让中间组件（代理、缓存、网关）能智能处理请求，让系统天然可扩展。

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

### 什么时候该用

- 公开 API（面向第三方开发者）——统一接口降低学习成本，HTTP/JSON 易于集成
- Web 和移动端后端——HTTP 天然适配，缓存和 CDN 加速读请求
- 微服务间轻量级通信——服务间不需要高性能二进制协议，REST 简单直观
- 需要利用 Web 基础设施——代理缓存、CDN 加速、负载均衡对 REST 请求天然友好

### 什么时候不该用

- 服务间高性能内部通信——gRPC/Protocol Buffers 的二进制通信性能显著优于 REST/JSON
- 复杂查询和嵌套数据——GraphQL 的声明式查询比 REST 的多次请求更高效
- 实时双向通信——WebSocket/Server-Sent Events 比 REST 的请求-响应模式更适合
- 需要严格接口契约——SOAP/WSDL 的强类型契约比 REST 的松散约定更可靠

### 常见误解

- **误解：REST 就是 HTTP API** — REST 是架构风格，HTTP 是协议。REST 的六项约束可以应用于任何协议——Fielding 的论文用 HTTP 作为 REST 的参考实现，但 REST 本身不绑定 HTTP。实际中 REST 几乎总是用 HTTP 实现，但这不是 REST 的定义要求。
- **误解：用了 HTTP 方法就是 RESTful** — Richardson 成熟度模型定义了 REST 的三个成熟度层级：Level 0（HTTP 作为隧道，所有操作用 POST）、Level 1（引入资源 URI）、Level 2（引入 HTTP 方法语义）、Level 3（HATEOAS 超媒体驱动）。用了 HTTP 方法只是 Level 2，真正的 RESTful 要求 Level 3（HATEOAS）。
- **误解：REST API 必须返回 JSON** — REST 的统一接口约束要求资源有标准化的表示(Representation)，但表示格式是媒体类型(Media Type)的选择——可以是 JSON、XML、HTML、PDF、图片。Fielding 在论文中强调：REST 的关键不是固定格式，而是客户端通过媒体类型理解资源的语义。

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **resources字典** — 模拟资源存储，URI(`/users`, `/orders`)标识不同资源集合
   - 每个 URI 对应一个资源集合——`/users` 是用户资源集合，`/orders` 是订单资源集合
   - 资源是 REST 的核心概念——系统围绕资源建模，而非围绕操作建模

2. **handle_request(method, uri, body)** — 统一接口：同一函数处理所有HTTP方法，语义由method决定
   - `GET /users` → 返回用户集合——读操作
   - `POST /users` + body → 创建新用户——写操作
   - `PUT /users/1` + body → 更新用户1——写操作（必须传完整对象）
   - `DELETE /users/1` → 删除用户1——写操作
   - 同一个函数处理四种方法——这就是统一接口：操作语义由方法决定，不由 URI 路径决定

3. **无状态验证** — PUT请求必须传完整对象（不能只传变更字段），DELETE必须传资源ID——请求自足
   - `PUT` 传完整对象：`{"name": "Alice_updated", "email": "alice_new@example.com"}`——请求包含理解此操作所需的全部信息
   - 不依赖之前的 GET 请求——服务器不需要记住"上次 GET 返回的 Alice 是什么"，客户端在 PUT 中传完整数据

4. **GET/POST/PUT/DELETE演示** — 四种操作依次执行，最终GET验证无状态累积效果
   - `GET /users` → 返回变更后的用户列表——两次 GET 返回相同结果，不依赖之前操作的历史

> **要点提示**：注意 `handle_request` 不保存任何会话状态——两次GET返回相同结果，不依赖之前的操作历史。这是无状态约束的核心：每个请求自足，服务器不维护会话。

> **要点提示**：PUT 必须传完整对象而非部分字段——这是无状态的要求。如果允许只传变更字段，服务器需要知道"当前 Alice 的完整状态是什么"才能合并更新，这隐式依赖了之前的 GET 请求——违反无状态约束。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示**HATEOAS（Hypermedia as the Engine of Application State）**——REST最被忽视的约束：

- 响应包含`_links`，列出当前状态下可用的后续操作
  - `_links` 是超媒体链接——包含 `rel`（关系类型）和 `href`（目标 URI）
  - 客户端通过 `rel` 理解链接语义：`rel=pay` 表示"支付此订单"，`rel=ship` 表示"发货此订单"

- 客户端跟随链接导航（`rel=pay` → `rel=ship`），无需硬编码URL
  - 客户端不需要知道 `/orders/1/pay` 或 `/orders/1/ship` 这些 URL——从响应的 `_links` 动态发现
  - 这意味着服务端可以自由改变 URL 结构——客户端跟随链接而非硬编码路径

- 状态流转由服务端控制：`pending` → `paid` → `shipped` → `completed`
  - `pending` 状态的订单有 `pay` 链接——可以支付
  - `paid` 状态的订单有 `ship` 链接——可以发货
  - `shipped` 状态的订单有 `complete` 链接——可以完成
  - 每个状态只暴露合法的后续操作——非法操作（如对已支付订单再次支付）的链接不存在

> **要点提示**：效果：客户端只需知道入口URL和媒体类型，所有业务流程通过超媒体链接动态发现。这是 HATEOAS 的核心价值——客户端不需要硬编码业务流程，服务端通过链接控制状态流转。

> **要点提示**：HATEOAS 是 REST 成熟度模型 Level 3 的要求——大部分自称"RESTful"的 API 只达到 Level 2（用了 HTTP 方法），没有实现 Level 3 的超媒体驱动。Fielding 明确表示：没有 HATEOAS 就不是 RESTful。

效果：客户端只需知道入口URL和媒体类型，所有业务流程通过超媒体链接动态发现。

## 优缺点

**优点**
- 简单直观——与HTTP天然契合，上手成本低。原因：HTTP 的 GET/POST/PUT/DELETE 方法语义与日常操作（读/写/改/删）对应，开发者无需学习新的操作语义
- 无状态利于缓存和水平扩展——每个请求独立处理。原因：无状态意味着任何服务器实例都能处理任何请求，不需要会话同步；GET 请求可以被代理和 CDN 缓存
- 统一接口降低学习成本——一套方法操作所有资源。原因：学会了 GET/POST/PUT/DELETE 就能操作任何资源，不需要为每个资源学习不同的操作方式
- 与现有Web基础设施兼容（代理、缓存、负载均衡）。原因：REST 的统一接口让中间组件无需理解应用语义即可正确处理请求——代理缓存 GET、转发 POST/PUT/DELETE

**缺点**
- 纯REST难以满足复杂业务——HATEOAS在实践中极少完整实现。原因：HATEOAS 要求响应包含所有可用后续操作的链接，实现复杂且响应体积增大；大多数 API 只用 HTTP 方法（Level 2），不实现超媒体驱动（Level 3）
- 无状态不适合长事务——多步操作需要客户端自行管理状态。原因：无状态要求每个请求自足，多步业务流程（如购物车→支付→发货）的状态需要客户端维护或通过其他机制（如 JWT token）传递
- 过度依赖HTTP——非HTTP场景（消息队列、RPC）不适用。原因：REST 的统一接口和无状态约束基于 HTTP 的语义设计，在消息队列（异步通信）、RPC（强契约通信）等场景中不合适
- 资源建模有时不自然——某些业务操作难以映射为资源CRUD。原因：如"激活用户"是业务操作而非资源变更——用 `POST /users/1/activate` 还是 `PUT /users/1 {status: "active"}`？资源建模对纯操作型业务不够直观

### 适用场景

- 公开 API——面向第三方开发者，HTTP/JSON 易于集成
- Web 和移动端后端——读多写少，缓存和 CDN 加速读请求
- 微服务间简单通信——服务间调用不需要高性能，REST 简直观
- 需要利用 Web 生态——代理缓存、CDN、负载均衡对 REST 天然友好

### 不适用场景

- 高性能服务间通信——gRPC/Protocol Buffers 的二进制通信性能更好
- 复杂嵌套数据查询——GraphQL 的声明式查询比 REST 的多次请求更高效
- 实时双向通信——WebSocket 比 REST 的请求-响应更适合
- 强契约内部通信——SOAP/WSDL 或 gRPC 的强类型契约更可靠

## 真实项目中的应用

- **GitHub API** — 典型RESTful API，资源（repo/issue/pr）通过URI标识，统一接口操作。GitHub API 的资源建模清晰：`/repos/:owner/:repo` 是仓库资源，`/repos/:owner/:repo/issues` 是仓库下的 issue 资源集合，`/repos/:owner/:repo/issues/:number` 是特定 issue。GET/POST/PUT/DELETE 操作语义固定
- **Stripe API** — 优秀的REST设计，严格遵循资源命名和HTTP语义。Stripe 的 API 设计被业界广泛参考：资源 URI 使用复数名词(`/customers`, `/charges`)，HTTP 方法语义严格（POST 创建、GET 读取、PUT 更新、DELETE 删除），错误响应使用标准 HTTP 状态码
- **Spring Boot REST** — Java生态最流行的REST框架，`@RestController` + 资源映射。Spring Boot 的 REST 开发体验极简：`@GetMapping("/users")` 对应 GET 操作，`@PostMapping("/users")` 对应 POST 操作，方法注解直接映射 HTTP 语义
- **Django REST Framework** — Python生态标准REST工具，Serializer + ViewSet。DRF 的 ViewSet 自动提供 list/create/retrieve/update/destroy 五个标准操作，映射为 GET/POST/GET/PUT/DELETE，统一接口由框架保证
- **PayPal 的支付 API** — PayPal 的公开支付 API 采用 REST 设计：支付(Payment)是核心资源，通过 `/payments/payment` URI 标识，创建支付用 POST、查询支付用 GET、更新支付用 PATCH。PayPal 在 API 设计中特别注重 HTTP 状态码的语义准确性——201(创建成功)、402(支付失败)、422(参数校验失败) 各有明确用途

## 进一步阅读

- Roy Fielding — [Architectural Styles and the Design of Network-based Software Architectures](https://www.ics.uci.edu/~fielding/pubs/dissertation/top.htm)（REST原始论文，2000，必读原文——第一章和第五章是核心）
- 《REST API Design Rulebook》 (Mark Masse) — REST API设计规则与实践，URI 设计、HTTP 方法语义、状态码选择的具体规则
- Martin Fowler — [Richardson Maturity Model](https://martinfowler.com/articles/richardsonMaturityModel.html) — REST 成熟度模型的三个层级：资源 → 方法 → 超媒体，理解"用了 HTTP 方法不等于 RESTful"
- 《RESTful Web APIs》 (Mike Amundsen & Leonard Richardson) — HATEOAS 和超媒体驱动的实践指南，超越 Level 2 达到真正 RESTful 的设计方法
