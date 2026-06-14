# 分层架构进阶：Django

## 软件简介

Django 是 Python 最流行的 Web 框架，采用 MTV（Model-Template-View）分层架构。它遵循"不要重复自己"(DRY)原则，通过清晰的层级分离让开发者各司其职：URL路由负责请求分发，View处理业务逻辑，Model封装数据访问，Template负责页面渲染。

## 该软件的架构

Django 的 MTV 分层架构（本质上与 MVC 相同，只是命名不同）：

1. **URL Dispatcher（路由层）**：请求入口
   - `urls.py` 定义 URL 模式与 View 的映射
   - 支持正则匹配、路径参数提取（如 `<pk>`）
   - 请求进入后首先匹配路由，找到对应的 View 函数

2. **View（业务逻辑层）**：Django 的"Controller"
   - 接收 HTTP 请求，调用 Model 获取数据
   - 将数据传递给 Template 渲染响应
   - Django 称之为 View 而非 Controller，因为它更侧重"展示逻辑"

3. **Model（数据层）**：Django 的 ORM
   - 每个 Model 类映射一张数据库表
   - ORM 自动生成 SQL，开发者用 Python 对象操作数据
   - 支持查询(`filter/get`)、创建(`create`)、更新(`save`)、删除(`delete`)
   - Manager/QuerySet 提供链式查询接口

4. **Template（展示层）**：响应格式化
   - Django Template Language：`{{ variable }}`、`{% tag %}`
   - 模板继承：`{% extends "base.html" %}` 实现布局复用
   - 模板只负责渲染，不含业务逻辑

**跨层机制**：
- **Middleware**：中间件，请求/响应的横切关注点（认证、日志、CORS等）
- **Signals**：信号，Model 事件通知（`post_save`、`pre_delete`等）

## 简化实现思路

我们的简化代码模拟了 Django 一个请求的完整流转：

- `URLDispatcher` → URL路由层，路径映射到 View 方法
- `DjangoView` → View层，协调 Model 和 Template
- `DjangoModel` → Model层，模拟 ORM 的 `get`/`filter` 操作
- `DjangoTemplate` → Template层，模拟模板渲染

数据流：请求 → URL路由匹配 → View调用Model → View调用Template → 返回响应

关键原则：View 只调用 Model 和 Template，不直接操作数据库或手写 HTML。

## 与真实实现的对照

| 简化代码 | 真实 Django | 说明 |
|---------|------------|------|
| `URLDispatcher` | `django.urls` | 真实支持正则、路径参数、命名路由、include分模块 |
| `DjangoView` | View函数/类 | 真实支持 FBV(函数视图) 和 CBV(类视图)，处理HttpRequest对象 |
| `DjangoModel` | Django ORM Model | 真实ORM映射数据库表，支持QuerySet链式查询、迁移管理 |
| `DjangoTemplate` | Django Template | 真实模板语言支持变量、标签、继承、过滤器 |
| 字典模拟数据库 | SQLite/PostgreSQL | 真实通过ORM连接实际数据库 |
| 无Middleware | Middleware | 真实Django有完整的中间件机制处理横切关注点 |
| 无Signals | Django Signals | 真实Django通过信号实现Model事件的观察者模式 |

## 学习建议

1. **理解分层本质**：每层只依赖下一层，不跨层调用。View调Model和Template，Template不调Model
2. **对比 MVC vs MTV**：Django的View=MVC的Controller，Django的Template=MVC的View，Django的Model=MVC的Model
3. **动手实践**：创建一个 Django 项目，观察 `urls.py → views.py → models.py → templates/` 的文件分层
4. **理解 ORM**：Django ORM 是分层的关键——Model层通过ORM完全屏蔽了SQL细节
5. **Middleware 的意义**：它是分层的"例外"——横跨所有层的关注点（认证、日志），理解它为什么不被放进某一层
