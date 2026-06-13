# 组合模式 (Composite Pattern)

## 什么是组合模式

组合模式将对象组织成树形结构，使客户端可以统一对待单个对象（叶子）和组合对象（树枝）。就像文件系统——计算文件夹大小时，你不需要区分它是文件还是子文件夹，统一调用 get_size() 即可。

## 核心思想

**统一接口，递归组合**：叶子与组合实现同一接口，组合对象递归管理子对象并汇总结果。客户端无需判断"这是叶子还是组合"，统一调用即可。

```
FileSystemNode (接口)
  ├── File (叶子)  ── get_size() → 返回自身大小
  └── Folder (组合) ── get_size() → 递归求和子对象
           ├── File
           ├── Folder
           │     └── File ...
           └── File
```

关键机制：
- **统一接口** — File 和 Folder 都实现 get_size()
- **递归汇总** — Folder.get_size() 遍历所有子对象递归求和
- **透明性** — 客户端对 File 和 Folder 一视同仁，无需类型判断

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **FileSystemNode** — 统一接口，定义 get_size() 方法
2. **File** — 叶子节点，直接返回自身大小 `_size`
3. **Folder** — 组合节点，通过 `add()` 管理子对象，`get_size()` 递归调用所有子对象的 `get_size()` 并求和
4. **树形构建** — project 包含 readme、src_folder、test_folder，src_folder 又包含两个 File——典型的树结构

注意 Folder.get_size() 中的 `sum(child.get_size() for child in self._children)`：它不知道 child 是 File 还是 Folder，只是统一调用。如果 child 是 Folder，它会自动递归——这就是组合模式的威力。

## 优缺点

**优点**
- 统一接口——客户端无需区分叶子与组合，代码简洁
- 递归结构天然——树形数据（文件系统、组织架构、UI组件）天然适配
- 开闭原则——新增叶子或组合类型无需修改客户端代码
- 灵活组合——可以动态添加/删除子对象

**缺点**
- 类型安全弱——统一接口使得难以限制某些操作只对叶子或组合有效
- 过度泛化——某些操作只适合叶子或只适合组合，强行统一可能导致设计不够精确
- 调试困难——递归遍历深层树结构时，错误追踪较复杂

## 真实项目中的应用

- **GUI 框架** — Qt/WinForms 中控件树（Panel 包含 Button、Label），统一处理布局和事件
- **文件系统** — Unix 文件系统的目录和文件统一由 `stat()` 返回信息
- **DOM 树** — HTML 的 Element 和 TextNode 统一实现 Node 接口
- **组织架构** — 公司-部门-员工树形结构，统一计算薪资总额

## 进一步阅读

- 《设计模式》 (GoF) — 组合模式的经典定义
- 《Head First 设计模式》 — 以菜单系统为例的生动讲解
- 《DOM 标准》 — [MDN Web Docs](https://developer.mozilla.org/) — 组合模式在浏览器中的经典实现
