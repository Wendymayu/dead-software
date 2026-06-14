"""P2P 进阶示例：模拟 BitTorrent 文件分片交换
展示 BitTorrent 的核心 P2P 架构：
- Tracker：发现协调者，帮助 Peer 发现彼此（不传输数据）
- Peer：直接与其他 Peer 连接，请求和交换文件分片
- Peer A 从 Peer B 下载分片 → Peer A 拥有新分片后可共享给其他人
"""

import socket, threading, json, time

class Tracker:
    """Tracker：帮助 Peer 发现彼此，不传输数据"""
    def __init__(self):
        self._peers = {}
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def start(self, port):
        self._server.bind(("localhost", port)); self._server.listen(5)
        threading.Thread(target=self._serve, daemon=True).start()
        print(f"[Tracker] 启动，监听 localhost:{port}")
    def _serve(self):
        while True:
            conn, _ = self._server.accept()
            d = json.loads(conn.recv(4096).decode())
            self._peers[d["peer"]] = d["addr"]
            conn.sendall(json.dumps({"peers": dict(self._peers)}).encode())
            conn.close()
            print(f"[Tracker] {d['peer']} 加入，当前 Peers: {list(self._peers.keys())}")

class Peer:
    """Peer：直接与其他 Peer 交换分片"""
    TOTAL = 8
    def __init__(self, name, port):
        self._name, self._port, self._have, self._known = name, port, set(), {}
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def start_server(self):
        self._server.bind(("localhost", self._port)); self._server.listen(5)
        threading.Thread(target=self._serve_pieces, daemon=True).start()
        print(f"[Peer:{self._name}] 监听 localhost:{self._port}")
    def _serve_pieces(self):
        while True:
            conn, _ = self._server.accept()
            d = json.loads(conn.recv(4096).decode())
            if d["cmd"] == "have":
                conn.sendall(json.dumps({"pieces": list(self._have)}).encode())
            elif d["cmd"] == "download" and d["piece"] in self._have:
                print(f"[Peer:{self._name}] 向 {d['from']} 上传分片 {d['piece']}")
                conn.sendall(json.dumps({"piece": d["piece"]}).encode())
            conn.close()
    def announce(self, tracker_addr):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect(tracker_addr)
        s.sendall(json.dumps({"peer": self._name, "addr": f"localhost:{self._port}"}).encode())
        self._known = json.loads(s.recv(4096).decode())["peers"]; s.close()
    def seed(self, pieces):
        for p in pieces: self._have.add(p)
        print(f"[Peer:{self._name}] 种子拥有分片: {sorted(self._have)}")
    def download(self, piece_id):
        for name, addr in self._known.items():
            if name == self._name: continue
            host, port = addr.split(":")
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s.connect((host, int(port)))
            s.sendall(json.dumps({"cmd": "have"}).encode())
            resp = json.loads(s.recv(4096).decode())
            if piece_id in resp["pieces"] and piece_id not in self._have:
                s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM); s2.connect((host, int(port)))
                s2.sendall(json.dumps({"cmd": "download", "piece": piece_id, "from": self._name}).encode())
                s2.recv(4096); s2.close()
                print(f"[Peer:{self._name}] 从 {name} 下载分片 {piece_id}")
                self._have.add(piece_id)
            s.close()
    def status(self):
        have, miss = sorted(self._have), sorted(set(range(self.TOTAL)) - self._have)
        print(f"[Peer:{self._name}] 已有 {have}, 缺少 {miss}")

if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示: 模拟 BitTorrent P2P 分片交换")
    print("=" * 50 + "\n")
    tracker = Tracker(); tracker.start(7000)
    p1 = Peer("Seeder-1", 7001); p1.start_server(); p1.seed([0, 1, 2, 3])
    p2 = Peer("Seeder-2", 7002); p2.start_server(); p2.seed([4, 5, 6, 7])
    p3 = Peer("Leecher-1", 7003); p3.start_server()
    p4 = Peer("Leecher-2", 7004); p4.start_server()
    for p in [p1, p2, p3, p4]: p.announce(("localhost", 7000))
    time.sleep(0.1)
    print("\n--- Peers 直接交换分片（无中央服务器传输数据）---")
    p3.download(0); p3.download(4); p4.download(1); p4.download(5)
    print("\n--- Leecher 之间互相交换 ---")
    p4.download(0)
    print("\n--- 各 Peer 状态 ---")
    for p in [p1, p2, p3, p4]: p.status()
