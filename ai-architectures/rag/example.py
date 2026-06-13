"""RAG（检索增强生成）最小化示例

演示核心流程：知识库存储文档 → 检索器按关键词匹配 → 生成器用检索结果生成回答
对比：没有 RAG 回答泛泛而谈，有 RAG 回答有据可依"""

import re

def _tokenize(text):
    """简易分词：提取英文单词和连续中文字符（≥2字），兼容中英文"""
    return re.findall(r'[a-zA-Z]{2,}|[一-鿿]{2,}', text.lower())

class KnowledgeBase:
    """文档存储 — RAG 的知识来源"""
    def __init__(self):
        self.docs = []
    def add(self, content):
        self.docs.append(content)
    def all(self):
        return self.docs

class Retriever:
    """检索器 — 从知识库中找出与查询相关的文档"""
    def __init__(self, kb: KnowledgeBase):
        self.kb = kb
    def search(self, query, top_k=2):
        # 关键词匹配：查询词在文档中出现越多，越相关
        q_tokens = _tokenize(query)
        scored = []
        for doc in self.kb.all():
            hits = sum(1 for t in q_tokens if t in doc.lower())
            if hits > 0:
                scored.append((hits, doc))
        scored.sort(reverse=True)
        return [doc for _, doc in scored[:top_k]]

class Generator:
    """生成器 — 模拟 LLM，基于检索到的上下文生成回答"""
    def generate_without_rag(self, query):
        return f"[无RAG] 关于{query}，这是一个常见话题，建议查阅相关资料了解更多。"
    def generate_with_rag(self, query, contexts):
        # 把检索到的文档拼接成上下文，让"LLM"基于事实回答
        ref = "；".join(contexts)
        return f"[有RAG] 关于{query}，根据资料：{ref}"

# --- 运行演示 ---
if __name__ == "__main__":
    kb = KnowledgeBase()
    kb.add("Python由Guido van Rossum于1991年创建，强调代码可读性")
    kb.add("RAG是检索增强生成，先检索再生成，减少幻觉")
    kb.add("Golang由Google设计，2009年发布，擅长并发编程")
    kb.add("Python的GIL限制多线程并发，但异步IO不受影响")

    retriever = Retriever(kb)
    generator = Generator()
    query = "Python是谁创建的"

    print("=" * 50)
    print("RAG 演示：检索增强生成 vs 无检索生成")
    print("=" * 50 + "\n")
    print(f"查询: {query}\n")
    print("【无 RAG】— LLM 只凭训练数据回答（泛泛而谈）")
    print(generator.generate_without_rag(query) + "\n")

    contexts = retriever.search(query)
    print(f"【检索结果】: {contexts}\n")
    print("【有 RAG】— LLM 基于检索到的文档回答（有据可依）")
    print(generator.generate_with_rag(query, contexts))
