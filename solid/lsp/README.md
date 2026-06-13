# 里氏替换原则 (Liskov Substitution Principle)

## 什么是里氏替换原则

里氏替换原则（LSP）要求子类对象必须能够替换其父类对象，且程序行为不变。如果用子类替换父类后程序行为异常，说明继承关系设计有问题。

## 核心思想

**子类必须能替换父类**：Square 继承 Rectangle 后，在 `use_rectangle()` 函数中替换 Rectangle，行为却从正常变为异常——这违反了 LSP。

```
┌────────────────────┐
│   Rectangle        │ ← width/height 独立设置
│  w=4, h=5 → area=20│    行为符合预期
└────────────────────┘

        vs

┌────────────────────┐
│   Square           │ ← 继承 Rectangle 但强制边相等
│  w=4, h=5 → area=25│    设h时w也被改了！
│  行为不一致 → 违反LSP│
└────────────────────┘
```

关键机制：
- **契约一致** — 子类必须遵守父类的方法契约（前置条件不能更强，后置条件不能更弱）
- **行为等价** — 在任何使用父类的场景，子类替换后行为应一致
- **继承即约束** — 继承不仅是代码复用，更是行为契约的承诺

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Rectangle** — `width` 和 `height` setter 各自独立，设 width 不影响 height
2. **Square** — 继承 Rectangle，但 `width.setter` 同时修改 `_height`，`height.setter` 同时修改 `_width`
3. **use_rectangle()** — 期望设 width=4、height=5 后面积=20；用 Square 替换后面积=25
4. **行为差异** — Square 的 setter 修改了另一个属性，违反了 Rectangle 的隐含契约

## 优缺点

**优点**
- 继承安全——子类可放心替换父类，无需担心行为异常
- 多态可靠——基于继承的多态才有意义
- 代码复用——符合 LSP 的继承才真正实现代码复用

**缺点**
- 设计约束——限制了子类的行为自由度
- 继承判断难——有时难以判断子类是否满足替换条件
- 替代方案——组合优于继承，Square 不应继承 Rectangle

## 真实项目中的应用

- **Java Collections** — ArrayList 和 LinkedList 都能替换 List 接口，行为一致
- **Python io** — StringIO 和 BytesIO 替换文件对象时行为一致
- **测试框架** — Mock 对象必须能替换真实对象而不改变测试行为
- **图形库** — 不用继承强行建模 Square-Rectangle，而是各自独立实现

## 进一步阅读

- 《架构整洁之道》 (Robert C. Martin) — LSP 的契约视角深入讨论
- 《Effective Java》 (Joshua Bloch) — 继承与组合的选择原则
- 《程序设计语言的基础概念》 (Barbara Liskov) — LSP 的原始定义论文
