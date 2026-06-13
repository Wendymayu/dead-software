"""过早优化 反模式 最小化示例

演示在不知瓶颈时盲目优化：
- 开发者对很少使用的功能加缓存和复杂索引
- 结果浪费开发时间，增加代码复杂度
"""

import time


# --- 反模式 ---
class PrematureOptimizer:
    """对每月只用1次的报表功能过度优化"""
    def __init__(self):
        self._cache = {}
        self._index = {}

    def _build_index(self, data):
        """构建复杂索引——数据量小时毫无必要"""
        print("[过早优化] 构建索引...")
        for i, item in enumerate(data):
            self._index[item] = i

    def _check_cache(self, key):
        """检查缓存——数据从不重复，缓存无用"""
        if key in self._cache:
            print("[过早优化] 缓存命中(但数据从不重复)")
            return self._cache[key]
        return None

    def report(self, data):
        self._build_index(data)
        cached = self._check_cache("report")
        if cached:
            return cached
        print("[过早优化] 生成报表...")
        result = f"报表: 共{len(data)}条数据"
        self._cache["report"] = result
        return result


# --- 正确做法 ---
class SimpleReporter:
    """先写简单版本，需要时再优化"""
    def report(self, data):
        print("[简洁] 生成报表...")
        return f"报表: 共{len(data)}条数据"


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("过早优化 反模式演示")
    print("=" * 40 + "\n")

    data = ["a", "b", "c"]

    print("--- 反模式: 过早优化 ---")
    t1 = time.perf_counter()
    PrematureOptimizer().report(data)
    t1 = time.perf_counter() - t1
    print(f"  耗时: {t1:.4f}s，代码复杂度高")
    print()

    print("--- 正确做法: 先简洁后优化 ---")
    t2 = time.perf_counter()
    SimpleReporter().report(data)
    t2 = time.perf_counter() - t2
    print(f"  耗时: {t2:.4f}s，代码简洁明了")

    print("\n关键：先让它正确运行，再找瓶颈优化")
    print("\"过早优化是万恶之源\" — Donald Knuth")
