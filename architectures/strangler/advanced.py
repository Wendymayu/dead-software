"""绞杀者模式进阶示例：完整迁移生命周期

展示三个阶段和数据同步：
- 开始阶段：100%旧系统
- 中间阶段：新旧并存，数据双向同步
- 最终阶段：100%新系统，旧系统移除
"""


# --- 旧系统 ---
class LegacySystem:
    """遗留系统：包含所有业务数据"""
    def __init__(self):
        self._data = {
            "user": {"u1": {"name": "Alice"}},
            "order": {"o1": {"item": "Book"}},
        }

    def query(self, entity, id):
        print(f"  [旧系统] 查询 {entity}/{id}")
        return self._data.get(entity, {}).get(id)

    def update(self, entity, id, value):
        print(f"  [旧系统] 更新 {entity}/{id}")
        self._data[entity][id] = value


# --- 新系统 ---
class NewSystem:
    """新系统：逐步接收迁移的功能"""
    def __init__(self):
        self._data = {}  # 从空开始，通过同步填充

    def query(self, entity, id):
        print(f"  [新系统] 查询 {entity}/{id}")
        return self._data.get(entity, {}).get(id)

    def update(self, entity, id, value):
        print(f"  [新系统] 更新 {entity}/{id}")
        self._data.setdefault(entity, {})[id] = value


# --- 数据同步器 ---
class DataSynchronizer:
    """新旧系统间的数据同步：迁移前将旧数据复制到新系统"""
    def sync_to_new(self, legacy, new, entity):
        print(f"[同步] {entity} 数据从旧系统 → 新系统")
        for id, value in legacy._data.get(entity, {}).items():
            new._data.setdefault(entity, {})[id] = value


# --- 绞杀者路由层 ---
class StranglerRouter:
    """路由层：管理请求分发，迁移时自动触发数据同步"""
    def __init__(self, legacy, new):
        self._legacy = legacy
        self._new = new
        self._routes = {}  # entity -> "new"
        self._sync = DataSynchronizer()

    def migrate(self, entity):
        """迁移某个实体到新系统：路由切换 + 数据同步"""
        print(f"[路由] {entity} → 新系统")
        self._routes[entity] = "new"
        self._sync.sync_to_new(self._legacy, self._new, entity)

    def query(self, entity, id):
        target = self._routes.get(entity, "legacy")
        system = self._new if target == "new" else self._legacy
        return system.query(entity, id)

    def update(self, entity, id, value):
        # 迁移后写入新系统，未迁移仍写旧系统
        system = self._new if entity in self._routes else self._legacy
        system.update(entity, id, value)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 50)
    print("绞杀者模式进阶：完整迁移生命周期")
    print("=" * 50 + "\n")

    legacy = LegacySystem()
    new = NewSystem()
    router = StranglerRouter(legacy, new)

    # 阶段1：100%旧系统
    print("--- 阶段1: 100%旧系统 ---")
    router.query("user", "u1")
    router.query("order", "o1")
    print()

    # 阶段2：迁移user（路由切换+数据同步）
    print("--- 阶段2: 迁移user（数据同步+并存）---")
    router.migrate("user")
    router.query("user", "u1")   # → 新系统
    router.query("order", "o1")  # → 仍旧系统
    router.update("user", "u1", {"name": "Alice_V2"})
    print()

    # 阶段3：全部迁移，旧系统可移除
    print("--- 阶段3: 全部迁移 → 移除旧系统 ---")
    router.migrate("order")
    router.query("user", "u1")
    router.query("order", "o1")
    print("\n[完成] 旧系统已被绞杀，可安全移除")
