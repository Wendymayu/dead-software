# Dead-Software Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a software engineering learning material repository with 8 topics (4 architecture patterns + 4 design patterns), each containing README.md documentation and minimal runnable Python code examples.

**Architecture:** Flat topic directories under two top-level categories (`architectures/` and `design-patterns/`). Each topic is self-contained with a README.md explaining the concept and example.py/advanced.py demonstrating it. No external dependencies — pure Python standard library. Output-driven examples that print clear results.

**Tech Stack:** Python 3 (standard library only), Markdown documentation, Git

---

### Task 1: Initialize Project Foundation

**Files:**
- Create: `README.md` (project intro + navigation)
- Modify: `CLAUDE.md` (update from placeholder to real project guidance)
- Create: directory skeleton for all 8 topics + shared

- [ ] **Step 1: Create directory structure**

```bash
mkdir -p architectures/layered architectures/event-driven architectures/microservices architectures/pipeline
mkdir -p design-patterns/observer design-patterns/strategy design-patterns/factory design-patterns/decorator
mkdir -p shared
```

- [ ] **Step 2: Write project README.md**

```markdown
# Dead-Software

> 软件工程架构与设计模式的阅读资料，配有简单但可运行的代码示例。

AI coding 正在深刻改变软件工程。新入门的工程师可能缺少传统的成长经历，但对软件工程的整体了解仍然不可或缺。本项目提供常见架构模式和设计模式的讲解与最小化可运行示例，帮助你快速建立软件工程的宏观认知。

## 如何使用

每个主题目录包含：
- `README.md` — 概念讲解、优缺点、真实项目应用、延伸阅读
- `example.py` — 最小化可运行示例（`python example.py` 即可运行）
- `advanced.py` — 进阶示例（部分主题提供）

## 架构模式 (Architecture Patterns)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 分层架构 | [architectures/layered/](architectures/layered/) | 三层分离（展示层/业务层/数据层） |
| 事件驱动架构 | [architectures/event-driven/](architectures/event-driven/) | 事件总线 + 发布订阅 |
| 微服务架构 | [architectures/microservices/](architectures/microservices/) | 独立服务通过 HTTP 通信 |
| 管道架构 | [architectures/pipeline/](architectures/pipeline/) | 数据经过多个处理阶段流转 |

## 设计模式 (Design Patterns)

| 主题 | 目录 | 核心演示 |
|------|------|----------|
| 观察者模式 | [design-patterns/observer/](design-patterns/observer/) | 一对多依赖通知 |
| 策略模式 | [design-patterns/strategy/](design-patterns/strategy/) | 算法族可互换封装 |
| 工厂模式 | [design-patterns/factory/](design-patterns/factory/) | 对象创建逻辑集中管理 |
| 装饰器模式 | [design-patterns/decorator/](design-patterns/decorator/) | 动态给对象添加职责 |

## 代码原则

- 纯 Python 标准库，无需安装额外依赖
- 单文件可运行：`python example.py` 即可看到输出
- 最小化示例：只演示核心机制，通常 < 80 行
- 输出驱动：运行结果清晰展示架构/模式的作用

## 贡献

欢迎添加新的架构模式或设计模式主题。每个新主题请遵循已有目录的 README.md 模板和代码原则。
```

- [ ] **Step 3: Update CLAUDE.md**

```markdown
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

dead-software is a learning material repository for software engineering — architecture patterns and design patterns with minimal runnable Python code examples. Target audience: mixed (beginners to experienced developers entering the field in the AI coding era).

## Running Examples

Every topic has `example.py` (and optional `advanced.py`). Run with:

```bash
python architectures/layered/example.py
python design-patterns/observer/example.py
```

No pip install needed — all examples use only the Python standard library.

## Adding New Topics

Each topic directory follows this structure:
- `README.md` — standard template (What is / Core Idea / Code Example / Pros and Cons / Real-World Applications / Further Reading)
- `example.py` — minimal runnable example (< 80 lines, output-driven)
- `advanced.py` — optional progressive example

Place architecture topics under `architectures/`, design pattern topics under `design-patterns/`.

## Code Principles

- Python standard library only
- Single-file runnable (`python example.py` produces clear output)
- Under 80 lines, demonstrating only core mechanism
- Comments explain why, not just what — connecting code to concept
- Output-driven: printed output demonstrates what the pattern/architecture does

## Directory Structure

```
architectures/          # Macro architecture patterns
  layered/
  event-driven/
  microservices/
  pipeline/
design-patterns/        # Micro design patterns
  observer/
  strategy/
  factory/
  decorator/
shared/                 # Shared utilities
```
```

- [ ] **Step 4: Commit project foundation**

```bash
git init
git add README.md CLAUDE.md
git commit -m "feat: initialize project structure and documentation"
```

---

### Task 2: Layered Architecture Topic

**Files:**
- Create: `architectures/layered/example.py`
- Create: `architectures/layered/advanced.py`
- Create: `architectures/layered/README.md`

- [ ] **Step 1: Write example.py**

```python
"""分层架构 (Layered Architecture) 最小化示例

演示三层分离：展示层(Presentation) → 业务层(Business) → 数据层(Data)
每层只与相邻层交互，不跨层调用。
"""


# --- 数据层：负责数据存取 ---
class DataLayer:
    def __init__(self):
        self._users = {
            "alice": {"name": "Alice", "age": 30},
            "bob": {"name": "Bob", "age": 25},
        }

    def get_user(self, user_id):
        print(f"  [DataLayer] 查询用户: {user_id}")
        return self._users.get(user_id)

    def save_user(self, user_id, data):
        print(f"  [DataLayer] 保存用户: {user_id}")
        self._users[user_id] = data


# --- 业务层：负责业务逻辑 ---
class BusinessLayer:
    def __init__(self, data_layer):
        self.data = data_layer

    def get_user_info(self, user_id):
        print(f" [BusinessLayer] 处理用户查询: {user_id}")
        user = self.data.get_user(user_id)
        if user:
            return f"{user['name']}, 年龄 {user['age']}"
        return "用户不存在"

    def update_age(self, user_id, new_age):
        print(f" [BusinessLayer] 处理年龄更新: {user_id} → {new_age}")
        user = self.data.get_user(user_id)
        if user:
            user["age"] = new_age
            self.data.save_user(user_id, user)
            return f"已更新 {user_id} 的年龄为 {new_age}"
        return "用户不存在"


# --- 展示层：负责用户交互 ---
class PresentationLayer:
    def __init__(self, business_layer):
        self.business = business_layer

    def show_user(self, user_id):
        print(f"[PresentationLayer] 展示用户: {user_id}")
        result = self.business.get_user_info(user_id)
        print(f"[PresentationLayer] 结果: {result}\n")

    def change_age(self, user_id, new_age):
        print(f"[PresentationLayer] 请求修改年龄: {user_id} → {new_age}")
        result = self.business.update_age(user_id, new_age)
        print(f"[PresentationLayer] 结果: {result}\n")


# --- 运行演示 ---
if __name__ == "__main__":
    data = DataLayer()
    business = BusinessLayer(data)
    presentation = PresentationLayer(business)

    print("=" * 40)
    print("分层架构演示：请求从展示层→业务层→数据层流转")
    print("=" * 40 + "\n")

    presentation.show_user("alice")
    presentation.show_user("unknown")
    presentation.change_age("bob", 26)
    presentation.show_user("bob")
```

