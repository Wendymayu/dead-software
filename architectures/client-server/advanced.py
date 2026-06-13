"""客户端-服务器进阶示例：模拟网络延迟 + 请求队列

展示服务器如何有序处理多个客户端的并发请求：
- 请求队列：服务器依次处理，保证顺序
- 响应回调：客户端通过回调接收响应
- 连接管理：服务器维护活跃客户端列表
"""


# --- 服务器：带请求队列和回调分发 ---
class Server:
    def __init__(self):
        self._data = {"items": []}
        self._request_queue = []
        self._clients = {}

    def register_client(self, name, callback):
        self._clients[name] = callback
        print(f"[Server] 客户端 {name} 已注册")

    def enqueue(self, client_name, action, params):
        self._request_queue.append((client_name, action, params))

    def process_all(self):
        print(f"[Server] 处理队列中 {len(self._request_queue)} 个请求...")
        for client_name, action, params in self._request_queue:
            print(f"  [Server] 处理 {client_name} → {action}")
            response = self._handle(action, params)
            # 通过回调将响应发送给对应客户端
            self._clients[client_name](response)
        self._request_queue.clear()

    def _handle(self, action, params):
        if action == "ADD_ITEM":
            self._data["items"].append(params["item"])
            return {"status": "OK", "count": len(self._data["items"])}
        elif action == "LIST_ITEMS":
            return {"status": "OK", "items": self._data["items"]}
        return {"status": "ERROR", "msg": "未知操作"}


# --- 客户端：带回调响应 ---
class Client:
    def __init__(self, name, server):
        self._name = name
        self._server = server
        self._server.register_client(name, self._on_response)

    def send_request(self, action, params):
        print(f"[Client-{self._name}] 发送: {action} {params}")
        self._server.enqueue(self._name, action, params)

    def _on_response(self, response):
        print(f"[Client-{self._name}] 回调响应: {response}")


# --- 运行演示 ---
if __name__ == "__main__":
    server = Server()

    print("=" * 50)
    print("进阶演示: 请求队列 + 回调分发")
    print("=" * 50 + "\n")

    # 两个客户端同时发送请求（排队）
    c1 = Client("A", server)
    c2 = Client("B", server)

    c1.send_request("ADD_ITEM", {"item": "apple"})
    c2.send_request("ADD_ITEM", {"item": "banana"})
    c1.send_request("LIST_ITEMS", {})

    print()
    server.process_all()  # 服务器一次性处理所有排队请求
