# SOA 架构 (Service-Oriented Architecture)

## 什么是 SOA

SOA（面向服务架构）将系统拆分为多个独立服务，服务之间通过标准契约（接口）通信。核心是 ESB（企业服务总线）——负责路由、转换、编排所有服务间交互。服务强调复用性和治理，而非独立部署速度。

## 核心思想

**标准契约 + ESB 协调 + 服务治理**：服务不直接通信，所有交互通过 ESB 路由和转换。

```
  Service A  Service B  Service C
     ↓           ↓           ↓
   标准契约     标准契约     标准契约
     ↓           ↓           ↓
              ESB (总线)
          路由/转换/编排/治理
```

关键特征：
- **ESB 是核心** — 与微服务的区别：SOA 用 ESB 集中协调，微服务用直接通信
- **标准契约** — 服务通过统一接口暴露能力，内部实现自由
- **服务治理** — ESB 统一负责日志、监控、错误处理、重试等横切关注点
- **复用优先** — 服务设计目标是跨业务线复用，而非单一场景快速交付

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **ESB** — 所有服务注册到 ESB，客户端通过 esb.call() 调用服务，ESB 负责路由
2. **UserService / OrderService / PaymentService** — 各服务独立，只提供标准 handle() 接口
3. **业务流程** — 查用户→下单→支付，每一步都通过 ESB，服务不直接互相调用
4. **与微服务对比** — 微服务中 OrderService 会直接调 UserService；SOA 中必须经过 ESB

ESB 是所有通信的中介——这是 SOA 与微服务最本质的区别。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示 SOA 的核心能力：**ESB 编排 + 消息转换 + 服务治理**。

- `orchestrate()` — ESB 编排跨服务的复合业务流程（PLACE_ORDER）
- 各服务用自己的术语（GET_USER vs GET, CREATE vs CREATE_ORDER）——ESB 负责转换
- 服务治理日志——ESB 记录所有调用，便于审计和监控

## 优缺点

**优点**
- 服务复用——同一服务可被多个业务线使用
- ESB 统一治理——路由、转换、监控、安全策略集中管理
- 松耦合——服务只依赖标准契约，不依赖其他服务的内部实现
- 便于集成——ESB 可桥接不同技术栈的服务

**缺点**
- ESB 单点瓶颈——所有通信经过 ESB，性能和可用性集中依赖
- 过度抽象——标准契约和消息转换增加复杂度，简单交互变重
- 部署耦合——服务复用意味着共享部署，不能独立演进
- 治理开销——ESB 配置、流程编排、消息转换需要专门团队维护

## 真实项目中的应用

- **企业 ESB** — IBM WebSphere ESB、Oracle Service Bus、Mule ESB
- **WebService/SOAP** — WSDL 契约 + SOAP 协议，SOA 的经典技术栈
- **银行核心系统** — 多个业务服务通过 ESB 编排转账、风控、清算流程

## 进一步阅读

- 《SOA Principles of Service Design》 (Thomas Erl) — SOA 设计原则的权威参考
- Martin Fowler — [SOA vs Microservices](https://martinfowler.com/articles/microservices.html)
- 《Enterprise Integration Patterns》 (Hohpe & Woolf) — ESB 和消息模式的经典著作