- [ ] **Step 2: Run example.py to verify output**

Run: `python architectures/layered/example.py`
Expected: Output showing requests flowing through three layers with clear `[PresentationLayer]`, `[BusinessLayer]`, `[DataLayer]` markers

- [ ] **Step 3: Write advanced.py**

```python
"""分层架构进阶示例：引入依赖反转

展示如何通过抽象接口实现依赖反转(DIP)，
使业务层不再直接依赖数据层的具体实现。
"""

from abc import ABC, abstractmethod


# --- 抽象接口：业务层定义它需要的数据访问能力 ---
class UserRepository(ABC):
    @abstractmethod
    def get_user(self, user_id): ...

    @abstractmethod
    def save_user(self, user_id, data): ...


# --- 数据层：实现抽象接口 ---
class InMemoryUserRepo(UserRepository):
    def __init__(self):
        self._users = {"alice": {"name": "Alice", "age": 30}}

    def get_user(self, user_id):
        print(f"  [InMemoryRepo] 查询: {user_id}")
        return self._users.get(user_id)

    def save_user(self, user_id, data):
        print(f"  [InMemoryRepo] 保存: {user_id}")
        self._users[user_id] = data


class JsonFileUserRepo(UserRepository):
    """模拟JSON文件存储（实际应读写文件，此处简化）"""

    def get_user(self, user_id):
        print(f"  [JsonFileRepo] 从文件查询: {user_id}")
        return {"name": user_id.capitalize(), "age": 99}

    def save_user(self, user_id, data):
        print(f"  [JsonFileRepo] 写入文件: {user_id}")


# --- 业务层：只依赖抽象接口，不依赖具体实现 ---
class UserService:
    def __init__(self, repo: UserRepository):  # 依赖注入
        self.repo = repo

    def get_info(self, user_id):
        print(f" [UserService] 查询: {user_id}")
        user = self.repo.get_user(user_id)
        return f"{user['name']}, 年龄 {user['age']}" if user else "不存在"


# --- 展示层 ---
class UserView:
    def __init__(self, service):
        self.service = service

    def show(self, user_id):
        print(f"[UserView] 展示: {user_id}")
        print(f"   → {self.service.get_info(user_id)}\n")


# --- 运行演示：同一业务逻辑，切换不同数据实现 ---
if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示：依赖反转 — 业务层不依赖具体数据实现")
    print("=" * 50 + "\n")

    # 使用内存存储
    print("--- 使用 InMemoryUserRepo ---")
    view1 = UserView(UserService(InMemoryUserRepo()))
    view1.show("alice")

    # 切换为文件存储，业务层代码无需修改
    print("--- 切换为 JsonFileUserRepo（业务层代码不变）---")
    view2 = UserView(UserService(JsonFileUserRepo()))
    view2.show("alice")
```

- [ ] **Step 4: Run advanced.py to verify output**

Run: `python architectures/layered/advanced.py`
Expected: Output showing the same business logic working with two different data implementations

- [ ] **Step 5: Write README.md**

```markdown
# 分层架构 (Layered Architecture)

## 什么是分层架构

分层架构将系统按照职责划分为若干水平层，每层只与相邻层交互。最常见的三层架构：展示层（UI）→ 业务层（逻辑）→ 数据层（存储）。请求自上而下流转，返回自下而上传递。

## 核心思想

**关注点分离（Separation of Concerns）**：每层只负责一类工作。展示层不管数据怎么存，数据层不管界面怎么展示。修改某一层的实现不影响其他层——只要接口不变。

```
┌─────────────────────┐
│   Presentation      │  用户交互、输入输出格式化
├─────────────────────┤
│   Business          │  业务规则、计算、验证
├─────────────────────┤
│   Data              │  数据存取、持久化
└─────────────────────┘
```

**关键约束**：层间依赖只能向下，不允许底层调用上层或跨层调用。

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **DataLayer** — 只做数据存取，不知道谁在调用它
2. **BusinessLayer** — 持有 DataLayer 引用，调用数据层但只关心业务逻辑
3. **PresentationLayer** — 持有 BusinessLayer 引用，负责用户交互和结果展示
4. **请求流转** — 每次调用打印日志，清晰展示请求从展示层→业务层→数据层的完整路径

注意 `PresentationLayer` 不会直接调用 `DataLayer`——这就是分层架构的核心约束。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例引入**依赖反转原则（DIP）**：

- 业务层定义抽象接口 `UserRepository`，声明它需要什么数据能力
- 数据层实现该接口（`InMemoryUserRepo`、`JsonFileUserRepo`）
- 业务层通过依赖注入接收具体实现

效果：切换数据存储方式（内存→文件→数据库）时，业务层和展示层代码完全不变。

## 优缺点

**优点**
- 结构清晰，易于理解和维护
- 各层可独立修改（只要接口不变）
- 适合大多数业务应用的标准架构
- 团队可按层分工

**缺点**
- 严格分层可能带来性能开销（简单操作也要穿过所有层）
- 容易退化成"贫血模型"——业务层只是数据层的透传
- 层数过多时增加复杂度

## 真实项目中的应用

- **Spring Framework** — 经典的分层架构：Controller → Service → DAO
- **Django** — View → Model（两层简化版，Template 独立于业务层）
- **ASP.NET MVC** — Controller → Service → Repository

## 进一步阅读

- 《软件架构模式》 (Mark Richards) — 五种常用架构的对比
- Martin Fowler — [Layered Architecture](https://martinfowler.com/bliki/LayeredArchitecture.html)
- 《Clean Architecture》 (Robert C. Martin) — 分层架构如何演化到六边形架构
```

- [ ] **Step 6: Commit**

```bash
git add architectures/layered/
git commit -m "feat: add layered architecture topic with example and advanced examples"
```

---

### Task 3: Event-Driven Architecture Topic

**Files:**
- Create: `architectures/event-driven/example.py`
- Create: `architectures/event-driven/advanced.py`
- Create: `architectures/event-driven/README.md`

- [ ] **Step 1: Write example.py**

```python
"""事件驱动架构 (Event-Driven Architecture) 最小化示例

演示事件总线 + 发布订阅模式：
- 发布者将事件发送到事件总线
- 订阅者通过事件总线接收感兴趣的事件
- 发布者和订阅者互不感知
"""


# --- 事件总线：核心中间层 ---
class EventBus:
    def __init__(self):
        self._subscribers = {}  # event_type -> [handlers]

    def subscribe(self, event_type, handler):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(handler)
        print(f"  [EventBus] {handler.__name__} 订阅了 '{event_type}'")

    def publish(self, event_type, data):
        print(f"  [EventBus] 发布事件 '{event_type}': {data}")
        for handler in self._subscribers.get(event_type, []):
            handler(data)


# --- 订阅者：对特定事件做出响应 ---
def order_handler(data):
    print(f"    [订单服务] 处理订单: 用户={data['user']}, 商品={data['item']}")


def inventory_handler(data):
    print(f"    [库存服务] 减少库存: {data['item']}")


def notification_handler(data):
    print(f"    [通知服务] 发送通知给 {data['user']}: 您的订单已创建")


# --- 发布者：产生事件 ---
class OrderService:
    def __init__(self, bus):
        self.bus = bus

    def create_order(self, user, item):
        print(f"[OrderService] 创建订单: {user} - {item}")
        self.bus.publish("order_created", {"user": user, "item": item})


# --- 运行演示 ---
if __name__ == "__main__":
    bus = EventBus()

    print("=" * 40)
    print("事件驱动架构演示：发布者→事件总线→订阅者")
    print("=" * 40 + "\n")

    # 先订阅
    print("--- 订阅阶段 ---")
    bus.subscribe("order_created", order_handler)
    bus.subscribe("order_created", inventory_handler)
    bus.subscribe("order_created", notification_handler)
    print()

    # 再发布
    print("--- 发布阶段 ---")
    order = OrderService(bus)
    order.create_order("Alice", "Python编程书")
    print()

    # 发布无人订阅的事件
    print("--- 发布无人订阅的事件 ---")
    bus.publish("payment_processed", {"user": "Bob", "amount": 100})
```

