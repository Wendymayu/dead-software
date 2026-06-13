# 迭代器模式 (Iterator Pattern)

## 什么是迭代器模式

迭代器模式提供一种顺序访问集合元素的方法，而不暴露集合的内部结构。就像翻书——你一页一页地翻，不需要知道书是用胶装还是线装绑定的，每次翻页看到的都是下一页的内容。

## 核心思想

**顺序遍历，隐藏内部存储**：迭代器实现 __iter__ 和 __next__，封装对集合的遍历逻辑。客户端只需用 for 循环，不需要知道集合内部用的是 list、dict 还是树。

```
Client ──→ for book in collection:
                │
          BookCollection.__iter__()
                │
          BookIterator ──→ __next__() ──→ 返回下一个元素
                           │
                     内部存储(_books dict) ← 客户端不可见
```

关键机制：
- **__iter__** — 返回迭代器对象自身
- **__next__** — 返回下一个元素，遍历结束抛出 StopIteration
- **分离遍历与存储** — 集合负责存储，迭代器负责遍历逻辑

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **BookCollection** — 内部用 dict 存储（key=书名, value=作者），但客户端不需要知道这个细节
2. **__iter__** — 每次调用都创建一个新的 BookIterator，保证多次遍历独立
3. **BookIterator** — 将 dict 的 keys/values 转为 list 后顺序遍历，__next__ 逐个返回并打印位置信息
4. **for 循环** — `for author in collection` 完全不知道内部是 dict，只通过迭代器接口获取元素

注意 BookCollection.__iter__() 每次创建新的 BookIterator 对象——这是关键设计。如果迭代器复用，第二次遍历会从上次结束的位置继续而非从头开始。Python 的 for 循环在开始时调用 __iter__() 获取新迭代器，确保每次遍历独立。

## 优缺点

**优点**
- 隐藏内部结构——客户端无需知道集合用的是 list/dict/tree
- 统一遍历接口——所有集合都用 for 循环遍历
- 多种遍历策略——同一集合可以有前序/后序/过滤等不同迭代器
- 延迟计算——迭代器可以逐个生成元素，无需一次性加载全部

**缺点**
- 增加类数量——每种遍历策略需要一个迭代器类
- 只能顺序前进——标准迭代器不支持回退或随机访问
- 遍历中修改集合——遍历过程中修改集合可能导致不一致
- 性能开销——相比直接索引访问，迭代器多了一层间接调用

## 真实项目中的应用

- **Python 内置** — `for x in list/dict/set/range` 都是迭代器模式的实现
- **Java Collections** — Iterator 接口是 Java 集合框架的核心遍历机制
- **数据库游标** — SQL 查询结果通过游标(Cursor)逐行读取，避免一次性加载
- **生成器函数** — Python 的 `yield` 语法是迭代器模式的语法糖，简化迭代器编写

## 进一步阅读

- 《设计模式》 (GoF) — 迭代器模式的经典定义
- 《Head First 设计模式》 — 迭代器模式与组合模式的结合讲解
- Python 官方文档 — [迭代器协议](https://docs.python.org/3/library/stdtypes.html#iterator-types) — Python 迭代器的底层机制
