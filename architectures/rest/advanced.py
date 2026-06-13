"""REST进阶：HATEOAS (Hypermedia as the Engine of Application State)

演示REST超越CRUD的核心约束：
- 响应包含超媒体链接，客户端动态发现可用操作
- 客户端无需硬编码URL，跟随链接即可导航
- 服务端控制状态流转，客户端只需理解媒体类型
"""

# --- 资源存储 ---
orders = {
    101: {"id": 101, "user_id": 1, "status": "pending", "item": "Book"},
}

# --- HATEOAS：响应包含_links，驱动应用状态 ---
def get_order(order_id):
    order = orders.get(order_id)
    if not order:
        return {"status": 404, "body": "Not found"}
    # 根据当前状态动态生成可用链接——HATEOAS核心
    links = [{"rel": "self", "href": f"/orders/{order_id}", "method": "GET"},
             {"rel": "user", "href": f"/users/{order['user_id']}", "method": "GET"}]
    if order["status"] == "pending":
        links.append({"rel": "pay", "href": f"/orders/{order_id}/pay", "method": "POST"})
        links.append({"rel": "cancel", "href": f"/orders/{order_id}/cancel", "method": "POST"})
    elif order["status"] == "paid":
        links.append({"rel": "ship", "href": f"/orders/{order_id}/ship", "method": "POST"})
    elif order["status"] == "shipped":
        links.append({"rel": "confirm", "href": f"/orders/{order_id}/confirm", "method": "POST"})
    return {"status": 200, "body": {**order, "_links": links}}

def follow_link(order_id, action):
    """客户端跟随链接——无需硬编码业务流程"""
    transitions = {"pay": "paid", "cancel": "cancelled", "ship": "shipped", "confirm": "completed"}
    orders[order_id]["status"] = transitions[action]

def show_links(order_id, note=""):
    res = get_order(order_id)
    body = res["body"]
    print(f"[GET] Order #{body['id']} status={body['status']} {note}")
    for link in body["_links"]:
        print(f"  {link['method']} {link['href']} ({link['rel']})")

if __name__ == "__main__":
    print("=" * 50)
    print("HATEOAS：超媒体驱动应用状态流转")
    print("=" * 50 + "\n")

    show_links(101)                      # pending → 可pay/cancel
    print("\n[HATEOAS] 客户端跟随 rel=pay → 支付")
    follow_link(101, "pay")
    show_links(101)                      # paid → 可ship
    print("\n[HATEOAS] 客户端跟随 rel=ship → 发货")
    follow_link(101, "ship")
    show_links(101, "(只剩确认)")          # shipped → 可confirm