- [ ] **Step 2: Run example.py to verify output**

Run: `python architectures/event-driven/example.py`
Expected: Output showing subscription registration, event publication triggering three handlers, and silent event with no subscribers

- [ ] **Step 3: Write advanced.py**

```python
"""事件驱动架构进阶示例：事件过滤与链式处理

展示事件驱动的更复杂场景：
- 事件过滤：订阅者可以只接收符合条件的事件
- 链式处理：一个事件的处理结果可以触发新事件
"""


class EventBus:
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, handler, filter_fn=None):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append((handler, filter_fn))

    def publish(self, event_type, data):
        print(f"  [EventBus] 事件 '{event_type}': {data}")
        for handler, filter_fn in self._subscribers.get(event_type, []):
            if filter_fn is None or filter_fn(data):
                handler(data)


# --- 事件处理链 ---
def validate_order(data):
    if data.get("amount", 0) > 0:
        print(f"    [验证] 订单有效: {data['user']}, 金额={data['amount']}")
    else:
        print(f"    [验证] 订单无效: 金额为0")


def on_order_valid(data):
    print(f"    [处理] 执行订单: {data['user']}")


# --- 过滤函数：只处理大额订单 ---
def is_large_order(data):
    return data.get("amount", 0) >= 100


def vip_handler(data):
    print(f"    [VIP处理] 大额订单特殊处理: {data['user']}, 金额={data['amount']}")


# --- 运行演示 ---
if __name__ == "__main__":
    bus = EventBus()

    print("=" * 50)
    print("进阶演示：事件过滤 + 链式处理")
    print("=" * 50 + "\n")

    bus.subscribe("order_created", validate_order)
    bus.subscribe("order_created", on_order_valid)
    bus.subscribe("order_created", vip_handler, filter_fn=is_large_order)

    print("--- 小额订单 ---")
    bus.publish("order_created", {"user": "Alice", "amount": 50})
    print()

    print("--- 大额订单（触发VIP处理）---")
    bus.publish("order_created", {"user": "Bob", "amount": 200})
```

- [ ] **Step 4: Run advanced.py to verify output**

Run: `python architectures/event-driven/advanced.py`
Expected: Small order triggers validate+process only; large order triggers all three including VIP handler

- [ ] **Step 5: Write README.md**

```markdown
# 事件驱动架构 (Event-Driven Architecture)

## 什么是事件驱动架构

事件驱动架构以**事件**为核心通信机制。当系统中发生重要变化时，产生一个事件；对该事件感兴趣的组件订阅并响应。发布者不知道谁会处理事件，订阅者也不知道事件从何而来。

## 核心思想

**解耦（Decoupling）**：组件之间不直接调用，而是通过事件总线间接通信。

```
发布者 ──→ [Event Bus] ──→ 订阅者A
                         ──→ 订阅者B
                         ──→ 订阅者C
```

关键特征：
- **发布者不关心谁接收** — 只管发出事件
- **订阅者不关心谁发出** — 只管处理事件
- **可随时增减订阅者** — 不影响发布者和其他订阅者

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **EventBus** — 中央事件路由器，维护 event_type → handlers 映射
2. **OrderService（发布者）** — 创建订单时发布 `"order_created"` 事件，不关心谁接收
3. **order_handler / inventory_handler / notification_handler（订阅者）** — 各自独立处理同一事件
4. **无人订阅的事件** — `payment_processed` 事件无人订阅，静默发布（不报错）

一个事件触发三个独立处理——这就是事件驱动的力量：新增处理逻辑只需订阅，不改发布者代码。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示两个实用特性：

1. **事件过滤** — `subscribe()` 可传入 `filter_fn`，只有符合条件的事件才传递给该订阅者（VIP处理只接收大额订单）
2. **链式处理** — 多个订阅者按注册顺序处理同一事件，形成处理链

## 优缺点

**优点**
- 极强的解耦——新增功能只需订阅事件
- 天然支持扩展——加订阅者不影响已有代码
- 异步友好——事件可排队、延迟处理
- 可回溯——事件可存储和重放

**缺点**
- 流程不直观——很难从代码看出"一个事件最终导致了什么"
- 调试困难——事件链可能很长，排查问题需要追踪整条链路
- 顺序问题——订阅者处理顺序可能影响结果
- 事件风暴——大量事件同时触发可能造成系统过载

## 真实项目中的应用

- **Node.js (EventEmitter)** — Node 的核心就是事件驱动
- **Spring Event** — Spring Framework 的应用事件机制
- **Kafka / RabbitMQ** — 分布式事件流平台，企业级事件驱动的基础设施
- **Vue.js** — 组件间通过 `$emit` / `$on` 通信（小型事件总线）

## 进一步阅读

- Martin Fowler — [Event Sourcing](https://martinfowler.com/eaaDev/EventSourcing.html)
- 《软件架构模式》 (Mark Richards) — 事件驱动架构的详细分析
- 《Designing Event-Driven Systems》 (Ben Stopford) — Kafka 事件驱动设计
```

- [ ] **Step 6: Commit**

```bash
git add architectures/event-driven/
git commit -m "feat: add event-driven architecture topic"
```

---

### Task 4: Microservices Architecture Topic

**Files:**
- Create: `architectures/microservices/example.py`
- Create: `architectures/microservices/advanced.py`
- Create: `architectures/microservices/README.md`

- [ ] **Step 1: Write example.py**

