"""代理模式 (Proxy Pattern) 最小化示例

演示通过代理对象控制访问：
- CachedDocumentProxy 包装 RealDocument
- 首次访问从源加载（慢），后续返回缓存（快）
- 客户端透明使用代理，不知道有代理存在
"""


class RealDocument:
    """真实文档：从源加载，速度慢"""

    def __init__(self, title):
        self._title = title
        self._content = None

    def load(self):
        print(f"[RealDocument] 从源加载 '{self._title}' (耗时操作)")
        self._content = f"这是文档 '{self._title}' 的内容"
        return self._content


class CachedDocumentProxy:
    """代理：缓存控制，首次加载后缓存结果"""

    def __init__(self, title):
        self._real = RealDocument(title)
        self._cache = None
        self._loaded = False
        print(f"[Proxy] 创建文档代理: '{title}'")

    def load(self):
        if self._loaded:
            print(f"[Proxy] 返回缓存内容 (快速)")
            return self._cache
        print(f"[Proxy] 缓存未命中，委托真实对象加载")
        self._cache = self._real.load()
        self._loaded = True
        return self._cache


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("代理模式演示：代理控制访问，缓存加速")
    print("=" * 40 + "\n")

    doc = CachedDocumentProxy("设计模式入门")

    print("--- 首次访问 (慢) ---\n")
    content1 = doc.load()
    print(f"  内容: {content1}\n")

    print("--- 再次访问 (快) ---\n")
    content2 = doc.load()
    print(f"  内容: {content2}\n")

    print("--- 客户端透明 ---")
    print("  客户端只调用 doc.load()，不知道有代理存在")
    print("  代理在背后控制了加载和缓存策略")
