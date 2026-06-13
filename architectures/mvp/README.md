# MVP 架构 (Model-View-Presenter)

## 什么是 MVP

MVP 将应用分为三部分：Model（数据和状态）、View（被动展示）、Presenter（全部逻辑）。View 完全被动，不观察 Model，所有交互由 Presenter 协调。这是 MVP 与 MVC 的核心区别——MVC 中 View 直接观察 Model，MVP 中 View 只是被 Presenter 驱动的"哑"接口。

**历史背景**：MVP 模式由 Taligent 公司的 Dolphin 小组于 1996 年在内部文档中首次正式定义。Taligent 是 Apple 和 IBM 的合资公司，致力于开发基于 OO 的下一代操作系统。Dolphin 小组在开发 UI 框架时发现传统 MVC 模式在复杂 UI 中存在问题——View 直接观察 Model 导致 Model 和 View 之间产生隐式依赖链，一个 Model 变更可能触发多个 View 的观察者回调，调试困难且无法控制更新顺序。他们的解决方案是让 View 完全被动：View 不观察 Model，只提供展示接口供 Presenter 调用。Presenter 成为 View 和 Model 之间的唯一桥梁，所有逻辑集中在 Presenter 中。此后 MVP 在 2000 年代被广泛传播——Martin Fowler 在 2006 年的 "UI Architectures" 文章中系统化梳理了 MVP 的两种变体（Passive View 和 Supervising Controller），Android 社区在 2010 年代将 MVP 作为主流 UI 架构推广。MVP 的影响力持续到 MVVM 出现之前——MVVM 通过数据绑定替代了 Presenter 的手动同步，但 MVP 在不支持数据绑定的平台（如 Android 原生开发、WinForms）中仍然是首选。

**与相关模式的比较**：
- **MVC (Model-View-Controller)** — MVC 中 View 直接观察 Model（通过观察者模式），Model 变更时自动通知 View 更新。MVP 中 View 不观察 Model，Presenter 从 Model 取数据后手动推给 View。MVP 的优势是 View 和 Model 完全解耦（View 不知道 Model 存在），代价是 Presenter 需要手动同步。
- **MVVM (Model-View-ViewModel)** — MVVM 通过数据绑定自动同步 ViewModel 和 View——ViewModel 属性变更时自动反映到 View，不需要手动调用 `show_xxx()`。MVVM 减少了 Presenter 的手动同步代码，但依赖框架提供数据绑定机制（如 Angular、Vue、WPF）。不支持数据绑定的平台不适合 MVVM。
- **传统三层架构** — 三层架构(UI → Business → Data)是服务端架构，关注服务分层；MVP 是客户端架构，关注 UI 交互分离。两者解决的问题域不同。

## 核心思想

**View 完全被动 + Presenter 全权控制**：Presenter 是唯一的逻辑中心，View 只提供展示接口，Model 只提供数据。

这一原则的深层含义是：**UI 逻辑应该与 UI 框架解耦**。Presenter 包含所有交互逻辑（验证、业务规则、数据获取、展示更新），但 Presenter 不依赖任何 UI 框架——它只依赖 View 的抽象接口。这意味着 Presenter 可以在没有真实 View 的情况下完整测试——只需 mock View 接口验证 Presenter 是否正确调用了 `show_user()` 或 `show_error()`。测试 Presenter 时不需要启动 Android Activity 或 Windows Form。

```
      用户输入
        ↓
    Presenter
     ↓    ↑
  操作   取数据
     ↓    ↑
   Model    View
   (数据)   (被动展示)
```

关键约束：
- **View 不观察 Model** — 与 MVC 的关键区别，View 不知道 Model 存在
- **View 是被动接口** — 只提供 show_xxx() 方法，由 Presenter 调用驱动
- **Presenter 控制一切** — 验证、业务逻辑、数据获取、展示更新都在 Presenter

### 什么时候该用

- 不支持数据绑定的 UI 框架——Android 原生、WinForms、Swing 等框架的 View 天然被动，MVP 手动驱动 View 比数据绑定更自然
- 需要高测试覆盖率的 UI 逻辑——Presenter 不依赖 UI 框架，可以独立单元测试
- 复杂交互逻辑——表单验证、多步骤流程、条件展示等逻辑集中到 Presenter 中清晰管理
- View 需要多实现——同一个业务逻辑需要 Console 视图、Web 视图、移动端视图

### 什么时候不该用

- 支持数据绑定的框架——Angular、Vue、WPF 等框架提供 MVVM 数据绑定，手动驱动 View 是多余工作
- 极简 UI——只有一个按钮、一个文本框的界面不需要 MVP 的三层分离
- 快速原型——原型阶段 UI 变化频繁，Presenter 的接口定义跟不上 UI 变化速度