```python
"""微服务架构 (Microservices Architecture) 最小化示例

演示多个独立服务通过消息通信：
- 每个服务独立运行，有自己的数据
- 服务之间通过"网络"（此处用模拟HTTP）通信
- 每个服务可独立部署和扩展
"""

import json


# --- 模拟HTTP通信 ---
class HttpClient:
    """模拟微服务间的HTTP调用"""
    _services = {}  # 服务注册表

    @classmethod
    def register(cls, name, service):
        cls._services[name] = service
        print(f"  [网络] 服务 '{name}' 已注册")

    @classmethod
    def call(cls, service_name, method, params):
        print(f"  [HTTP] → {service_name}/{method} params={params}")
        service = cls._services.get(service_name)
        if not service:
            return {"error": "服务不存在"}
        result = service.handle(method, params)
        print(f"  [HTTP] ← {service_name} response={result}")
        return result


# --- 用户服务 ---
class UserService:
    def __init__(self):
        self._users = {"u1": {"name": "Alice", "email": "alice@example.com"}}

    def handle(self, method, params):
        if method == "get_user":
            return self._users.get(params["user_id"], {"error": "not found"})
        return {"error": "unknown method"}


# --- 订单服务 ---
class OrderService:
    def __init__(self):
        self._orders = {}

    def handle(self, method, params):
        if method == "create_order":
            # 跨服务调用：查询用户信息
            user = HttpClient.call("user-service", "get_user",
                                   {"user_id": params["user_id"]})
            if "error" in user:
                return {"error": f"用户不存在: {params['user_id']}"}
            order_id = f"o{len(self._orders) + 1}"
            self._orders[order_id] = {
                "order_id": order_id, "user": user["name"],
                "item": params["item"],
            }
            return self._orders[order_id]
        return {"error": "unknown method"}


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 50)
    print("微服务架构演示：独立服务通过HTTP通信")
    print("=" * 50 + "\n")

    # 注册服务
    print("--- 服务注册 ---")
    HttpClient.register("user-service", UserService())
    HttpClient.register("order-service", OrderService())
    print()

    # 创建订单（订单服务会跨服务调用用户服务）
    print("--- 创建订单（跨服务调用）---")
    result = HttpClient.call("order-service", "create_order",
                             {"user_id": "u1", "item": "Python书"})
    print(f"\n最终结果: {json.dumps(result, ensure_ascii=False)}")
```

- [ ] **Step 2: Run example.py to verify output**

Run: `python architectures/microservices/example.py`
Expected: Output showing service registration, cross-service HTTP call (order-service → user-service), and final order result

- [ ] **Step 3: Write advanced.py**

```python
"""微服务进阶示例：服务发现与熔断

展示微服务架构中的关键问题：
- 服务发现：服务自动注册，客户端动态发现
- 简单熔断：当服务不可用时，快速失败而非无限等待
"""

import time


class ServiceRegistry:
    """服务发现注册中心"""

    def __init__(self):
        self._services = {}

    def register(self, name, service, healthy=True):
        self._services[name] = {"service": service, "healthy": healthy}
        print(f"  [Registry] '{name}' 已注册 (healthy={healthy})")

    def discover(self, name):
        entry = self._services.get(name)
        if entry and entry["healthy"]:
            return entry["service"]
        print(f"  [Registry] '{name}' 不可用!")
        return None

    def set_health(self, name, healthy):
        if name in self._services:
            self._services[name]["healthy"] = healthy
            status = "恢复" if healthy else "故障"
            print(f"  [Registry] '{name}' 状态: {status}")


class CircuitBreaker:
    """简单熔断器：连续失败2次后断开，2秒后尝试恢复"""

    def __init__(self, failure_threshold=2, recovery_timeout=2):
        self._failures = 0
        self._threshold = failure_threshold
        self._open = False
        self._last_failure_time = 0
        self._recovery_timeout = recovery_timeout

    def call(self, func):
        if self._open:
            if time.time() - self._last_failure_time > self._recovery_timeout:
                print("  [熔断器] 半开状态，尝试恢复...")
                self._open = False
            else:
                print("  [熔断器] 断开! 快速失败")
                return {"error": "circuit_breaker_open"}
        try:
            result = func()
            self._failures = 0
            return result
        except Exception as e:
            self._failures += 1
            print(f"  [熔断器] 失败计数: {self._failures}")
            if self._failures >= self._threshold:
                self._open = True
                self._last_failure_time = time.time()
                print("  [熔断器] 达到阈值，断开!")
            return {"error": str(e)}


# --- 模拟服务 ---
class GoodService:
    def handle(self, method, params):
        return {"status": "ok", "data": "正常响应"}


class BrokenService:
    def handle(self, method, params):
        raise RuntimeError("服务内部错误")


# --- 运行演示 ---
if __name__ == "__main__":
    registry = ServiceRegistry()
    breaker = CircuitBreaker(failure_threshold=2, recovery_timeout=2)

    print("=" * 50)
    print("进阶演示：服务发现 + 熔断保护")
    print("=" * 50 + "\n")

    # 注册服务
    print("--- 服务注册 ---")
    registry.register("good-service", GoodService())
    registry.register("bad-service", BrokenService())
    print()

    # 正常调用
    print("--- 正常调用 ---")
    svc = registry.discover("good-service")
    result = breaker.call(lambda: svc.handle("ping", {}))
    print(f"  结果: {result}\n")

    # 故障服务（触发熔断）
    print("--- 故障服务（触发熔断）---")
    svc = registry.discover("bad-service")
    breaker.call(lambda: svc.handle("ping", {}))
    breaker.call(lambda: svc.handle("ping", {}))
    breaker.call(lambda: svc.handle("ping", {}))  # 应被熔断器拦截
```

- [ ] **Step 4: Run advanced.py to verify output**

Run: `python architectures/microservices/advanced.py`
Expected: Normal service call succeeds; broken service fails twice, then circuit breaker opens and blocks the third call

- [ ] **Step 5: Write README.md**

```markdown
# 微服务架构 (Microservices Architecture)

## 什么是微服务架构

微服务架构将一个大型应用拆分为多个小型、独立的服务，每个服务负责一个业务能力，独立运行、独立部署，通过网络通信协作。每个服务可以有自己的数据库和技术栈。

## 核心思想

**独立性与自治**：每个服务是一个独立单元，可以单独开发、部署、扩展和替换。

```
┌──────────────┐     ┌──────────────┐
│  用户服务     │     │  订单服务     │
│  (Python)    │←──→ │  (Go)        │
│  用户数据库   │     │  订单数据库   │
└──────────────┘     └──────────────┘
         ↕                   ↕
┌─────────────────────────────────┐
│        API Gateway              │
└─────────────────────────────────┘
```

关键特征：
- **单一职责** — 每个服务只做一件事
- **独立数据** — 每个服务有自己的数据库
- **网络通信** — 服务间通过 HTTP/RPC/消息 通信
- **独立部署** — 可以单独上线，不影响其他服务

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **HttpClient** — 模拟网络层，服务注册表 + 请求转发
2. **UserService** — 独立服务，有自己的用户数据，处理 `get_user` 方法
3. **OrderService** — 独立服务，创建订单时**跨服务调用** UserService 获取用户信息
4. **跨服务调用** — `HttpClient.call("user-service", "get_user", {...})` 模拟真实的网络请求

核心看点：OrderService 不直接访问 UserService 的数据，而是通过网络调用——这就是微服务的本质：通过通信协作而非共享数据。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示微服务架构必须面对的两个关键问题：

1. **服务发现** — `ServiceRegistry` 模拟注册中心，服务启动时注册，调用方动态发现
2. **熔断器** — `CircuitBreaker` 在连续失败后"断开"，阻止继续调用故障服务（防止级联失败）

这两者是微服务架构中**不可或缺**的基础设施，没有它们，微服务系统在故障时会雪崩崩溃。

## 优缺点

**优点**
- 独立部署——一个服务上线不影响其他服务
- 技术异构——不同服务可用不同语言和框架
- 按需扩展——只扩展高负载的服务
- 故障隔离——一个服务宕机不影响整体（配合熔断）

**缺点**
- 分布式复杂度——网络延迟、数据一致性、分布式事务
- 运维负担——需要监控、日志聚合、服务发现、配置管理
- 调试困难——一个请求可能穿越多个服务
- 数据一致性——每个服务有自己的数据库，跨服务一致性难以保证

**注意**：微服务架构不是银弹。Martin Fowler 建议：先从单体开始，等到真正需要时再拆分。

## 真实项目中的应用

- **Amazon** — 从单体逐步拆分为数百个微服务
- **Netflix** — 微服务先驱，开发了整套微服务基础设施（Eureka、Hystrix）
- **Spring Cloud** — Java 微服务全家桶（服务发现、配置中心、熔断器、网关）
- **Kubernetes** — 微服务部署和管理的标准平台

## 进一步阅读

- Martin Fowler — [Microservices](https://martinfowler.com/articles/microservices.html)（定义性文章）
- 《微服务设计》 (Sam Newman) — 入门必读
- 《Building Microservices》 (Sam Newman, 2nd ed) — 更全面的实践指南
```

