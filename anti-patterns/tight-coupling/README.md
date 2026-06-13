# 紧耦合 (Tight Coupling)

## 什么是紧耦合

紧耦合是一种反模式——模块直接依赖具体实现而非抽象接口。OrderService 在构造函数中直接创建 StripeGateway，更换支付方式就必须修改 OrderService 的代码。依赖注入版本通过抽象接口实现松耦合，切换实现只需改传入参数。

## 核心思想

**直接依赖具体实现**：BadOrderService 硬编码依赖 StripeGateway，任何变更（换支付方式、加测试 Mock）都必须修改 BadOrderService 本身。

```
┌──────────────────┐
│ BadOrderService   │ ← 直接依赖具体实现
│ ──→ StripeGateway │    换支付？改 OrderService！
│    (硬编码)        │    测试？改 OrderService！
└──────────────────┘

        vs

┌──────────────────┐
│ GoodOrderService  │ ← 依赖抽象接口
│ ──→ PaymentGateway│    换支付？改传入参数！
│    (ABC)          │    测试？传 MockImpl！
└──────────────────┘
        ↑
┌───────┴──────────────────┐
│ StripeImpl │ AlipayImpl │ ← 具体实现注入
└──────────────────────────┘
```

关键问题：
- **硬编码依赖** — 构造函数直接创建具体类
- **替换困难** — 换实现必须修改依赖方代码
- **测试困难** — 无法注入 Mock 进行单元测试
- **扩展受限** — 新增实现需要修改已有代码

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **BadOrderService.__init__()** — `self._gateway = StripeGateway()`，硬编码创建
2. **PaymentGateway (ABC)** — 抽象接口，定义 `charge()` 方法签名
3. **StripeImpl / AlipayImpl** — 两种具体实现，都继承 PaymentGateway
4. **GoodOrderService.__init__()** — `self._gateway = gateway`，接受注入的抽象接口

## 反面

**为什么是反模式**
- 替换困难——换支付方式必须改 OrderService 代码
- 测试困难——无法注入 Mock，单元测试被迫依赖真实 StripeGateway
- 扩展受限——新增支付方式需要修改 if-else 或构造函数
- 维护负担——依赖链越长，一处修改的连锁反应越大

**正确做法**
- 依赖注入——通过构造函数或配置传入抽象接口的实现
- 抽象接口——定义高层和低层都依赖的抽象
- 配置驱动——运行时通过配置选择具体实现

## 真实项目中的应用

- **Spring IoC 容器** — 自动依赖注入，避免紧耦合
- **Django settings** — 通过配置切换数据库后端，不修改业务代码
- **测试框架** — Mock 对象替代真实依赖，依赖注入使 Mock 可行
- **遗留系统** — 很多老代码直接创建数据库连接、第三方客户端

## 进一步阅读

- 《架构整洁之道》 (Robert C. Martin) — 依赖倒置原则与紧耦合的对抗
- 《依赖注入》 (Mark Seemann) — DI 模式的系统化讲解
- 《重构》 (Martin Fowler) — 如何从紧耦合重构为依赖注入