### 常见误解

- **误解：MVP 就是 MVC 换了个名字** — MVP 与 MVC 有本质差异。MVC 中 View 观察 Model（Observer 模式），Model 变更自动通知 View；MVP 中 View 不观察 Model，Presenter 手动从 Model 取数据推给 View。这一差异导致 MVP 的 View 完全不知道 Model 存在，而 MVC 的 View 直接依赖 Model。
- **误解：Presenter 就是 Controller** — MVC 的 Controller 只处理用户输入分发，不负责从 Model 取数据推给 View（View 自己观察 Model）。MVP 的 Presenter 承担全部职责：接收输入、操作 Model、驱动 View 更新——Presenter 是"超级 Controller"。
- **误解：MVP 模式要求 View 是接口** — View 接口是 MVP 的最佳实践（方便测试和替换），但不是定义要求。MVP 的核心约束是 View 不观察 Model、Presenter 控制一切，View 可以是具体类而非接口——只是失去了 mock 测试的优势。

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **UserModel** — 只持有数据，没有通知机制（与 MVC 的 Model 不同）
   - `UserModel` 只有 `name` 和 `email` 属性——没有 `add_observer()`、没有 `notify()`，因为 MVP 中 View 不观察 Model
   - Model 在 MVP 中是最简单的组件——纯数据容器，不关心谁在用它

2. **UserView** — 完全被动：只有 show_user/show_error/show_success，自己不会主动做任何事
   - `show_user(name, email)` — Presenter 调用此方法展示用户信息，View 不决定展示什么、何时展示
   - `show_error(msg)` — Presenter 调用此方法展示错误信息
   - `show_success(msg)` — Presenter 调用此方法展示成功提示
   - View 没有"获取数据"的方法——它不知道数据从哪里来

3. **UserPresenter** — 接收输入、验证逻辑、更新 Model、驱动 View——全部逻辑集中在此
   - `update_user(name, email)` — 先验证（名称不为空、邮箱格式正确），再更新 Model，再从 Model 取数据推给 View
   - Presenter 是唯一知道 Model 和 View 同时存在的组件——它从 Model 取数据，调用 View 的方法展示

4. **update_user** — Presenter 先验证，再更新 Model，再从 Model 取数据推给 View，View 不主动获取
   - 验证失败 → `view.show_error()` — Presenter 决定展示错误
   - 验证成功 → `model.name = name` → `view.show_user(model.name, model.email)` — Presenter 手动同步

> **要点提示**：View 不观察 Model，Presenter 是唯一桥梁——这是 MVP 与 MVC 的本质区别。MVC 中 View 通过 Observer 监听 Model 变更自动更新；MVP 中 View 只提供方法供 Presenter 主动调用。

> **要点提示**：注意 Presenter 的 `update_user()` 方法中的手动同步流程——先 `model.name = name`，再 `view.show_user(model.name, model.email)`。这种"先写 Model 再推 View"的模式是 MVP 的标准做法，称为 Passive View 变体。Martin Fowler 定义了另一种变体 Supervising Controller——View 可以简单绑定 Model 属性（如显示 name），Presenter 只处理复杂逻辑。

View 不观察 Model，Presenter 是唯一桥梁——这是 MVP 与 MVC 的本质区别。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示 MVP 的核心优势：**View 接口抽象 + 多 View 切换**。

- `UserViewInterface` 是抽象接口，Presenter 只依赖它
  - Presenter 的构造函数接收 `view: UserViewInterface`——不引用具体 View 类
  - Presenter 只调用接口方法：`view.show_user()`、`view.show_error()`——不知道背后是 Console 还是 Table

- `ConsoleView` 和 `TableView` 是两种实现，切换时 Presenter 代码不变
  - `ConsoleView` 以文本形式展示——"用户: Alice, 邮箱: alice@example.com"
  - `TableView` 以表格形式展示——"| 字段 | 值 |" 的格式
  - 切换只需改组装代码：`UserPresenter(ConsoleView())` → `UserPresenter(TableView())`

- Presenter 可脱离真实 View 进行单元测试——只需 mock ViewInterface
  - 测试代码创建 MockView（记录 Presenter 调用了哪些方法、传了什么参数）
  - 测试验证 Presenter 的逻辑是否正确——"输入空名称应该调用 view.show_error()"

> **要点提示**：Presenter 只依赖 View 接口而非具体 View 类——这是 MVP 的测试优势根源。单元测试中用 MockView 替代真实 View，验证 Presenter 是否在正确时机调用了正确的 View 方法，不需要启动任何 UI 环境。