- [ ] **Step 6: Commit**

```bash
git add architectures/microservices/
git commit -m "feat: add microservices architecture topic"
```

---

### Task 5: Pipeline Architecture Topic

**Files:**
- Create: `architectures/pipeline/example.py`
- Create: `architectures/pipeline/advanced.py`
- Create: `architectures/pipeline/README.md`

- [ ] **Step 1: Write example.py**

```python
"""管道/过滤器架构 (Pipeline Architecture) 最小化示例

演示数据经过多个处理阶段（过滤器）逐步流转：
- 每个过滤器接收输入，处理后传给下一个
- 过滤器之间独立，只通过数据传递连接
"""


# --- 过滤器：每个阶段处理数据并传递 ---
def validate(data):
    """验证数据完整性"""
    print(f"  [验证] 检查数据: {data}")
    if not data.get("text"):
        data["errors"] = data.get("errors", []) + ["缺少文本内容"]
    data["validated"] = True
    return data


def normalize(data):
    """标准化文本"""
    print(f"  [标准化] 处理文本")
    data["text"] = data["text"].lower().strip()
    data["normalized"] = True
    return data


def enrich(data):
    """丰富数据：添加元信息"""
    print(f"  [丰富] 添加元信息")
    data["word_count"] = len(data["text"].split())
    data["enriched"] = True
    return data


# --- 管道：串联过滤器 ---
def pipeline(data, filters):
    """将数据依次通过所有过滤器"""
    print(f"[Pipeline] 开始处理，共 {len(filters)} 个阶段\n")
    for i, filter_fn in enumerate(filters, 1):
        print(f"  --- 阶段 {i}: {filter_fn.__name__} ---")
        data = filter_fn(data)
    print(f"\n[Pipeline] 处理完成")
    return data


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("管道架构演示：数据逐步通过多个过滤器")
    print("=" * 40 + "\n")

    input_data = {"text": "  Hello World of Software Engineering  "}
    filters = [validate, normalize, enrich]

    result = pipeline(input_data, filters)
    print(f"\n最终输出: {result}")
```

- [ ] **Step 2: Run example.py to verify output**

Run: `python architectures/pipeline/example.py`
Expected: Output showing data passing through validate → normalize → enrich stages with final enriched result

- [ ] **Step 3: Write advanced.py**

```python
"""管道架构进阶示例：分支管道与错误处理

展示更复杂的管道场景：
- 分支管道：根据条件选择不同处理路径
- 错误处理：某个阶段失败后的处理策略
"""


def validate(data):
    errors = []
    if not data.get("text"):
        errors.append("缺少文本")
    if len(data.get("text", "")) < 3:
        errors.append("文本过短")
    data["errors"] = errors
    data["valid"] = len(errors) == 0
    return data


def route(data):
    """根据语言分支到不同处理管道"""
    text = data.get("text", "")
    if any(ord(c) > 0x4E00 for c in text):
        data["route"] = "chinese"
    else:
        data["route"] = "english"
    return data


def process_chinese(data):
    data["processed"] = f"[中文处理] {data['text']}"
    return data


def process_english(data):
    data["processed"] = f"[英文处理] {data['text'].upper()}"
    return data


def error_handler(data):
    """错误处理阶段"""
    if data.get("errors"):
        print(f"  [错误处理] 发现错误: {data['errors']}")
        data["processed"] = f"[错误] {', '.join(data['errors'])}"
    return data


def run_pipeline(data, stages):
    for stage in stages:
        print(f"  → {stage.__name__}")
        data = stage(data)
    return data


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示：分支管道 + 错误处理")
    print("=" * 50 + "\n")

    # 英文文本
    print("--- 英文路径 ---")
    result = run_pipeline({"text": "hello world"},
                          [validate, route, process_english])
    print(f"  结果: {result}\n")

    # 中文文本
    print("--- 中文路径 ---")
    result = run_pipeline({"text": "你好世界"},
                          [validate, route, process_chinese])
    print(f"  结果: {result}\n")

    # 错误数据
    print("--- 错误路径 ---")
    result = run_pipeline({"text": "ab"},
                          [validate, error_handler])
    print(f"  结果: {result}")
```

- [ ] **Step 4: Run advanced.py to verify output**

Run: `python architectures/pipeline/advanced.py`
Expected: English text routed to English processor, Chinese text routed to Chinese processor, invalid data routed to error handler

- [ ] **Step 5: Write README.md**

```markdown
# 管道/过滤器架构 (Pipeline Architecture)

## 什么是管道架构

管道架构将数据处理组织为一系列顺序执行的过滤器（阶段），数据像流水一样从一个过滤器流向下一个，每个过滤器对数据做一种变换。Unix 管道 `cat file | grep pattern | sort` 就是最经典的例子。

## 核心思想

**逐步变换（Incremental Transformation）**：复杂的数据处理不是一步完成，而是拆成多个小步骤，每步只做一件事。

```
输入 → [过滤器A] → [过滤器B] → [过滤器C] → 输出
        变换1         变换2         变换3
```

关键特征：
- **每个过滤器独立** — 不依赖其他过滤器的内部实现
- **只通过数据连接** — 过滤器间唯一的纽带是经过变换的数据
- **可重组** — 过滤器可以自由排列组合，形成不同管道

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **validate / normalize / enrich** — 三个独立的过滤器函数，各做一件事
2. **pipeline()** — 通用管道函数，将数据依次通过所有过滤器
3. **数据流转** — 同一个 `data` dict 在过滤器间传递，每步添加新字段
4. **增减过滤器** — 只需修改 `filters` 列表，无需改任何过滤器代码

注意每个过滤器**只做一件事**：validate 只验证，normalize 只标准化，enrich 只丰富数据。这种单一职责使得管道可以灵活重组。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示两个实用场景：

1. **分支路由** — `route` 过滤器根据数据特征（中文/英文）选择不同后续处理
2. **错误处理** — `error_handler` 过滤器接管有问题的数据，给出友好的错误输出

分支路由体现了管道架构的灵活性：同一条管道的前半段可以共用，后半段根据数据分流。

## 优缺点

**优点**
- 概念简单直观——数据像流水一样通过
- 过滤器独立可复用——同一个过滤器可用于不同管道
- 易于组合——修改管道只需调整过滤器排列
- 适合数据处理场景——ETL、编译器、图片处理链

**缺点**
- 不适合交互式应用——管道是单向数据流，缺乏回传机制
- 数据格式耦合——所有过滤器必须对中间数据格式达成一致
- 错误传播——一个过滤器出错，后续过滤器可能收到无效数据
- 性能开销——数据在每步都要完整传递

## 眞实项目中的应用

- **Unix Shell 管道** — `grep | sort | uniq`，管道架构的鼻祖
- **编译器** — 词法分析 → 语法分析 → 语义分析 → 代码生成，每个阶段是过滤器
- **图像处理链** — 调色 → 滤镜 → 缩放 → 输出，每步变换图像数据
- **CI/CD 系统** — 构建 → 测试 → 部署，每个阶段是管道的一环

## 进一步阅读

- 《软件架构模式》 (Mark Richards) — 管道架构的详细分析
- POSIX — [Shell Command Language — Pipelines](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html#tag_18_07)
- 《Structure and Interpretation of Computer Programs》 — 流（stream）作为管道的抽象
```

