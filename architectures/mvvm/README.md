# MVVM 架构 (Model-View-ViewModel)

## 什么是 MVVM

MVVM 在 Model 和 View 之间加入 ViewModel 作为桥梁。ViewModel 将 Model 数据转换为 View 可直接使用的格式，并通过数据绑定让 View 自动更新。核心区别：View 只和 ViewModel 交互，不接触 Model。

## 核心思想

**数据绑定 + 转换隔离**：ViewModel 是唯一的中间人——它把 Model 的"原始数据"翻译成 View 的"展示数据"，并且双向传递变化。

```
Model ←──→ ViewModel ←──→ View
(数据)      (转换/绑定)    (展示)
         ↑ 双向 ↑
```

关键特征：
- **Model 不知道 View** — 数据层只管原始数据和业务规则
- **View 不知道 Model** — 展示层只观察 ViewModel，不关心数据来源
- **ViewModel 知道两者** — 转换层既读 Model 数据又为 View 提供展示格式，双向传递变化

对比 MVC: MVC 中 Controller 处理输入后操作 Model，Model 变化后通知 View。MVVM 中 ViewModel 同时承担"数据转换"和"绑定"两个职责，View 不需要主动拉取数据。

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **UserModel** — 持有原始数据（name="alice", age=30），不知道任何展示逻辑
2. **UserViewModel** — 将 "alice" 转为 "Alice"，将 30 转为 "30岁"——View 只需调用 `display_name()`，不需要自己做格式化
3. **UserView** — 只接收 ViewModel 的 `update()` 回调并打印展示数据，完全不接触 Model
4. **`_notify()`** — 数据变化后 ViewModel 主动通知所有绑定的 View，模拟数据绑定机制

ViewModel 的转换是 MVVM 与 MVC 的关键区别：View 不再需要"理解"Model 的原始数据。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示 MVVM 的核心优势：**双向数据绑定**——View 的输入通过 ViewModel 回写到 Model。

- `input_celsius(100)` → ViewModel 写入 Model → View 自动显示 100C / 212.0F
- `input_fahrenheit(68)` → ViewModel 将 68F 转换为 20C 写入 Model → View 显示 20C / 68.0F
- View 不需要知道摄氏和华氏的转换公式——所有转换逻辑都在 ViewModel 中
- 无论从哪个方向输入，View 都能正确展示两种单位——双向绑定保证了数据一致性

双向绑定是 MVVM 与 MVC 的根本区别：MVC 只有单向流动（Controller→Model→View），MVVM 允许 View→ViewModel→Model 的反向流动。

## 优缺点

**优点**
- View 和 Model 完全解耦——改展示不改数据逻辑
- 数据绑定减少手动更新代码——ViewModel 变化自动反映到 View
- ViewModel 可独立测试——不依赖 UI 组件，纯逻辑验证
- 适合数据驱动 UI——Vue/React/SwiftUI 的核心思想

**缺点**
- ViewModel 可能膨胀——承担转换+绑定双重职责，容易变成"God ViewModel"
- 数据绑定调试困难——不知道变化从哪触发，隐式调用链难追踪
- 简单场景过度设计——只有一两个字段时，ViewModel 的转换层显得多余
- 双向绑定可能循环触发——A 变化触发 B，B 变化又触发 A

## 真实项目中的应用

- **Vue.js** — 最典型的 MVVM：响应式数据绑定 + ViewModel (组件实例)
- **React Hooks** — MVVM 变体：useState 是 ViewModel，组件是 View，自定义 Hook 是转换逻辑
- **Angular** — 双向绑定 (`[(ngModel)]`)，最直接的 MVVM 实现
- **SwiftUI** — 声明式绑定：@Observable 是 ViewModel，View 自动响应变化
- **WPF** — 微软最早的 MVVM 实践，XAML 绑定 + ViewModel 分离

## 进一步阅读

- Martin Fowler — [GUI Architectures](https://martinfowler.com/eaaDev/uiArchs.html) (MVVM vs MVP vs MVC)
- Vue.js 文档 — 响应式系统，理解数据绑定的实现原理
- Microsoft — [MVVM pattern documentation](https://learn.microsoft.com/en-us/dotnet/architecture/maui/mvvm)
