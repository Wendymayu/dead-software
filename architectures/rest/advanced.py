"""REST 进阶示例：Stripe API 设计风格

模拟 Stripe 的 REST API 设计：
- 资源(Customers/Charges) + HTTP方法语义
- 统一错误格式、cursor分页、幂等键、关联资源链接(HATEOAS-lite)
"""


class StripeAPI:
    def __init__(self):
        self._customers, self._charges, self._idempotency, self._next_id = {}, {}, {}, 1

    def _new_id(self, prefix):
        id = f"{prefix}_{self._next_id}"
        self._next_id += 1
        return id

    def _links(self, resource, id, related=None):
        links = [{"rel": "self", "href": f"/v1/{resource}/{id}"}]
        for r, rid in (related or []):
            links.append({"rel": r, "href": f"/v1/{r}/{rid}"})
        return links

    def _error(self, type, msg, status):
        print(f"  [error] {type}: {msg}")
        return {"status": status, "body": {"error": {"type": type, "message": msg}}}

    def _check_idempotency(self, key):
        if key and key in self._idempotency:
            print(f"  [idempotent] key={key} -> 返回已有结果")
            return self._idempotency[key]
        return None

    def _save_idempotency(self, key, result):
        if key:
            self._idempotency[key] = result

    def POST_customers(self, data, idempotency_key=None):
        cached = self._check_idempotency(idempotency_key)
        if cached:
            return cached
        id = self._new_id("cus")
        customer = {"id": id, "name": data["name"], "email": data["email"], "_links": self._links("customers", id)}
        self._customers[id] = customer
        result = {"status": 200, "body": customer}
        self._save_idempotency(idempotency_key, result)
        print(f"  [POST /customers] 创建客户: {id}")
        return result

    def GET_customers(self, limit=3, starting_after=None):
        ids = sorted(self._customers.keys())
        if starting_after:
            ids = [i for i in ids if i > starting_after]
        has_more = len(ids) > limit
        print(f"  [GET /customers] limit={limit}, has_more={has_more}")
        return {"status": 200, "body": {"data": [self._customers[i] for i in ids[:limit]], "has_more": has_more}}

    def POST_charges(self, data, idempotency_key=None):
        cached = self._check_idempotency(idempotency_key)
        if cached:
            return cached
        cus_id = data["customer_id"]
        if cus_id not in self._customers:
            return self._error("customer_not_found", f"客户 {cus_id} 不存在", 404)
        id = self._new_id("ch")
        charge = {"id": id, "amount": data["amount"], "customer": cus_id,
                  "_links": self._links("charges", id, [("customers", cus_id)])}
        self._charges[id] = charge
        result = {"status": 200, "body": charge}
        self._save_idempotency(idempotency_key, result)
        print(f"  [POST /charges] 创建支付: {id}, amount={data['amount']}")
        return result


if __name__ == "__main__":
    api = StripeAPI()
    print("=" * 50)
    print("Stripe风格 REST API: 资源+方法+错误+分页+幂等")
    print("=" * 50 + "\n")

    print("--- 1. 创建客户(POST /customers) ---")
    api.POST_customers({"name": "Alice", "email": "a@test.com"})
    api.POST_customers({"name": "Bob", "email": "b@test.com"})
    print("\n--- 2. 分页查询(GET /customers) ---")
    api.GET_customers(limit=1)
    print("\n--- 3. 创建支付+幂等键 ---")
    api.POST_charges({"customer_id": "cus_1", "amount": 2000}, idempotency_key="pay_alice_1")
    print("\n--- 4. 重复请求(幂等) ---")
    api.POST_charges({"customer_id": "cus_1", "amount": 2000}, idempotency_key="pay_alice_1")
    print("\n--- 5. 错误响应(统一格式) ---")
    api.POST_charges({"customer_id": "cus_999", "amount": 100})
    print("\n--- 6. 关联资源链接 ---")
    charge = api.POST_charges({"customer_id": "cus_2", "amount": 500})
    print(f"  _links: {charge['body']['_links']}")
    print("\n核心洞察: Stripe=REST标杆, 幂等键防重复/统一错误/cursor分页/HATEOAS-lite链接")