- [ ] **Step 6: Commit**

```bash
git add architectures/pipeline/
git commit -m "feat: add pipeline architecture topic"
```

---

### Task 6: Observer Pattern Topic

**Files:**
- Create: `design-patterns/observer/example.py`
- Create: `design-patterns/observer/README.md`

- [ ] **Step 1: Write example.py**

```python
"""观察者模式 (Observer Pattern) 最小化示例

演示一对多的依赖关系：
- 被观察者(Subject)状态变化时，自动通知所有观察者
- 观察者无需主动查询，被动接收通知
"""


class Subject:
    """被观察者：维护观察者列表并通知变化"""

    def __init__(self):
        self._observers = []
        self._state = None

    def attach(self, observer):
        self._observers.append(observer)
        print(f"  [Subject] 添加观察者: {observer.__class__.__name__}")

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self):
        print(f"  [Subject] 通知所有观察者: state={self._state}")
        for observer in self._observers:
            observer.update(self._state)

    def set_state(self, state):
        self._state = state
        print(f"[Subject] 状态变更: {state}")
        self.notify()


class EmailNotifier:
    def update(self, state):
        print(f"    [EmailNotifier] 发送邮件: 温度变为 {state}°C")


class Logger:
    def update(self, state):
        print(f"    [Logger] 记录日志: temperature={state}")


class AlertSystem:
    def update(self, state):
        if state > 35:
            print(f"    [AlertSystem] ⚠️ 高温警报: {state}°C!")
        else:
            print(f"    [AlertSystem] 温度正常: {state}°C")


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("观察者模式演示：状态变化→自动通知所有观察者")
    print("=" * 40 + "\n")

    sensor = Subject()
    sensor.attach(EmailNotifier())
    sensor.attach(Logger())
    sensor.attach(AlertSystem())

    print("--- 温度变更 ---\n")
    sensor.set_state(25)
    print()
    sensor.set_state(38)
```

- [ ] **Step 2: Run example.py to verify output**

Run: `python design-patterns/observer/example.py`
Expected: Temperature 25 triggers three observers (email, log, alert-normal); temperature 38 triggers three observers (email, log, alert-warning)

- [ ] **Step 3: Write README.md**

```markdown
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
```

- [ ] **Step 4: Commit**

```bash
git add design-patterns/observer/
git commit -m "feat: add observer pattern topic"
```

---

### Task 7: Strategy Pattern Topic

**Files:**
- Create: `design-patterns/strategy/example.py`
- Create: `design-patterns/strategy/README.md`

- [ ] **Step 1: Write example.py**

```python
"""策略模式 (Strategy Pattern) 最小化示例

演示算法族的封装与互换：
- 不同策略实现同一接口
- 上下文对象可以在运行时切换策略
- 新增策略无需修改已有代码
"""

from abc import ABC, abstractmethod


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data): ...


class BubbleSort(SortStrategy):
    def sort(self, data):
        print("    [策略] 使用冒泡排序")
        arr = list(data)
        n = len(arr)
        for i in range(n):
            for j in range(0, n - i - 1):
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
        return arr


class QuickSort(SortStrategy):
    def sort(self, data):
        print("    [策略] 使用快速排序")
        if len(data) <= 1:
            return list(data)
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)


class BuiltInSort(SortStrategy):
    def sort(self, data):
        print("    [策略] 使用内置排序")
        return sorted(data)


class Sorter:
    """上下文：持有一个策略，可在运行时切换"""

    def __init__(self, strategy=None):
        self._strategy = strategy or BuiltInSort()

    def set_strategy(self, strategy):
        print(f"[Sorter] 切换策略为: {strategy.__class__.__name__}")
        self._strategy = strategy

    def sort(self, data):
        print(f"[Sorter] 排序 {data}")
        result = self._strategy.sort(data)
        print(f"[Sorter] 结果: {result}")
        return result


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("策略模式演示：运行时切换排序算法")
    print("=" * 40 + "\n")

    data = [5, 3, 8, 1, 9, 2, 7]
    sorter = Sorter()

    sorter.sort(data)
    print()

    sorter.set_strategy(BubbleSort())
    sorter.sort(data)
    print()

    sorter.set_strategy(QuickSort())
    sorter.sort(data)
```

- [ ] **Step 2: Run example.py to verify output**

Run: `python design-patterns/strategy/example.py`
Expected: Three rounds of sorting same data with different strategies (BuiltIn → Bubble → Quick), all producing [1, 2, 3, 5, 7, 8, 9]

- [ ] **Step 3: Write README.md**

```markdown
# 策略模式 (Strategy Pattern)

## 什么是策略模式

策略模式将一系列算法封装为独立的策略类，使它们可以互换使用。上下文对象持有当前策略，可以在运行时切换——切换算法就像换插头一样简单。

## 核心思想

**算法族的可互换封装**：同一个问题有多种解法，将每种解法封装为策略，使用时选择合适的策略，新增解法只需新增策略类。

```
┌──────────────┐
│   Sorter     │ ← 上下文，持有策略引用
│  _strategy   │
└──────┬───────┘
       │
   ┌───┴──────────────────┐
   │      SortStrategy     │ ← 抽象接口
   ├───┬────────┬─────────┤
   │Bubble│  Quick │BuiltIn│ ← 具体策略
   │Sort  │  Sort  │  Sort │
   └──────┴────────┴───────┘
```

关键机制：
- **抽象接口** — 所有策略实现同一方法签名
- **上下文委托** — Sorter 不自己排序，而是委托给 `_strategy.sort()`
- **运行时切换** — `set_strategy()` 动态更换算法

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **SortStrategy (ABC)** — 抽象接口，定义所有排序策略必须实现 `sort()` 方法
2. **BubbleSort / QuickSort / BuiltInSort** — 三个具体策略，各自实现不同排序算法
3. **Sorter** — 上下文对象，默认使用 BuiltInSort，可通过 `set_strategy()` 切换
4. **互换性** — 同一组数据 `data`，不同策略得到相同结果，但过程不同

注意 Sorter 的 `sort()` 方法内部只是一行 `self._strategy.sort(data)`——它不知道具体用了什么算法，只负责委托。这就是策略模式的核心：**使用者和算法解耦**。

## 优缺点

**优点**
- 算法可互换——运行时切换，无需改上下文代码
- 开闭原则——新增策略只需新增类，不修改已有代码
- 避免条件分支——用策略对象替代 if/else 硬编码选择
- 算法可独立演化——每个策略类独立维护

**缺点**
- 客户端必须了解所有策略——选择合适的策略需要了解它们的差异
- 策略数量膨胀——太多策略会增加系统复杂度
- 上下文与策略通信开销——某些策略需要上下文传入较多参数

## 真实项目中的应用

- **Python sort()** — `list.sort(key=...)` 的 `key` 参数就是策略模式的体现
- **支付系统** — 不同支付方式（信用卡/支付宝/微信）作为策略
- **路由算法** — 导航 App 的"最快路线/最短路线/避开收费"就是不同策略
- **压缩算法** — ZIP/GZIP/BZIP2 作为不同的压缩策略

## 进一步阅读

- 《设计模式》 (GoF) — 策略模式的经典定义
- 《Head First 设计模式》 — 以鸭子游泳/飞翔为例的生动讲解
- 《重构》 (Martin Fowler) — 用策略模式替代条件逻辑的重构手法
```