> **要点提示**：多 View 实现的切换不需要修改 Presenter——这是 MVP 的灵活性优势。同一个 Presenter 可以驱动 Console 视图（开发调试）、Web 视图（生产部署）、Mock 视图（单元测试），代码完全不变。

## 优缺点

**优点**
- Presenter 可独立单元测试——不依赖 UI 框架，只需 mock View 接口。原因：Presenter 只依赖 View 抽象接口和 Model，不依赖 Android Activity 或 Windows Form，测试只需创建 MockView 即可验证逻辑
- View 完全被动——UI 框架差异不影响业务逻辑。原因：View 只提供展示方法，具体 UI 框架的实现细节封装在 View 类内部，Presenter 不知道用了什么框架
- 职责清晰——Model 数据、View 展示、Presenter 逻辑，三者界限分明。原因：Model 不关心展示、View 不关心逻辑、Presenter 不关心 UI 细节，每个组件只负责一件事
- 适合 Android/WinForms 等 UI 框架——这些框架的 View 天然被动。原因：这些框架没有数据绑定机制，UI 更新必须手动驱动，MVP 的 Presenter 驱动模式与这些框架的设计哲学一致

**缺点**
- Presenter 容易膨胀——所有逻辑集中一处，可能变成"God Presenter"。原因：验证、业务规则、数据获取、展示更新全部在 Presenter 中，复杂页面的 Presenter 可能有数百行代码
- View 接口过细——每个展示动作都要定义接口方法，接口数量膨胀。原因：页面上每个显示点（用户名、邮箱、错误提示、加载状态、按钮启用/禁用）都需要对应的 View 接口方法，复杂页面可能有 20-30 个接口方法
- 手动同步麻烦——Presenter 需手动从 Model 取数据再推给 View，不像 MVC 自动通知。原因：Presenter 的每次状态更新都需要两步操作（写 Model + 推 View），容易遗漏或顺序错误

### 适用场景

- Android 原生开发——Activity/Fragment 作为 View，Presenter 处理所有逻辑
- WinForms/WPF(无数据绑定)——Form 作为被动 View，Presenter 驱动展示
- 需要多 UI 实现的应用——Console/Web/Mobile 不同 View 共享同一 Presenter
- 高测试覆盖率要求的 UI 项目——Presenter 可独立测试

### 不适用场景

- 支持数据绑定的框架——Angular/Vue/WPF(有绑定)更适合 MVVM
- 极简 UI——只有一个展示点，三层分离过于复杂
- 快速原型阶段——UI 变化频繁，Presenter 接口定义跟不上变化
- 纯展示页面——没有交互逻辑，Presenter 只起转发作用

## 真实项目中的应用

- **Android (Java/Kotlin)** — MVP 是 Android UI 的主流架构，Activity/Fragment 作为 View。典型的 Android MVP 做法：Activity 实现 View 接口（只包含 `showUser()`、`showError()` 等方法），Presenter 处理所有逻辑（网络请求、数据解析、验证），Activity 在生命周期回调中调用 Presenter 方法。Android 社区推广 MVP 的核心原因是 Android 的 Activity 生命周期复杂且难以测试——MVP 将逻辑移到可测试的 Presenter 中
- **WinForms (.NET)** — Form 作为被动 View，事件处理器在 Presenter 中。WinForms 没有数据绑定机制（或绑定功能有限），MVP 手动驱动 UI 更新比 MVVM 更自然
- **GWT (Google Web Toolkit)** — MVP 是 GWT 官方推荐的架构模式。GWT 团队于 2010 年发布 "GWT MVP Architecture" 最佳实践文档，推荐将 UI 逻辑从 View 移到 Presenter，提高测试覆盖率和代码可维护性
- **Django Admin 的表单处理** — Django Admin 的表单验证和展示逻辑采用类似 MVP 的分离：Model 是数据库模型，View（Template）是被动展示，Form（类似 Presenter）包含验证和数据处理逻辑。虽然不是严格 MVP，但分离思想一致

## 进一步阅读

- Martin Fowler — [UI Architectures: MVP](https://martinfowler.com/eaaDev/uiArchs.html)（系统梳理 MVP 的 Passive View 和 Supervising Controller 两种变体，2006）
- 《Clean Architecture》 (Robert C. Martin) — MVP 与整洁架构的关系，Presenter 作为 Use Case Interactor 的角色
- Taligent 1996 — MVP 模式的原始定义文档，Dolphin 小组首次提出（可搜索 "Taligent MVP" 找到相关历史资料）
- 《Android 开发艺术探索》 — Android MVP 架构的实战落地，包含 Presenter 生命周期管理、View 接口设计、Fragment 与 Presenter 的协作
