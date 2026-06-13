# MVP 架构 (Model-View-Presenter)

## 什么是 MVP

MVP 将应用分为三部分：Model（数据和状态）、View（被动展示）、Presenter（全部逻辑）。View 完全被动，不观察 Model，所有交互由 Presenter 协调。这是 MVP 与 MVC 的核心区别——MVC 中 View 直接观察 Model，MVP 中 View 只是被 Presenter 驱动的"哑"接口。

## 核心思想

**View 完全被动 + Presenter 全权控制**：Presenter 是唯一的逻辑中心，View 只提供展示接口，Model 只提供数据。

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

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **UserModel** — 只持有数据，没有通知机制（与 MVC 的 Model 不同）
2. **UserView** — 完全被动：只有 show_user/show_error/show_success，自己不会主动做任何事
3. **UserPresenter** — 接收输入、验证逻辑、更新 Model、驱动 View——全部逻辑集中在此
4. **update_user** — Presenter 先验证，再更新 Model，再从 Model 取数据推给 View，View 不主动获取

View 不观察 Model，Presenter 是唯一桥梁——这是 MVP 与 MVC 的本质区别。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示 MVP 的核心优势：**View 接口抽象 + 多 View 切换**。

- `UserViewInterface` 是抽象接口，Presenter 只依赖它
- `ConsoleView` 和 `TableView` 是两种实现，切换时 Presenter 代码不变
- Presenter 可脱离真实 View 进行单元测试——只需 mock ViewInterface

## 优缺点

**优点**
- Presenter 可独立单元测试——不依赖 UI 框架，只需 mock View 接口
- View 完全被动——UI 框架差异不影响业务逻辑
- 职责清晰——Model 数据、View 展示、Presenter 逻辑，三者界限分明
- 适合 Android/WinForms 等 UI 框架——这些框架的 View 天然被动

**缺点**
- Presenter 容易膨胀——所有逻辑集中一处，可能变成"God Presenter"
- View 接口过细——每个展示动作都要定义接口方法，接口数量膨胀
- 手动同步麻烦——Presenter 需手动从 Model 取数据再推给 View，不像 MVC 自动通知

## 玜实项目中的应用

- **Android (Java/Kotlin)** — MVP 是 Android UI 的主流架构，Activity/Fragment 作为 View
- **WinForms (.NET)** — Form 作为被动 View，事件处理器在 Presenter 中
- **GWT (Google Web Toolkit)** — MVP 是 GWT 官方推荐的架构模式

## 进一步阅读

- Martin Fowler — [UI Architectures: MVP](https://martinfowler.com/eaaDev/uiArchs.html)
- 《Clean Architecture》 (Robert C. Martin) — MVP 与整洁架构的关系
- Taligent 1996 — MVP 模式的原始定义文档，Dolphin 小组首次提出
