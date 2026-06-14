# Eclipse RCP：微内核架构的经典实现

## 软件简介

Eclipse 最初是 IBM 于 2001 年发布的 Java IDE，但其架构远不止 IDE。Eclipse Rich Client Platform（RCP）将 IDE 的核心框架抽取出来，使其成为构建任意桌面应用的通用平台。从 IDE 到通用 RCP 的演进，正是微内核架构"最小核心 + 可扩展功能"思想的完美体现——**核心越薄，适用范围越广**。

## 该软件的架构

Eclipse RCP 的微内核架构由三层组成：

- **EclipseCore（极薄核心）**：只提供两个能力——Workbench（窗口管理，打开/关闭窗口）和 Extension Point Registry（扩展点注册表，定义插件可贡献的契约）。核心本身不包含任何 IDE 功能——甚至编辑器也是扩展。
- **Extension Point（扩展点）**：核心定义的"插槽"契约，如 `org.eclipse.ui.editors`（编辑器插槽）、`org.eclipse.ui.views`（视图插槽）。插件声明"我要向哪个扩展点贡献什么"，核心在运行时读取并集成。
- **扩展（全部功能）**：JavaEditor、PackageExplorer、DebugView——所有 IDE 功能都是扩展，通过扩展点注册。`JavaEditorExtension` 注册到 `org.eclipse.ui.editors` 扩展点，核心不需要知道 Java 编辑器的存在。

**与 VS Code 插件架构的关键区别**：微内核的核心更薄。VS Code 的核心包含渲染引擎、文件系统 API、终端等；Eclipse RCP 的核心只有窗口管理和扩展点注册。微内核 = 核心更薄，扩展更基础。

```
EclipseCore (极薄——只有窗口管理 + 扩展点注册表)
  ┌─────────────────────────────────────────┐
  │  Workbench: 打开/关闭窗口                 │
  │  Extension Registry: 定义扩展点契约        │
  │  OSGi Runtime: 模块化生命周期管理          │
  └─────────────────────────────────────────┘
         ↑ Extension Points (契约/插槽)
         │  org.eclipse.ui.editors
         │  org.eclipse.ui.views
         │  org.eclipse.ui.menus
         ↓
  Extensions (所有 IDE 功能都是扩展)
  JavaEditorExtension → 贡献到 org.eclipse.ui.editors
  DebugExtension      → 贡献到 org.eclipse.ui.views + menus
```

## 简化实现思路

本示例模拟了 Eclipse RCP 微内核的核心机制：

| 简化概念 | 对应 Eclipse RCP 机制 |
|---------|---------------------|
| `EclipseCore` 极薄核心 | Eclipse Workbench + Extension Registry |
| `define_extension_point` | Eclipse 定义 org.eclipse.ui.editors 等扩展点 |
| `JavaEditorExtension.install` | Eclipse JDT 插件通过 plugin.xml 注册 |
| `install_plugin` | Eclipse Extension Registry 扫描插件贡献 |
| `CoreEditor.open_window` + `render` | Workbench 打开窗口并根据注册表渲染 |

## 与真实实现的对照

| 简化实现 | 真实 Eclipse RCP |
|---------|-----------------|
| Python 类同进程 | 每个插件是独立 OSGi Bundle（独立类加载器） |
| `EclipseCore` 只有窗口+注册表 | 真实 Eclipse Core 还有 OSGi 运行时和 SWT |
| 代码调用 install_plugin | 真实 Eclipse 通过 plugin.xml 自动扫描发现 |
| print 渲染 | 真实 Eclipse 用 SWT/JFace 渲染复杂 UI |
| 无依赖管理 | 真实 Eclipse 有 OSGi 依赖解析和版本约束 |
| JavaEditorExtension 是 Python 类 | 真实 JDT 是庞大的 Java 插件，含编译器、调试器等 |

## 学习建议

1. **理解"IDE 到 RCP"的演进**：Eclipse 从 IDE 演进为通用 RCP 平台的关键是把 IDE 功能全部抽取为插件，只留下最薄的核心。这是微内核的核心思想——**核心越薄，适用范围越广**。
2. **对比 Eclipse 与 VS Code**：两者都用"核心 + 扩展"，但 Eclipse 的核心更薄（只有窗口和注册表），VS Code 的核心更厚（含渲染引擎、文件 API）。思考：核心厚度如何影响扩展的自由度和系统稳定性？
3. **研究 Extension Point 契约**：扩展点是插件与核心的"合同"。读 Eclipse 的 `plugin.xml` 格式，理解声明式扩展 vs 编程式扩展的区别。扩展点 ID 如 `org.eclipse.ui.editors` 是命名空间——这是契约的版本化设计。
4. **了解 OSGi**：OSGi 是 Eclipse 的模块化基础。理解 Bundle 的类加载器隔离如何避免"类路径地狱"。这对理解 Java 模块化演进至关重要。
5. **延伸阅读**：对比 IntelliJ IDEA 的插件架构（同样微内核，但用不同的插件 API 设计），看同一架构思想的不同实现方式。
