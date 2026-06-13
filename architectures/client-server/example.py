"""客户端-服务器架构 (Client-Server) 最小化示例

模拟请求/响应循环：客户端发请求，服务器处理并响应。
展示服务器处理多个客户端请求的基本模型。
"""


# --- 服务器：接收请求，处理并返回响应 ---
class Server:
    def __init__(self):
        self._data = {"users": {"alice": 30, "bob": 25}}

    def handle_request(self, client_name, action, params):
        print(f"  [Server] 收到 {client_name} 的请求: {action} {params}")
        if action == "GET_USER":
            name = params.get("name", "")
            age = self._data["users"].get(name)
            if age is not None:
                return {"status": "OK", "data": {"name": name, "age": age}}
            return {"status": "ERROR", "msg": f"用户 {name} 不存在"}
        elif action == "ADD_USER":
            name, age = params.get("name"), params.get("age")
            self._data["users"][name] = age
            return {"status": "OK", "msg": f"用户 {name} 已添加"}
        return {"status": "ERROR", "msg": "未知操作"}


# --- 客户端：构造请求，发送给服务器，接收响应 ---
class Client:
    def __init__(self, name, server):
        self._name = name
        self._server = server

    def send_request(self, action, params):
        print(f"[Client-{self._name}] 发送请求: {action} {params}")
        response = self._server.handle_request(self._name, action, params)
        print(f"[Client-{self._name}] 收到响应: {response}")
        return response


# --- 运行演示 ---
if __name__ == "__main__":
    server = Server()

    # 多个客户端共享同一服务器
    client_a = Client("A", server)
    client_b = Client("B", server)

    print("=" * 45)
    print("Client-Server 演示: 客户端请求 → 服务器响应")
    print("=" * 45 + "\n")

    client_a.send_request("GET_USER", {"name": "alice"})
    print()
    client_b.send_request("GET_USER", {"name": "unknown"})
    print()
    client_a.send_request("ADD_USER", {"name": "charlie", "age": 35})
    print()
    client_b.send_request("GET_USER", {"name": "charlie"})  # B 也能看到 A 添加的数据
