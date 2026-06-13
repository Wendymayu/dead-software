"""REST架构 (Representational State Transfer) 最小化示例

演示REST核心约束：
- 资源(Resource)通过URI标识，统一接口操作
- 无状态通信：每次请求自带全部上下文
- 标准媒体类型响应
"""

# --- 资源与存储：模拟后端数据 ---
resources = {
    "/users": [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
    "/orders": [{"id": 101, "user_id": 1, "item": "Book"}],
}

# --- 统一接口：GET/POST/PUT/DELETE ---
def handle_request(method, uri, body=None):
    """每个请求自足——无状态，不依赖之前的请求"""
    store = resources.get(uri)
    if store is None:
        return {"status": 404, "body": f"Resource {uri} not found"}

    if method == "GET":
        # GET：读取资源集合
        return {"status": 200, "body": store}
    elif method == "POST":
        # POST：创建新资源，body自带全部信息
        new_id = max(r["id"] for r in store) + 1
        body["id"] = new_id
        store.append(body)
        return {"status": 201, "body": body}
    elif method == "PUT":
        # PUT：更新资源，body必须包含完整状态(无状态约束)
        for r in store:
            if r["id"] == body["id"]:
                r.update(body)
                return {"status": 200, "body": r}
        return {"status": 404, "body": "Item not found"}
    elif method == "DELETE":
        # DELETE：移除资源
        resources[uri] = [r for r in store if r["id"] != body["id"]]
        return {"status": 204, "body": None}

if __name__ == "__main__":
    print("=" * 50)
    print("REST架构：统一接口 + 无状态通信")
    print("=" * 50 + "\n")

    # GET——读取用户列表(请求无需额外上下文)
    res = handle_request("GET", "/users")
    print(f"[GET /users] {res['status']} → {res['body']}")

    # POST——创建用户(请求自带全部信息)
    res = handle_request("POST", "/users", {"name": "Carol"})
    print(f"[POST /users] {res['status']} → {res['body']}")

    # PUT——完整替换(无状态：必须传完整对象)
    res = handle_request("PUT", "/users", {"id": 1, "name": "Alice-Updated"})
    print(f"[PUT /users]  {res['status']} → {res['body']}")

    # DELETE——删除(请求包含目标资源标识)
    res = handle_request("DELETE", "/orders", {"id": 101})
    print(f"[DELETE /orders] {res['status']} → deleted")

    # 无状态验证：再次GET看到最终状态，无需记住历史
    res = handle_request("GET", "/users")
    print(f"\n[GET /users] 最终状态 → {res['body']}")
    res = handle_request("GET", "/orders")
    print(f"[GET /orders] 最终状态 → {res['body']}")
