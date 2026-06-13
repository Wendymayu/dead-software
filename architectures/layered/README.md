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
