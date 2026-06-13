"""RAG 进阶示例：向量检索、分块策略、重排序

展示 RAG 系统的三个进阶技术：
- 向量检索：用简单词频模拟 embedding 相似度，比关键词匹配更灵活
- 分块策略：长文档拆成小块，检索粒度更精细
- 重排序：多路检索后按相关性排序，取最优结果"""

import re


def _tokenize(text):
    """简易分词：提取英文单词和连续中文字符（≥2字），兼容中英文混合"""
    return re.findall(r'[a-zA-Z]{2,}|[一-鿿]{2,}', text.lower())


# --- 分块策略 ---
def chunk_document(text, chunk_size=20):
    """将长文档按固定词数拆成小块 — 检索粒度更细，匹配更精准"""
    tokens = _tokenize(text)
    chunks = []
    for i in range(0, len(tokens), chunk_size):
        chunk = " ".join(tokens[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    # 原始文本也保留一个完整块，防止单词拆散丢失语义
    if text not in chunks:
        chunks.append(text)
    return chunks


# --- 向量检索（词频模拟 embedding 相似度） ---
def compute_similarity(query, doc):
    """模拟 embedding 相似度 — 用词频重叠率代替向量余弦相似度"""
    q_tokens = set(_tokenize(query))
    d_tokens = set(_tokenize(doc))
    if not q_tokens:
        return 0.0
    overlap = q_tokens & d_tokens
    return len(overlap) / len(q_tokens)


class VectorRetriever:
    """向量检索器 — 用相似度评分代替关键词匹配，检索更灵活"""
    def __init__(self, chunks):
        self.chunks = chunks  # 已分块的文档库

    def search(self, query, top_k=5):
        scored = [(compute_similarity(query, c), c) for c in self.chunks]
        scored.sort(reverse=True)
        results = [(s, c) for s, c in scored if s > 0]
        return results[:top_k]


# --- 重排序 ---
def rerank(results, query):
    """对检索结果重排序 — 考虑信息密度，短而精准的块额外加权"""
    q_tokens = set(_tokenize(query))
    reranked = []
    for score, chunk in results:
        c_tokens = set(_tokenize(chunk))
        # 信息密度加分：块中查询词占比越高，越精准
        density = len(q_tokens & c_tokens) / max(len(c_tokens), 1) * 0.3
        reranked.append((score + density, chunk))
    reranked.sort(reverse=True)
    return reranked


# --- 运行演示 ---
if __name__ == "__main__":
    docs = [
        "Python由Guido van Rossum于1991年创建，强调代码可读性与简洁性。"
        "Python支持多种编程范式，包括面向对象、函数式和过程式编程。"
        "Python的标准库非常丰富，涵盖网络、文件处理、数据结构等。",
        "RAG是检索增强生成技术，先从知识库检索相关文档，再将检索结果"
        "作为上下文提供给LLM，让生成有据可依，这种方法显著减少幻觉。"
        "RAG系统通常包含索引、检索和生成三个核心组件。",
        "Golang由Google的Robert Griesemer等设计，2009年发布。"
        "Golang天生支持并发，goroutine和channel是核心特性。"
        "Golang编译速度快、运行效率高，适合构建微服务和网络工具。",
    ]

    print("=" * 50)
    print("RAG 进阶：分块 → 向量检索 → 重排序")
    print("=" * 50 + "\n")

    # 1. 分块
    print("【步骤1: 分块】长文档拆成小块")
    all_chunks = []
    for doc in docs:
        chunks = chunk_document(doc, chunk_size=20)
        all_chunks.extend(chunks)
        print(f"  文档({len(_tokenize(doc))}词) → {len(chunks)}个块")
    print(f"  总计: {len(all_chunks)}个块\n")

    # 2. 向量检索
    query = "Python创建者"
    retriever = VectorRetriever(all_chunks)
    results = retriever.search(query, top_k=5)
    print(f"【步骤2: 向量检索】查询='{query}'")
    for i, (score, chunk) in enumerate(results, 1):
        print(f"  #{i} 相似度={score:.2f} → {chunk[:50]}...")
    print()

    # 3. 重排序
    reranked = rerank(results, query)
    print("【步骤3: 重排序】考虑信息密度后重新排序")
    for i, (score, chunk) in enumerate(reranked, 1):
        print(f"  #{i} 最终分={score:.2f} → {chunk[:50]}...")
    print()

    print("--- 与基础示例对比 ---")
    print("基础示例: 关键词匹配检索，整篇文档为单位")
    print("进阶示例: 分块提升粒度，向量检索更灵活，重排序优化结果")
