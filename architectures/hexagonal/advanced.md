# Spring Boot：六边形架构（端口与适配器）的经典实现

## 软件简介

Spring Boot 是 Pivotal 团队于 2014 年发布的 Java 应用框架，它基于 Spring 框架提供自动配置、内嵌服务器、starter 依赖管理等能力，让开发者"开箱即用"快速构建应用。Spring Boot 的核心是依赖注入（DI）——通过 @Autowired 自动组装对象，这天然支持了六边形架构的"端口与适配器"模式：核心业务定义接口（端口），适配器实现接口，DI 容器负责注入。

## 该软件的架构

Spring Boot 六边形架构由三层组成：

- **Core（核心领域）**：纯业务逻辑，不依赖任何外部技术。核心定义两种端口：(1) 入站端口——核心暴露的业务接口（如 UserService.register），供外部调用；(2) 出站端口——核心定义的依赖接口（如 UserRepositoryPort、NotificationPort），声明"我需要什么能力"，但不关心谁来实现。核心包（com.app.core）不导入任何适配器包。
- **Driving Adapter（入站适配器）**：REST Controller、消息监听器等，它们是外部世界调用核心的桥梁。@RestController 实现了入站适配器——将 HTTP 请求翻译为核心业务调用。Driving Adapter 依赖核心，核心不依赖它。
- **Driven Adapter（出站适配器）**：JPA Repository、邮件客户端、外部 API 客户端等，它们实现核心定义的出站端口。@Repository 实现 UserRepositoryPort，@Service 实现 NotificationPort。Driven Adapter 可以自由替换——换数据库、换邮件服务、换通知渠道，核心代码零修改。

```
依赖方向 (箭头指向被依赖方):

  Driving Adapter          Core Domain          Driven Adapter
  (RestController)    →    (UserService)    ←    (JpaUserRepo)
       │                    │     │                  │
       │                    │     │                  │
  HTTP 请求            入站端口  出站端口           数据库
       │              (register)  (Port接口)         │
       └──────────────────→──────────────────←──────┘

  Spring DI 组装:
  @Service UserService(@Autowired repo, @Autowired notifier)
  @Repository JpaUserRepo implements UserRepositoryPort
  @Component EmailNotifier implements NotificationPort
```

## 简化实现思路

本示例模拟了 Spring Boot 六边形架构的核心机制：

| 简化概念 | 对应 Spring Boot 机制 |
|---------|---------------------|
| `UserRepositoryPort` / `NotificationPort` | Spring Boot 出站端口接口 |
| `UserService` 只依赖端口 | Spring @Service 只依赖接口，不依赖具体类 |
| `RestController` 调用核心 | Spring @RestController 作为入站驱动适配器 |
| `JpaUserRepository` 实现端口 | Spring @Repository 实现出站端口 |
| `bootstrap()` 组装 | Spring @Autowired DI 容器自动注入 |
| 适配器可替换（Email→Log） | Spring DI 允许切换实现（@Profile/@Qualifier） |

## 与真实实现的对照

| 简化实现 | 真实 Spring Boot |
|---------|----------------|
| Python ABC 抽象接口 | Java Interface + @Autowired 注入 |
| `bootstrap()` 手动组装 | Spring ApplicationContext 自动扫描 + @Component |
| 字典模拟数据库 | Spring Data JPA + Hibernate + PostgreSQL |
| print 模拟 HTTP | Spring MVC DispatcherServlet + HTTP 协议 |
| 无包结构约束 | 真实项目用包结构强制依赖方向（core 不导入 adapter 包） |
| 无 AOP | Spring AOP 提供事务管理、日志切面等 |
| 无配置文件 | Spring Boot application.yml + @Profile 切换适配器 |

## 学习建议

1. **理解"端口"的含义**：端口不是网络端口，而是"核心与外界的契约"。入站端口是核心暴露的业务能力（"我能做什么"），出站端口是核心声明的依赖需求（"我需要什么"）。核心定义端口，适配器实现端口——这就是"依赖倒置"。
2. **包结构是六边形的保证**：六边形架构不只是接口设计，更重要的是包结构。真实的 Spring Boot 项目应将 core、driving-adapter、driven-adapter 分为不同包，并确保 core 包不导入任何 adapter 包。IDE 的依赖检查可以强制执行这个约束。
3. **Spring DI 是六边形的天然搭档**：Spring 的 @Autowired 自动将适配器注入核心——开发者只声明"我需要 UserRepositoryPort"，Spring 自动找到 JpaUserRepository 实现并注入。这让替换适配器变得极为简单——加一个 @Profile 注解即可。
4. **延伸阅读**：研究 Spring Boot 的 @Profile 机制（按环境切换适配器）和 @Conditional 注解（按条件注入实现），理解 Spring DI 如何在运行时动态选择适配器组合。
