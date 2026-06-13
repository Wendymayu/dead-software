# 桥接模式 (Bridge Pattern)

## 什么是桥接模式

桥接模式将抽象部分与其实现部分分离，使两者可以独立变化。就像画图——形状（圆形/方形）和渲染方式（矢量/像素）是两个维度，形状委托渲染器去画，新增形状或渲染器都不影响另一方。

## 核心思想

**抽象与实现解耦，各自独立演化**：抽象侧持有实现侧的引用（桥接点），通过委托调用实现侧的方法。新增形状只需新增 Shape 子类，新增渲染器只需新增 Renderer 子类——两个维度独立扩展。

```
Shape (抽象侧)          Renderer (实现侧)
  │ _renderer │ ←────────── 桥接点
  │           │
  Circle      │          VectorRenderer
  Square ─────┘          RasterRenderer
```

关键机制：
- **桥接引用** — Shape 持有 Renderer 引用，通过组合而非继承连接两个维度
- **委托调用** — Circle.draw() 调用 self._renderer.render_circle()
- **独立变化** — 新增形状不改 Renderer，新增渲染器不改 Shape

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Renderer (ABC)** — 实现侧接口，定义 render_circle() 和 render_square()
2. **VectorRenderer / RasterRenderer** — 两个具体渲染器，各自实现绘制逻辑
3. **Shape** — 抽象侧基类，持有 `_renderer` 引用（桥接点）
4. **Circle / Square** — 具体形状，draw() 方法委托给 `_renderer` 执行实际渲染

注意 Circle 的构造器 `Circle(vector, 5)` 和 `Circle(raster, 5)`：同一个形状可以搭配不同渲染器，同一个渲染器也可以搭配不同形状。这就是桥接模式的核心——**两个维度独立组合**，而非继承导致的类爆炸。

## 优缺点

**优点**
- 避免类爆炸——多维变化用组合替代继承，M×N 变为 M+N 个类
- 灵活组合——运行时切换实现侧（如动态更换渲染器）
- 开闭原则——新增维度只需新增子类，不影响另一侧
- 可独立测试——抽象侧和实现侧可以分别进行单元测试

**缺点**
- 增加复杂度——对单维度场景引入桥接反而过度设计
- 客户端需要理解两侧——选择正确的组合需要了解抽象和实现的差异
- 间接调用开销——委托调用多了一层间接

## 真实项目中的应用

- **Java JDBC** — Driver（实现侧）与 Connection（抽象侧）桥接，不同数据库驱动独立实现
- **Qt 渲染** — QPainter（抽象侧）与 QPaintDevice（实现侧）桥接，同一绘制代码可输出到屏幕/PDF/图片
- **Python logging** — Logger（抽象侧）与 Handler（实现侧）桥接，同一日志可输出到文件/终端/网络
- **跨平台 UI** — Flutter 的 Widget（抽象侧）与 RenderObject（实现侧）桥接

## 进一步阅读

- 《设计模式》 (GoF) — 桥接模式的经典定义
- 《Head First 设计模式》 — 桥接模式的直观讲解
- 《Clean Code》 (Robert C. Martin) — 组合优于继承的设计原则
