"""迭代器模式 (Iterator Pattern) 最小化示例

演示顺序访问集合元素而不暴露内部结构：
- 自定义迭代器实现 __iter__ 和 __next__
- 客户端用 for 循环遍历，无需关心内部存储方式
- 同一集合可有多种遍历策略
"""


class BookIterator:
    """迭代器：封装对 BookCollection 的顺序遍历"""

    def __init__(self, books_dict):
        self._keys = list(books_dict.keys())
        self._values = list(books_dict.values())
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._keys):
            print("  [Iterator] 遍历结束")
            raise StopIteration
        key = self._keys[self._index]
        value = self._values[self._index]
        self._index += 1
        print(f"  [Iterator] 位置 {self._index}: {key} → {value}")
        return value


class BookCollection:
    """集合：内部用 dict 存储，但对外提供统一迭代接口"""

    def __init__(self):
        self._books = {}  # 内部存储是 dict，客户端无需知道

    def add_book(self, title, author):
        self._books[title] = author
        print(f"[Collection] 添加: 《{title}》 by {author}")

    def __iter__(self):
        """返回自定义迭代器"""
        print("[Collection] 创建 BookIterator")
        return BookIterator(self._books)


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("迭代器模式演示：遍历集合无需知道内部结构")
    print("=" * 40 + "\n")

    collection = BookCollection()
    collection.add_book("三体", "刘慈欣")
    collection.add_book("活着", "余华")
    collection.add_book("百年孤独", "马尔克斯")
    print()

    # 客户端只用 for，不知道内部是 dict 还是 list
    print("--- for 循环遍历 ---")
    for author in collection:
        pass  # 迭代器内部已打印详情

    print("\n--- 第二次遍历（新迭代器） ---")
    for author in collection:
        pass
