# Ruby on Rails：MVC 架构的经典实现

## 软件简介

Ruby on Rails（简称 Rails）是 David Heinemeier Hansson（DHH）于 2004 年发布的 Ruby Web 应用框架。Rails 以"约定优于配置"（Convention over Configuration）和"不要重复自己"（DRY）为核心理念，将 MVC 架构落地为高效的全栈 Web 开发体验。Rails 被广泛用于创业公司和成熟企业（Basecamp、Shopify、GitHub、Airbnb 早期均基于 Rails 构建）。

## 该软件的架构

Rails 的 MVC 架构由四层组成，请求从 Router 进入，经 Controller 调度 Model 获取数据，最终由 View 渲染响应：

- **Router（config/routes.rb）**：将 URL 映射到 Controller#action。Rails 的约定是 `resources :users` 自动生成 7 个标准路由（index/show/create/update/destroy 等），无需逐条配置。
- **Controller（app/controllers/）**：每个请求由一个 Controller Action 处理。Controller 的职责是"协调"——调用 Model 查数据，选 View 渲染，不做业务逻辑。Rails 约定：`UsersController#show` 自动渲染 `users/show.html.erb`。
- **Model（app/models/，ActiveRecord）**：Rails 的 Model 就是 ActiveRecord——ORM + 业务规则。ActiveRecord 提供查询（find/all/where）、验证（validates）、关联（has_many/belongs_to），将数据库表映射为 Ruby 类。
- **View（app/views/，ERB 模板）**：ERB（Embedded Ruby）模板将 Controller 传来的数据嵌入 HTML。View 只负责展示，不含逻辑。Rails 的 Helper（app/helpers/）提供格式化辅助方法。

```
请求流: GET /users/1
  │
  ├─ Router: config/routes.rb → UsersController#show
  │
  ├─ Controller: Users Controller 调用 User.find(1)
  │     │
  │     ├─ Model: ActiveRecord 查询 SELECT * FROM users WHERE id=1
  │     │
  │     └─ View: users/show.html.erb 渲染 <h1><%= @user.name %></h1>
  │
  └─ 响应: HTML 返回浏览器
```

## 简化实现思路

本示例模拟了 Rails MVC 的核心请求流程：

| 化概念 | 对应 Rails 机制 |
|---------|--------------|
| `Router.draw()` + `dispatch()` | Rails config/routes.rb 的 URL 映射 |
| `UsersController#index/show` | Rails Controller Action 方法 |
| `UserModel.find/all` | Rails ActiveRecord 的数据查询 |
| View 模板渲染 | Rails ERB 模板（`<%= user.name %>`） |
| Convention（自动匹配） | Rails 约定优于配置理念 |

## 与真实实现的对照

| 简化实现 | 真实 Rails |
|---------|----------|
| 简单字典路由 | Rails 支持 RESTful resources、嵌套路由、命名空间 |
| 直接调用 Model | Rails 有 before_action 过滤器、strong parameters 安全过滤 |
| 字典模拟数据库 | Rails ActiveRecord 连接真实数据库（PostgreSQL/MySQL） |
| print 模拟 ERB | Rails ERB 是真正的 Ruby 嵌入 HTML 模板引擎 |
| 无中间件 | Rails 有 Rack 中间件链（认证、CORS、日志） |
| 无请求对象 | Rails 有 ActionController::Parameters 和 Request/Response 对象 |

## 学习建议

1. **理解"约定优于配置"**：Rails 的核心哲学是——只要按约定命名（`UsersController` 对应 `users` 表），就能自动获得路由、视图路径、数据库映射。对比 Spring 的"一切都要配置"，思考约定如何减少冗余配置。
2. **Controller 是协调者，不是逻辑中心**：Rails Controller 的职责是"调度"——拿到参数、调 Model、选 View。业务逻辑应放 Model（ActiveRecord）或 Service Object，不要把 Controller 写成"上帝对象"。
3. **ActiveRecord 的双面性**：ActiveRecord 同时是 ORM 和业务模型——简单场景下极为高效，但复杂业务中容易导致 Model 臃肿。学习 Service Object、Concern 等 Rails 社区的解耦方案。
4. **延伸阅读**：研究 Rails 的 Request/Response 生命周期（Rack 中间件链），理解 Rails 如何从 Rack 框架一步步演进为全栈 MVC 框架。