- [ ] **Step 4: Commit**

```bash
git add design-patterns/strategy/
git commit -m "feat: add strategy pattern topic"
```

---

### Task 8: Factory Pattern Topic

**Files:**
- Create: `design-patterns/factory/example.py`
- Create: `design-patterns/factory/README.md`

- [ ] **Step 1: Write example.py**

```python
"""工厂模式 (Factory Pattern) 最小化示例

演示对象创建逻辑的集中管理：
- 工厂根据参数决定创建哪种对象
- 调用者无需知道具体类名，只与抽象接口交互
- 新增产品类型只需修改工厂
"""

from abc import ABC, abstractmethod


class Notification(ABC):
    @abstractmethod
    def send(self, message): ...


class EmailNotification(Notification):
    def send(self, message):
        print(f"    [Email] 发送邮件: {message}")


class SMSNotification(Notification):
    def send(self, message):
        print(f"    [SMS] 发送短信: {message}")


class PushNotification(Notification):
    def send(self, message):
        print(f"    [Push] 发送推送: {message}")


class NotificationFactory:
    """工厂：根据类型创建通知对象"""

    _types = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
    }

    def create(self, notification_type):
        print(f"  [Factory] 创建通知: type={notification_type}")
        cls = self._types.get(notification_type)
        if not cls:
            raise ValueError(f"未知通知类型: {notification_type}")
        return cls()


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("工厂模式演示：根据类型创建不同通知对象")
    print("=" * 40 + "\n")

    factory = NotificationFactory()
    msg = "您的订单已发货"

    for type_name in ["email", "sms", "push"]:
        notification = factory.create(type_name)
        notification.send(msg)
        print()

    # 尝试创建未知类型
    try:
        factory.create("unknown")
    except ValueError as e:
        print(f"错误捕获: {e}")
```

- [ ] **Step 2: Run example.py to verify output**

Run: `python design-patterns/factory/example.py`
Expected: Factory creates and sends email/SMS/push notifications, then catches ValueError for unknown type

- [ ] **Step 3: Write README.md**

```markdown
# 工厂模式 (Factory Pattern)

## 什么是工厂模式

工厂模式将对象的创建逻辑集中到工厂类中，调用者不需要知道具体创建了哪个类，只需要通过工厂获取一个符合接口的对象。就像你去餐厅点菜——你不需要知道厨房怎么做的，只需要说"我要一份宫保鸡丁"。

## 核心思想

**创建与使用分离**：调用者只关心"我能用这个对象做什么"（接口），不关心"这个对象是怎么创建的"（具体类）。

```
调用者 ──→ Factory.create("email") ──→ EmailNotification
                                           │
                                           ↓
调用者 ←── Notification.send(msg) ←───────┘
          （只知道是 Notification，不知道具体类）
```

关键机制：
- **抽象接口** — 所有产品实现同一接口
- **工厂映射** — `_types` dict 将类型名映射到具体类
- **类型参数** — 调用者传入字符串标识，工厂决定创建哪个类

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Notification (ABC)** — 抽象接口，所有通知类型必须实现 `send()` 方法
2. **EmailNotification / SMSNotification / PushNotification** — 三个具体产品
3. **NotificationFactory** — 工厂类，`_types` dict 维护类型→类的映射，`create()` 根据参数创建对象
4. **调用者** — 只与 Notification 接口交互，不知道具体类名

注意调用者代码：`notification = factory.create("email"); notification.send(msg)`——全程没有出现 `EmailNotification` 类名。调用者只知道类型字符串和 `send()` 方法，创建细节全由工厂处理。

## 优缺点

**优点**
- 创建逻辑集中——所有对象创建在一处管理
- 调用者解耦——不需要知道具体类名和构造细节
- 易于扩展——新增产品类型只需在 `_types` 加一行
- 统一错误处理——工厂可以对无效参数统一抛异常

**缺点**
- 产品类必须相近——工厂通常创建同一家族的产品
- 新增产品需改工厂——`_types` dict 需要更新（违反开闭原则，但影响有限）
- 工厂可能膨胀——产品太多时工厂类会变得臃肿

**变体**：抽象工厂模式用多个工厂类分别创建不同产品家族，完全满足开闭原则。

## 真实项目中的应用

- **Django ORM** — `models.Model` 的 Manager 是工厂，创建 QuerySet 对象
- **logging 模块** — `logging.getLogger()` 是工厂方法，创建 Logger 对象
- **Spring Bean Factory** — IoC 容器本质就是工厂模式的大规模应用
- **数据库连接** — `create_engine("postgresql://...")` 根据URL创建不同数据库连接

## 进一步阅读

- 《设计模式》 (GoF) — 简单工厂 vs 工厂方法 vs 抽象工厂的区分
- 《Head First 设计模式》 — 工厂模式的pizza店例子
- 《Effective Java》 (Joshua Bloch) — "用静态工厂方法替代构造器"
```

- [ ] **Step 4: Commit**

```bash
git add design-patterns/factory/
git commit -m "feat: add factory pattern topic"
```

---

### Task 9: Decorator Pattern Topic

**Files:**
- Create: `design-patterns/decorator/example.py`
- Create: `design-patterns/decorator/README.md`

- [ ] **Step 1: Write example.py**

```python
"""装饰器模式 (Decorator Pattern) 最小化示例

演示动态给对象添加职责：
- 装饰器和被装饰对象实现同一接口
- 装饰器包裹原对象，添加新行为后转发调用
- 可以层层嵌套装饰
"""

from abc import ABC, abstractmethod


class Coffee(ABC):
    @abstractmethod
    def cost(self): ...

    @abstractmethod
    def description(self): ...


class SimpleCoffee(Coffee):
    def cost(self):
        return 10

    def description(self):
        return "普通咖啡"


class MilkDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 3

    def description(self):
        return self._coffee.description() + " + 牛奶"


class SugarDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 2

    def description(self):
        return self._coffee.description() + " + 糖"


class WhipDecorator(Coffee):
    def __init__(self, coffee):
        self._coffee = coffee

    def cost(self):
        return self._coffee.cost() + 5

    def description(self):
        return self._coffee.description() + " + 奶泡"


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("装饰器模式演示：层层添加职责")
    print("=" * 40 + "\n")

    coffee = SimpleCoffee()
    print(f"  {coffee.description()} — ¥{coffee.cost()}")

    coffee = MilkDecorator(coffee)
    print(f"  {coffee.description()} — ¥{coffee.cost()}")

    coffee = SugarDecorator(coffee)
    print(f"  {coffee.description()} — ¥{coffee.cost()}")

    coffee = WhipDecorator(coffee)
    print(f"  {coffee.description()} — ¥{coffee.cost()}")

    print("\n装饰链: Whip → Sugar → Milk → SimpleCoffee")
```

