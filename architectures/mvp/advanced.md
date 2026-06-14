# Android MVP：从 MVC 到 MVP 的架构演进

## 软件简介

Android MVP（Model-View-Presenter）是 Android 开发社区在 2014-2018 年间广泛采用的架构模式。Android 早期使用 MVC，但 Activity 同时承担了 View 和 Controller 的职责，导致 Activity 变成"上帝对象"——数千行代码、难以测试。MVP 将 Controller 逻辑提取为独立的 Presenter，通过 View 接口解耦 Activity 与 Presenter，使 Presenter 可以在没有 Android 依赖的情况下进行单元测试。

## 该软件的架构

Android MVP 的核心是 View 接口的引入：

- **View 接口（ViewContract）**：定义 Activity 能做什么（show_loading、show_users、show_error）。Presenter 只依赖这个接口，不依赖具体 Activity。这使得 Presenter 可以在纯 JVM 环境下测试——用 MockView 替代真实 Activity。
- **Activity（View 实现）**：Activity 完全被动——它实现 View 接口，只做两件事：(1) 按 Presenter 指令更新 UI；(2) 将用户操作（按钮点击）转发给 Presenter。Activity 不做任何业务逻辑。
- **Presenter（逻辑中心）**：Presenter 持有 View 接口引用和 Model 引用。它接收 View 转发的用户操作，调用 Model 获取数据，然后通过 View 接口通知 Activity 更新 UI。Presenter 是唯一包含逻辑的地方。
- **Model（数据层）**：Repository 模式——从数据库、网络、缓存获取数据。Model 不依赖 Presenter 或 View。

```
用户操作流: 点击按钮
  │
  ├─ Activity(View): on_button_click() → presenter.on_load_users_clicked()
  │     (Activity 只转发，不做逻辑)
  │
  ├─ Presenter: on_load_users_clicked()
  │     ├─ view.show_loading()  → Activity 显示 ProgressBar
  │     ├─ model.fetch_users()  → Repository 获取数据
  │     └─ view.show_users()    → Activity 更新 RecyclerView
  │
  └─ Activity(View): 按指令更新 UI（被动）
```

## 简化实现思路

本示例模拟了 Android MVP 的核心流程：

| 简化概念 | 对应 Android MVP 机制 |
|---------|---------------------|
| `UserViewContract` 接口 | Android MVP 的 View 接口定义 |
| `MainActivity` 实现 ViewContract | Android Activity 作为被动 View |
| `UserPresenter` 持有 View 接口引用 | Presenter 不依赖具体 Activity |
| `on_button_click` 转发给 Presenter | Activity 将用户操作转发到 Presenter |
| Presenter 调用 View 接口方法 | Presenter 通过接口驱动 UI 更新 |

## 与真实实现的对照

| 简化实现 | 真实 Android MVP |
|---------|----------------|
| Python ABC 接口 | Android Java/Kotlin Interface |
| print 模拟 UI | Android RecyclerView、ProgressBar、Toast |
| Presenter 直接引用 View | 真实 MVP 需处理 Activity 生命周期（View 可能被销毁） |
| 无生命周期问题 | 真实 Android 中 Presenter 需在 onDestroy 时释放 View 引用 |
| 无 Fragment 场景 | Android MVP 也适用于 Fragment 作为 View |
| 同步调用 | 真实 Android 中 Model.fetchUsers() 是异步（RxJava/Coroutines） |

## 学习建议

1. **理解为什么 Android 需要 MVP**：Android 的 Activity 既是 View（显示 UI）又是 Controller（处理输入）——这是 MVC 在 Android 上的失败。MVP 通过引入 View 接口，把 Activity 变成纯 View，把逻辑搬到 Presenter。理解这个"从 Activity 提取逻辑"的动机。
2. **View 接口是 MVP 的灵魂**：Presenter 只依赖 View 接口，这意味着 Presenter 可以用 MockView 做纯 JUnit 测试——不需要 Android SDK、不需要模拟器。这是 MVP 最大的优势：**可测试性**。
3. **注意 MVP 的生命周期陷阱**：真实 Android 中，用户旋转屏幕时 Activity 会重建，但 Presenter 不应该重建。如果 Presenter 持有已销毁 Activity 的引用，就会崩溃。学习如何通过 Loader/ViewModel 持有 Presenter。
4. **MVP → MVVM 的演进**：MVP 的痛点是 View 接口方法太多（每个 UI 状态一个方法）、Presenter 与 View 的手动绑定繁琐。Android 后来引入 ViewModel + LiveData（MVVM），用数据绑定替代 View 接口。对比 MVP 和 MVVM 的优劣。
5. **延伸阅读**：研究 Google 官方的 Android Architecture Components（ViewModel、LiveData、Room），理解 Google 为什么选择 MVVM 而不是 MVP 作为官方推荐架构。
