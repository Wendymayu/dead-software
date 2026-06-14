# Stripe API —— RESTful API 设计的标杆

## 软件简介

Stripe 是一家成立于 2010 年的在线支付平台，为互联网企业提供支付处理、订阅管理、欺诈检测等服务。Stripe 不仅是支付领域的领导者，更因其 API 设计的卓越质量而成为 RESTful API 设计的行业标杆。无数开发者和公司将 Stripe API 作为设计自己 REST API 的参考标准——它的资源命名一致性、HTTP 方法语义正确性、错误格式统一性、分页策略、幂等性机制，都是教科书级的最佳实践。

## 该软件的架构

Stripe API 的架构是 REST 原则的精确实现：

- **资源(Resource) + URL 命名**：Stripe 的 API 围绕资源组织，URL 采用一致的命名模式：
  - `/v1/customers` — 客户资源
  - `/v1/charges` — 支付资源
  - `/v1/subscriptions` — 订阅资源
  - URL 是名词(资源名)，不是动词(动作名)。这是 REST 的核心原则——URL 标识资源，HTTP 方法标识动作。

- **HTTP 方法语义正确**：
  - `GET /customers` — 列出所有客户（读操作）
  - `POST /customers` — 创建新客户（写操作）
  - `GET /customers/:id` — 获取指定客户（读操作）
  - `DELETE /subscriptions/:id` — 取消订阅（删除操作）
  - Stripe 不使用 `PUT /customers/:id/update` 这种"URL里包含动词"的反模式。

- **统一错误格式**：所有错误响应都遵循相同的 JSON 结构：
  ```json
  { "error": { "type": "card_error", "message": "Your card number is incorrect.", "code": "incorrect_number" } }
  ```
  开发者只需要一套错误处理逻辑，不需要为每种错误类型写不同的处理代码。

- **分页(Pagination)**：Stripe 使用 cursor-based 分页（`starting_after` + `has_more`），而非 offset 分页。cursor 分页在大数据集上性能更好，且不会因为数据变化导致重复或遗漏。

- **幂等性(Idempotency)**：Stripe 支持 `Idempotency-Key` 请求头。如果同一个幂等键被多次使用，Stripe 只执行一次操作，后续请求返回第一次的结果。这解决了网络不稳定导致的重复请求问题——重试不会产生重复创建。

- **HATEOAS-lite**：每个响应包含 `_links` 字段，提供关联资源的链接。例如支付响应包含客户链接，开发者可以跟随链接导航到相关资源，而不需要自己拼凑 URL。

```
POST /v1/charges
  → { id: "ch_123", amount: 2000, customer: "cus_1",
      _links: [{ rel: "self", href: "/v1/charges/ch_123" },
               { rel: "customer", href: "/v1/customers/cus_1" }] }
```

## 简化实现思路

本示例模拟 Stripe API 的核心设计要素：

1. **资源存储**：customers、charges、subscriptions 三个资源集合
2. **HTTP 方法映射**：POST=创建，GET=列出/获取，DELETE=取消
3. **统一错误格式**：所有错误返回 `{error: {type, message}}`
4. **cursor 分页**：GET /customers 支持 limit + starting_after
5. **幂等键**：POST 操作支持 Idempotency-Key，重复请求返回已有结果
6. **关联链接**：响应包含 _links，链接到相关资源

## 与真实实现的对照

| 简化实现 | Stripe 真实 API | 差异说明 |
|---------|---------------|---------|
| 内存存储 | Stripe 使用分布式数据库 | 真实 Stripe 有完整的数据持久化和事务保证 |
| 简单 ID 生成 | Stripe 使用有意义的前缀ID | 真实 Stripe ID 格式如 `cus_1234abcd`(前缀+随机) |
| 无速率限制 | Stripe 有严格的速率限制 | 真实 Stripe 每秒限制请求数，超出返回 429 错误 |
| 无认证 | Stripe 要求 API Key 认证 | 真实 Stripe 每个 API 请求都需要携带密钥 |
| 无版本管理 | Stripe 有明确的 API 版本 | 真实 Stripe 通过 `Stripe-API-Version` 头管理版本兼容 |
| 无 webhook | Stripe 支持 webhook 事件通知 | 真实 Stripe 资源变更时主动推送事件到回调 URL |

**Stripe API 的关键设计原则**：
1. **一致性优于灵活性**：所有资源遵循相同的 URL 模式、相同的错误格式、相同的分页策略。开发者学了一种资源的用法，就能推断所有资源的用法。
2. **渐进式复杂度**：简单的操作（创建客户）只需要最少的参数；复杂的操作（带元数据的支付）可以逐步添加可选参数。新手不会被复杂度吓到，老手有足够的灵活性。
3. **幂等性是安全网**：网络请求可能丢失、超时、重复。幂等键保证重试安全——这在大规模系统中是必不可少的基础设施。

## 学习建议

1. **直接阅读 Stripe API 文档**：Stripe 的 API 文档是业界公认的最佳文档之一。访问 stripe.com/docs，体验它的结构、示例、错误说明。好的 API 设计首先是好的文档。

2. **对比"差"的 REST API**：思考哪些 API 设计是反模式：URL 里包含动词（`/users/create`）、用 POST 做读操作、错误格式不一致、没有分页。对比 Stripe 的做法，理解"为什么 Stripe 的做法更好"。

3. **理解幂等性的价值**：在网络不稳定的环境中，客户端需要重试。如果没有幂等性，重试可能创建重复资源（两次 POST 创建了两个客户）。幂等键保证：同样的操作无论重试多少次，结果都一样。

4. **实践 cursor 分页**：对比 offset 分页（`GET /customers?page=2`）和 cursor 分页（`GET /customers?starting_after=cus_123`）。cursor 分页在大数据集上的性能更好，且不会因为新数据插入导致分页偏移。

5. **延伸到 OpenAPI/Swagger**：Stripe API 有完整的 OpenAPI 规范描述。学习如何用 OpenAPI 规范定义 REST API 的资源、方法、参数、响应格式——这是从"手工设计 API"到"规范驱动设计 API"的进化。
