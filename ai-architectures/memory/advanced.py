"""Memory 进阶示例：遗忘、摘要、相关性检索

展示记忆管理的三大策略：
- 遗忘机制：短期记忆按重要性淘汰低价值条目
- 摘要压缩：将对话历史压缩为长期记忆中的摘要
- 相关性检索：从长期记忆中按关键词重叠评分检索最相关事实"""


# --- 短期记忆 + 遗忘机制 ---
class ShortTermMemory:
    """短期记忆 — 每条消息带重要性评分，超容量时淘汰最低分的"""
    def __init__(self, capacity=5):
        self.capacity = capacity
        self.items = []  # [(message, importance)]

    def add(self, msg, importance=1):
        self.items.append((msg, importance))
        if len(self.items) > self.capacity:
            # 淘汰重要性最低的条目（而非最早的）
            min_idx = min(range(len(self.items)),
                          key=lambda i: self.items[i][1])
            dropped = self.items.pop(min_idx)
            print(f"[STM-遗忘] 淘汰低重要性条目: {dropped[0][:25]}... (重要度={dropped[1]})")

    def get_all(self):
        return [(m, s) for m, s in self.items]


# --- 摘要压缩：对话 → 长期记忆 ---
class MemorySummarizer:
    """摘要器 — 将多条对话压缩为一条摘要存入长期记忆"""
    def summarize(self, messages):
        """模拟 LLM 摘要：提取关键词拼接成摘要"""
        keywords = []
        for msg, _ in messages:
            # 提取核心词（简易：取每条消息前10字符+关键标记）
            keywords.append(msg[:15])
        summary = "摘要: " + "; ".join(keywords)
        print(f"[摘要] 对话压缩: {len(messages)}条 → 1条摘要")
        return summary


# --- 长期记忆 + 相关性检索 ---
class LongTermMemory:
    """长期记忆 — 持久存储事实，支持按相关性评分检索"""
    def __init__(self):
        self.facts = {}  # key → value

    def store(self, key, value):
        self.facts[key] = value
        print(f"[LTM-存储] {key}: {value}")

    def retrieve_by_relevance(self, query, top_k=3):
        """按关键词重叠评分检索最相关的长期记忆"""
        q_words = set(query.lower().split())
        scored = []
        for key, value in self.facts.items():
            overlap = len(q_words & set(key.lower().split()))
            overlap += len(q_words & set(value.lower().split()))
            if overlap > 0:
                scored.append((overlap, key, value))
        scored.sort(reverse=True)
        results = scored[:top_k]
        if results:
            print(f"[LTM-检索] 查询'{query}' → 最相关{len(results)}条:")
            for score, key, value in results:
                print(f"  相关度={score}: {key} → {value}")
        return results


# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 50)
    print("Memory 进阶：遗忘、摘要、相关性检索")
    print("=" * 50 + "\n")

    stm = ShortTermMemory(capacity=5)
    ltm = LongTermMemory()
    summarizer = MemorySummarizer()

    # 1. 短期记忆 + 遗忘
    print("【步骤1: 短期记忆与重要性遗忘】")
    conversations = [
        ("你好", 1), ("我想学Python", 3), ("天气不错", 1),
        ("Python有GIL限制", 4), ("午饭吃什么", 1),
        ("GIL影响多线程性能", 4), ("Python简洁易学", 3),
    ]
    for msg, importance in conversations:
        stm.add(msg, importance)

    remaining = stm.get_all()
    print(f"  保留{len(remaining)}条（高重要性优先）:")
    for msg, imp in remaining:
        print(f"    {msg} (重要度={imp})")

    # 2. 摘要压缩
    print("\n【步骤2: 对话摘要压缩为长期记忆】")
    summary = summarizer.summarize(remaining)
    ltm.store("对话摘要", summary)

    # 3. 相关性检索
    print("\n【步骤3: 从长期记忆按相关性检索】")
    ltm.store("Python特性", "Python简洁易学，支持多范式编程")
    ltm.store("GIL机制", "GIL限制多线程并行，异步IO不受影响")
    ltm.store("Go语言", "Go天生支持并发，goroutine轻量高效")

    ltm.retrieve_by_relevance("Python 并发 GIL", top_k=2)
