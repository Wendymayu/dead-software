# 工厂模式 (Factory Pattern)

## 什么是工厂模式

工厂模式将对象的创建逻辑集中到工厂类中，调用者不需要知道具体创建了哪个类，只需要通过工厂获取一个符合接口的对象。就像你去餐厅点菜——你不需要知道厨房怎么做的，只需要说"我要一份宫保鸡丁"。

## 核心思想

**创建与使用分离**：调用者只关心"我能用这个对象做什么"（接口），不关心"这个对象是怎么创建的"（具体类）。

```
调用者 ──→ Factory.create("email") ──→ EmailNotification
                                           │
                                           ↓
调用者 ←── Notification.send(msg) ←───────┘
          （只知道是 Notification，不知道具体类）
```

关键机制：
- **抽象接口** — 所有产品实现同一接口
- **工厂映射** — `_types` dict 将类型名映射到具体类
- **类型参数** — 调用者传入字符串标识，工厂决定创建哪个类

## 代码示例

运行示例：

```bash
python example.py
```

关键代码解读：

1. **Notification (ABC)** — 抽象接口，所有通知类型必须实现 `send()` 方法
2. **EmailNotification / SMSNotification / PushNotification** — 三个具体产品
3. **NotificationFactory** — 工厂类，`_types` dict 维护类型→类的映射，`create()` 根据参数创建对象
4. **调用者** — 只与 Notification 接口交互，不知道具体类名

注意调用者代码：`notification = factory.create("email"); notification.send(msg)`——全程没有出现 `EmailNotification` 类名。调用者只知道类型字符串和 `send()` 方法，创建细节全由工厂处理。

## 优缺点

**优点**
- 创建逻辑集中——所有对象创建在一处管理
- 调用者解耦——不需要知道具体类名和构造细节
- 易于扩展——新增产品类型只需在 `_types` 加一行
- 统一错误处理——工厂可以对无效参数统一抛异常

**缺点**
- 产品类必须相近——工厂通常创建同一家族的产品
- 新增产品需改工厂——`_types` dict 需要更新（违反开闭原则，但影响有限）
- 工厂可能膨胀——产品太多时工厂类会变得臃肿

**变体**：抽象工厂模式用多个工厂类分别创建不同产品家族，完全满足开闭原则。

## 真实项目中的应用

- **Django ORM** — `models.Model` 的 Manager 是工厂，创建 QuerySet 对象
- **logging 模块** — `logging.getLogger()` 是工厂方法，创建 Logger 对象
- **Spring Bean Factory** — IoC 容器本质就是工厂模式的大规模应用
- **数据库连接** — `create_engine("postgresql://...")` 根据URL创建不同数据库连接

## 进一步阅读

- 《设计模式》 (GoF) — 简单工厂 vs 工厂方法 vs 抽象工厂的区分
- 《Head First 设计模式》 — 工厂模式的pizza店例子
- 《Effective Java》 (Joshua Bloch) — "用静态工厂方法替代构造器"
