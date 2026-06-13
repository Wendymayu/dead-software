"""P2P 进阶示例：数据复制 + 去中心化共识

展示 P2P 网络的进阶能力：
- 数据复制：节点存储数据时自动复制到邻居，提高可用性
- 去中心化共识：无中心节点时如何达成一致（简易投票）
- 网络自愈：节点离开后数据仍可通过其他节点获取
"""


class PeerNode:
    def __init__(self, name):
        self._name = name
        self._data = {}
        self._neighbors = []
        self._replica_count = 2  # 每份数据复制到几个邻居

    def connect(self, other):
        self._neighbors.append(other)
        other._neighbors.append(self)
        print(f"[P2P] {self._name} <-> {other._name} 直连")

    def store(self, key, value):
        """存储数据并自动复制到邻居"""
        self._data[key] = value
        print(f"  [{self._name}] 存储: {key}={value}")
        # 自动复制——提高数据可用性
        replicated = 0
        for neighbor in self._neighbors:
            if replicated >= self._replica_count:
                break
            neighbor._data[key] = value
            print(f"  [{self._name}] 复制到 {neighbor._name}: {key}")
            replicated += 1

    def query(self, key):
        if key in self._data:
            print(f"  [{self._name}] 本地命中: {key}")
            return self._data[key]
        for neighbor in self._neighbors:
            if key in neighbor._data:
                print(f"  [{self._name}] 从 {neighbor._name} 获取: {key}")
                return neighbor._data[key]
        print(f"  [{self._name}] 未找到: {key}")
        return None

    def leave_network(self):
        """节点离开网络"""
        print(f"[P2P] {self._name} 离开网络")
        for neighbor in self._neighbors:
            neighbor._neighbors.remove(self)
        self._neighbors.clear()


def decentralized_vote(nodes, proposal):
    """去中心化共识：各节点独立投票，多数通过"""
    print(f"\n[共识] 提议: {proposal}")
    votes = {}
    for node in nodes:
        vote = "YES" if hash(node._name + proposal) % 2 == 0 else "NO"
        votes[node._name] = vote
        print(f"  [{node._name}] 投票: {vote}")
    yes_count = sum(1 for v in votes.values() if v == "YES")
    result = "通过" if yes_count > len(nodes) // 2 else "否决"
    print(f"  → 结果: {result} ({yes_count}/{len(nodes)})")


# --- 运行演示 ---
if __name__ == "__main__":
    a, b, c, d = PeerNode("A"), PeerNode("B"), PeerNode("C"), PeerNode("D")
    a.connect(b); b.connect(c); c.connect(d); d.connect(a)

    print("=" * 50)
    print("进阶演示: 数据复制 + 去中心化共识 + 网络自愈")
    print("=" * 50 + "\n")

    # 数据自动复制
    a.store("config", "v2.0")
    print()

    # C 离开后，D 仍能通过复制数据获取 config
    c.leave_network()
    print()
    result = d.query("config")

    # 去中心化投票
    decentralized_vote([a, b, d], "升级到v3.0")
