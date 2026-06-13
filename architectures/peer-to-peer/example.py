"""对等网络架构 (Peer-to-Peer) 最小化示例

节点既是客户端又是服务器，无中心权威。节点直接通信，
数据分散存储。对比客户端-服务器：没有专属的服务器节点。
"""


# --- 节点：既是客户端又是服务器 ---
class PeerNode:
    def __init__(self, name):
        self._name = name
        self._data = {}       # 本地存储的数据
        self._neighbors = []  # 直接连接的对等节点

    def connect(self, other):
        """节点之间直接建立连接——没有中心服务器"""
        self._neighbors.append(other)
        other._neighbors.append(self)
        print(f"[P2P] {self._name} <-> {other._name} 建立直连")

    def store(self, key, value):
        """本地存储数据"""
        self._data[key] = value
        print(f"  [{self._name}] 存储: {key}={value}")

    def query(self, key):
        """先查本地，没有则向邻居查询——自己既是客户端又是服务器"""
        if key in self._data:
            print(f"  [{self._name}] 本地命中: {key}={self._data[key]}")
            return self._data[key]
        # 向邻居节点查询（作为客户端）
        print(f"  [{self._name}] 本地未命中，向邻居查询: {key}")
        for neighbor in self._neighbors:
            result = neighbor._respond_query(key, exclude=self._name)
            if result is not None:
                print(f"  [{self._name}] 从 {neighbor._name} 获得: {key}={result}")
                return result
        print(f"  [{self._name}] 全网未找到: {key}")
        return None

    def _respond_query(self, key, exclude=None):
        """响应邻居查询（作为服务器）"""
        if key in self._data:
            return self._data[key]
        for neighbor in self._neighbors:
            if neighbor._name != exclude:
                result = neighbor._respond_query(key, exclude=self._name)
                if result is not None:
                    return result
        return None


# --- 运行演示 ---
if __name__ == "__main__":
    a, b, c = PeerNode("A"), PeerNode("B"), PeerNode("C")

    print("=" * 45)
    print("P2P 演示: 无中心，节点直连互查数据")
    print("=" * 45 + "\n")

    # 建立对等连接
    a.connect(b)
    b.connect(c)

    # 数据分散存储在不同节点
    a.store("file1", "data-A")
    c.store("file3", "data-C")
    print()

    # B 本地没有 file1，通过邻居网络查到
    b.query("file1")
    print()
    # A 查 file3，通过 B 中转到 C
    a.query("file3")
