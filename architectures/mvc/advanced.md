# Spring MVC：Java 世界 MVC 架构的标准实现

## 软件简介

Spring MVC 是 Spring Framework 的 Web 模块，由 Rod Johnson 于 2003 年发布，是 Java 企业级 Web 开发中使用最广泛的 MVC 实现。Spring MVC 的核心设计是**DispatcherServlet 前端控制器模式**——所有 HTTP 请求都通过一个统一的入口点（DispatcherServlet），再由它分派到具体的 Handler（Controller）、ViewResolver 等组件处理。Spring MVC 被 Spring Boot 大幅简化后，已成为 Java Web 开发的事实标准。

## 该软件的架构

Spring MVC 的请求处理流程是一条清晰的组件链：

```
请求流: GET /users/1
  │
  ├─ DispatcherServlet (前端控制器)
  │     ├─ HandlerMapping: URL -> Controller#方法
  │     ├─ Controller: @GetMapping 处理请求
  │     │     ├─ Service: 业务逻辑
  │     │     │     └─ Repository: 数据访问 (JPA/Hibernate)
  │     │     └─ 返回: 逻辑视图名 "users/detail" + Model 数据
  │     ├─ ViewResolver: "users/detail" -> templates/users/detail.html
  │     └─ View: 渲染模板 + 数据 -> HTML 响应
  │
  └─ 响应: HTML 返回浏览器
```

关键组件：

- **DispatcherServlet** — 唯一的前端控制器，所有请求的统一入口。它协调 HandlerMapping、Controller、ViewResolver 等组件，是整个 MVC 流程的"指挥中心"。对应设计模式中的 Front Controller 模式。
- **HandlerMapping** — 将 URL 映射到 Controller 方法。Spring 默认使用 `RequestMappingHandlerMapping`，解析 `@RequestMapping` / `@GetMapping` / `@PostMapping` 注解。
- **Controller (@RestController / @Controller)** — 业务协调者。Controller 不做业务逻辑，而是调用 Service 层获取数据，选择返回逻辑视图名或直接返回 JSON（@RestController）。
- **Service (@Service)** — 业务逻辑层。Spring 推荐将业务规则放在 Service 而非 Controller 或 Repository，保持 Controller 轻量。
- **Repository (@Repository)** — 数据访问层。Spring Data JPA 让 Repository 只需定义接口，自动生成 CRUD 实现。
- **ViewResolver** — 将 Controller 返回的逻辑视图名（如 `"users/detail"`）解析为实际模板路径（如 `/templates/users/detail.html`）。Thymeleaf 是 Spring Boot 默认模板引擎。

**Spring MVC 与 Rails MVC 的关键区别：**

| 对比项 | Spring MVC | Rails |
|--------|-----------|-------|
| 前端控制器 | DispatcherServlet（显式） | Rails Router（隐式） |
| 路由定义 | 注解 @GetMapping（分散在Controller中） | config/routes.rb（集中配置） |
| 视图解析 | ViewResolver（逻辑名→模板路径） | Convention（自动匹配） |
| 数据层 | Repository + JPA（分离） | ActiveRecord（ORM=Model） |
| 业务层 | Service（独立层） | Model 中混入业务逻辑 |
| 配置哲学 | 约定 + 配置均可 | 约定优于配置 |

## 简化实现思路

本示例模拟了 Spring MVC 的核心请求处理链：

| 简化概念 | 对应 Spring MVC 机制 |
|---------|---------------------|
| `DispatcherServlet.do_dispatch()` | Spring DispatcherServlet 的 doDispatch() 方法 |
| `HandlerMapping` 字典 | RequestMappingHandlerMapping 解析注解 |
| `UserController#show/list` | @GetMapping("/users/{id}") / @GetMapping("/users") |
| `UserService.getUser/listUsers` | @Service 业务逻辑层 |
| `UserRepository.findById/findAll` | @Repository + Spring Data JPA |
| `ViewResolver.resolve()` | ThymeleafViewResolver 解析逻辑视图名 |

Spring MVC 比 Rails 更显式地分离了每一层的职责：Controller 只做协调，Service 只做业务，Repository 只做数据，ViewResolver 只做视图解析。这种严格分层让每层可独立替换——比如把 Thymeleaf 换成 FreeMarker，只需换一个 ViewResolver，Controller 不受影响。

## 与真实实现的对照

| 简化实现 | 真实 Spring MVC |
|---------|---------------|
| 字典路由映射 | @RequestMapping 注解 + RequestMappingHandlerMapping |
| 直接调用 Service | Spring DI 自动注入 @Autowired |
| 字典模拟数据库 | Spring Data JPA + Hibernate 连接真实数据库 |
| print 模拟模板渲染 | Thymeleaf 模板引擎渲染真实 HTML |
| 无拦截器 | HandlerInterceptor（登录检查、日志等） |
| 无异常处理 | @ExceptionHandler + HandlerExceptionResolver |
| 无参数绑定 | @RequestParam / @PathVariable 自动解析 |
| 无数据验证 | @Valid + Hibernate Validator |
| 无内容协商 | ContentNegotiation（同一URL返回HTML或JSON） |

## 学习建议

1. **理解 DispatcherServlet 的"前端控制器"角色** — 它不是"另一个 Controller"，而是所有 Controller 的入口和协调者。理解这个角色，就能理解 Spring MVC 为什么能灵活地插入拦截器、异常处理器、视图解析器——它们都挂在 DispatcherServlet 的处理链上。
2. **Controller-Service-Repository 三层分离** — Spring MVC 推荐 Controller 只做"协调"（拿到参数、调 Service、选视图），Service 只做业务规则，Repository 只做数据访问。对比 Rails 的 ActiveRecord（Model=ORM+业务），思考哪种方式更适合复杂业务场景。
3. **注解驱动 vs 配置文件** — Spring MVC 用注解（@GetMapping、@Service、@Autowired）替代 XML 配置。对比 Rails 的 routes.rb 集中路由配置，思考"分散在代码中"和"集中在一个文件"各自的优缺点。
4. **延伸阅读** — 研究 Spring Boot 如何简化 Spring MVC 配置（自动配置 ViewResolver、内置 Tomcat、自动注册 DispatcherServlet），理解"约定 + 配置"如何平衡灵活性和简洁性。
