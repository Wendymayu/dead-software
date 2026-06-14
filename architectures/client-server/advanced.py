"""客户端-服务器进阶示例：模拟 Redis 客户端-服务器通信

展示 Redis 核心的客户端-服务器架构：
- RedisServer 监听端口，接受客户端连接，处理命令（GET/SET/PING/SUBSCRIBE）
- 多个 RedisClient 连接同一服务器，并发发送命令
- 服务器用事件循环逐个处理请求，模拟单线程模型
"""

import socketserver, threading, socket, time


class RedisHandler(socketserver.BaseRequestHandler):
    """Redis 服务器命令处理器：逐个处理客户端命令"""
    STORE = {}
    SUBS = {}

    def handle(self):
        peer = self.client_address
        print(f"[Server] 客户端连接: {peer}")
        try:
            while True:
                data = self.request.recv(4096).decode().strip()
                if not data: break
                resp = self._process(data)
                self.request.sendall((resp + "\n").encode())
        except: pass
        print(f"[Server] 客户端断开: {peer}")

    def _process(self, data):
        parts = data.split()
        cmd = parts[0].upper()
        if cmd == "PING": return "PONG"
        elif cmd == "SET": RedisHandler.STORE[parts[1]] = parts[2]; return "OK"
        elif cmd == "GET": return RedisHandler.STORE.get(parts[1], "(nil)")
        elif cmd == "SUBSCRIBE":
            RedisHandler.SUBS.setdefault(parts[1], []).append(self.request)
            return f"SUBSCRIBED {parts[1]}"
        elif cmd == "PUBLISH":
            ch, msg = parts[1], parts[2]
            for s in RedisHandler.SUBS.get(ch, []):
                try: s.sendall(f"PUB {ch} {msg}\n".encode())
                except: pass
            return f"PUBLISHED {len(RedisHandler.SUBS.get(ch, []))}"
        return "ERR unknown command"


class RedisClient:
    """Redis 客户端：连接服务器，发送命令，接收响应"""
    def __init__(self, name):
        self._name = name
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        self._sock.connect((host, port))
        print(f"[Client:{self._name}] 已连接服务器")

    def send(self, cmd):
        print(f"[Client:{self._name}] 发送: {cmd}")
        self._sock.sendall((cmd + "\n").encode())
        time.sleep(0.05)
        return self._sock.recv(4096).decode().strip()

    def close(self):
        self._sock.close()
        print(f"[Client:{self._name}] 断开连接")


if __name__ == "__main__":
    print("=" * 50)
    print("进阶演示: 模拟 Redis 客户端-服务器架构")
    print("=" * 50 + "\n")

    server = socketserver.ThreadingTCPServer(("localhost", 6380), RedisHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    print("[Server] Redis 服务器监听 localhost:6380\n")

    c1 = RedisClient("A"); c1.connect("localhost", 6380)
    c2 = RedisClient("B"); c2.connect("localhost", 6380)
    c3 = RedisClient("C"); c3.connect("localhost", 6380)

    # 客户端A：SET + GET
    print(f"[Client:A] 收到: {c1.send('SET mykey hello')}")
    print(f"[Client:A] 收到: {c1.send('GET mykey')}")

    # 客户端B：并发 SET + PING
    print(f"[Client:B] 收到: {c2.send('SET counter 42')}")
    print(f"[Client:B] 收到: {c2.send('PING')}")

    # 客户端C：订阅频道，客户端A：发布消息
    print(f"[Client:C] 收到: {c3.send('SUBSCRIBE news')}")
    print(f"[Client:A] 收到: {c1.send('PUBLISH news breaking')}")

    # 客户端B读取A写入的数据——共享存储
    print(f"[Client:B] 收到: {c2.send('GET mykey')}")

    print("\n[Server] 单线程事件循环处理所有客户端并发请求")
    for c in [c1, c2, c3]: c.close()
    server.shutdown()