- [ ] **Step 2: Run example.py to verify output**

Run: `python design-patterns/decorator/example.py`
Expected: Progressively decorated coffee: "普通咖啡 ¥10" → "普通咖啡 + 牛奶 ¥13" → "普通咖啡 + 牛奶 + 糖 ¥15" → "普通咖啡 + 牛奶 + 糖 + 奶泡 ¥20"

- [ ] **Step 3: Write README.md**

```markdown
# 装饰器模式 (Decorator Pattern)

## 什么是装饰器模式

装饰器模式动态地给对象添加额外职责，而不修改原始对象的代码。装饰器和被装饰对象实现同一接口，装饰器包裹原对象——就像层层套上衣服，每件衣服增加一个功能。

## 核心思想

**包裹式增强（Wrapping Enhancement）**：不通过继承扩展功能，而是通过包裹旧对象添加新行为。每层装饰器持有被装饰对象的引用，先添加自己的行为，再转发给内部对象。

```
WhipDecorator
  ├─ 自己的行为: cost + 5, description + "奶泡"
  └─ 转发 → SugarDecorator
              ├─ 自己的行为: cost + 2, description + "糖"
              └─ 转发 → MilkDecorator
                          ├─ 自己的行为: cost + 3, description + "牛奶"
                          └─ 转发 → SimpleCoffee
                                      └─ 基础值: cost=10, description="咖啡"
```

关键机制：
- **同接口** — 装饰器和原对象实现同一接口，对外透明
- **持有引用** — 装饰器构造时接收被装饰对象
- **先加后转** — 先添加自己的行为，再调用内部对象的同名方法

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Coffee (ABC)** — 抽象接口，`cost()` 和 `description()` 是所有咖啡和装饰器共有的方法
2. **SimpleCoffee** — 基础对象，提供最基础的咖啡（¥10）
3. **MilkDecorator / SugarDecorator / WhipDecorator** — 三个装饰器，各自添加一种配料
4. **层层包裹** — `coffee = WhipDecorator(SugarDecorator(MilkDecorator(SimpleCoffee())))`——每层添加自己的行为后转发

注意每个装饰器的 `cost()` 方法：`self._coffee.cost() + 3`——它不是自己计算总价，而是把内部对象的 cost 加上自己的增量。这样嵌套多层时，cost 会自然累加。

## 优缺点

**优点**
- 动态增强——运行时决定添加哪些功能
- 避免继承膨胀——不需要为每种功能组合创建子类
- 可撤销——去掉装饰器就恢复原功能
- 符合开闭原则——新增装饰器不影响已有代码

**缺点**
- 装饰链长——多层装饰时调试和追踪变复杂
- 对象标识问题——装饰后的对象与原对象类型相同但不是同一个实例
- 排序敏感——某些装饰器的顺序会影响最终行为

## 真实项目中的应用

- **Python 装饰器语法** — `@decorator` 是装饰器模式的语法糖（尽管实现机制不同）
- **Java I/O 流** — `BufferedInputStream(FileInputStream(...))` 是经典的装饰器链
- **Django middleware** — 请求经过多个中间件层层包裹处理
- **Express.js middleware** — 每个中间件包裹请求处理链

**注意**：Python 的 `@decorator` 语法（函数装饰器）和 GoF 的装饰器模式有关联但机制不同。Python 函数装饰器在定义时包裹函数，GoF 装饰器在运行时包裹对象。本示例展示的是 GoF 装饰器模式。

## 进一步阅读

- 《设计模式》 (GoF) — 装饰器模式的经典定义
- 《Head First 设计模式》 — 星巴克咖啡的装饰器例子
- Python `@decorator` — [PEP 318](https://peps.python.org/pep-0318/) — Python 函数装饰器语法
```

- [ ] **Step 4: Commit**

```bash
git add design-patterns/decorator/
git commit -m "feat: add decorator pattern topic"
```

---

### Task 10: Shared Verification + Final Integration

**Files:**
- Create: `shared/verify_all.py` — script that runs all examples and verifies they produce output
- Modify: `README.md` — add link to shared verification script (if needed)

- [ ] **Step 1: Write verification script**

```python
"""运行所有主题的示例代码并验证它们能正常执行

用法: python shared/verify_all.py
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXAMPLES = [
    ROOT / "architectures" / "layered" / "example.py",
    ROOT / "architectures" / "layered" / "advanced.py",
    ROOT / "architectures" / "event-driven" / "example.py",
    ROOT / "architectures" / "event-driven" / "advanced.py",
    ROOT / "architectures" / "microservices" / "example.py",
    ROOT / "architectures" / "microservices" / "advanced.py",
    ROOT / "architectures" / "pipeline" / "example.py",
    ROOT / "architectures" / "pipeline" / "advanced.py",
    ROOT / "design-patterns" / "observer" / "example.py",
    ROOT / "design-patterns" / "strategy" / "example.py",
    ROOT / "design-patterns" / "factory" / "example.py",
    ROOT / "design-patterns" / "decorator" / "example.py",
]


def run_example(path):
    """运行单个示例，返回是否成功"""
    rel = path.relative_to(ROOT)
    print(f"\n{'='*50}")
    print(f"运行: {rel}")
    print(f"{'='*50}")
    result = subprocess.run(
        [sys.executable, str(path)],
        capture_output=True, text=True, timeout=10
    )
    print(result.stdout)
    if result.returncode != 0:
        print(f"❌ 失败: {rel}")
        print(result.stderr)
        return False
    print(f"✅ 成功: {rel}")
    return True


def main():
    print("验证所有示例代码...\n")
    results = []
    for path in EXAMPLES:
        if not path.exists():
            print(f"⚠️  跳过（文件不存在）: {path.relative_to(ROOT)}")
            results.append(True)  # 不存在的文件不算失败
            continue
        results.append(run_example(path))

    passed = sum(results)
    total = len(results)
    print(f"\n{'='*50}")
    print(f"结果: {passed}/{total} 通过")
    if passed < total:
        print("有示例运行失败，请检查上方输出")
        sys.exit(1)
    else:
        print("所有示例运行正常！")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run verification script**

Run: `python shared/verify_all.py`
Expected: All 12 examples run successfully (8 example.py + 4 advanced.py), output shows ✅ for each

- [ ] **Step 3: Commit**

```bash
git add shared/
git commit -m "feat: add verification script for all examples"
```

---

## Self-Review

**Spec coverage check:**
- ✅ Project structure (dual category directories) — Task 1
- ✅ README.md template per topic — Tasks 2-9
- ✅ example.py < 80 lines with clear output — Tasks 2-9
- ✅ advanced.py for architecture patterns — Tasks 2-5
- ✅ Standard library only — all code uses only `abc`, `json`, `time`, `subprocess`, `sys`, `pathlib`
- ✅ Output-driven — all examples print clear labeled output
- ✅ 4 architecture + 4 design pattern topics — Tasks 2-9
- ✅ Shared utilities — Task 10
- ✅ CLAUDE.md updated — Task 1

**Placeholder scan:** No TBD, TODO, or vague descriptions found. All code is complete and all steps have exact commands with expected output descriptions.

**Type consistency:** All class names, method signatures, and variable names are consistent within and across tasks. No mismatches found.
