# MVC 架构 (Model-View-Controller)

## 什么是 MVC

MVC 将应用分为三部分：Model（数据和业务逻辑）、View（展示）、Controller（输入处理和协调）。Controller 是桥梁——接收用户输入，操作 Model，Model 变化后更新 View。

## 核心思想

**关注点分离 + 单一数据源**：Model 是唯一的数据权威，View 只是 Model 的投影，Controller 是输入的入口。

```
    Controller
     ↓   ↑
  输入  操作
     ↓   ↑
   Model ←——→ View
   (数据)    (展示)
```

关键特征：
- **Model 不知道 View** — 数据层只管数据和业务规则，不关心展示方式
- **View 不知道 Controller** — 展示层只接收数据并渲染，不关心数据从哪来
- **Controller 知道两者** — 协调层接收输入、操作 Model、间接触发 View 更新

## 代码示例

运行基础示例：

```bash
python example.py
```

关键代码解读：

1. **TemperatureModel** — 持有温度数据，变化时主动通知所有绑定的 View（Observer 模式）
2. **TextView / ChartView** — 两种不同的展示方式，都只负责渲染数据，不知道 Controller
3. **TemperatureController** — 接收输入后操作 Model，不直接操作 View；View 更新由 Model 间接触发
4. **increase()** — Controller 从 Model 读取当前值 +1 后写回，展示 Controller 作为"协调者"的角色

Controller 不直接调用 View——这是 MVC 与简单三层调用的关键区别。

## 进阶示例

运行进阶示例：

```bash
python advanced.py
```

进阶示例展示 MVC 的核心优势：**一个 Model，多个 View 自动同步**。

- `UserModel` 变化时，`ProfileView` 和 `ListView` 同时收到更新
- 新增 View 只需调用 `model.attach(new_view)`，不需要修改 Model 或 Controller
- 每个 View 各自决定如何展示同一数据——这是关注点分离的直接体现

## 优缺点

**优点**
- Model 和 View 解耦——改展示不改数据逻辑
- 一个 Model 可有多个 View——同一数据不同呈现
- 新增 View 不改 Model——扩展性强
- 适合 UI 应用——天然匹配"输入→处理→展示"流程

**缺点**
- Controller 可能膨胀成"God Controller"——所有逻辑都堆在协调层
- Model-View 直接观察耦合（不是纯 MVC）——Model 通知 View 违背了"Model 不知道 View"的理想
- 三角通信容易混乱——Controller 操作 Model，Model 通知 View，View 又可能触发 Controller

## 真实项目中的应用

- **Rails (Ruby)** — 经典 Web MVC：路由→Controller→Model→View(模板)
- **Django (Python)** — MTV 变体：Model-Template-View，Template 对应 MVC 的 View，View 对应 MVC 的 Controller
- **Spring MVC (Java)** — DispatcherServlet 前端控制器 + HandlerMapping + Controller + ViewResolver
- **ASP.NET MVC** — Controller→Model→Razor View

几乎所有 Web 框架的默认架构都是 MVC 的变体。

## 进一步阅读

- Martin Fowler — [GUI Architectures](https://martinfowler.com/eaaDev/uiArchs.html)
- Trygve Reenskaug — MVC 原始发明者的论文，1979 年提出 MVC 的初衷
- 《Head First 设计模式》 — MVC 章节，结合 Observer 模式理解
