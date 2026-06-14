"""分层架构进阶示例：模拟 Django MTV 分层架构

展示请求在 Django 各层的流转：
URL路由 → View(业务逻辑) → Model(数据访问) → Template(响应格式化)
每层只调用下一层，不跨层访问。
"""


# --- Model层：数据访问 ---
class DjangoModel:
    """模拟 Django ORM Model，封装数据存取"""

    def __init__(self):
        self._db = {"alice": {"name": "Alice", "age": 30, "role": "admin"},
                    "bob": {"name": "Bob", "age": 25, "role": "user"}}

    def get_user(self, pk: str) -> dict | None:
        print(f"  [Model] ORM查询: pk={pk}")
        return self._db.get(pk)

    def filter_users(self, role: str) -> list[dict]:
        print(f"  [Model] ORM过滤: role={role}")
        return [u for u in self._db.values() if u["role"] == role]


# --- Template层：响应格式化 ---
class DjangoTemplate:
    """模拟 Django Template，将数据渲染为响应文本"""

    def render(self, template_name: str, context: dict) -> str:
        if template_name == "user_detail":
            user = context["user"]
            return f"<h1>{user['name']}</h1><p>年龄:{user['age']} 角色:{user['role']}</p>"
        elif template_name == "user_list":
            users = context["users"]
            items = "".join(f"<li>{u['name']}</li>" for u in users)
            return f"<ul>{items}</ul>"
        print(f"  [Template] 渲染: {template_name}")
        return ""


# --- View层：业务逻辑（只调Model和Template） ---
class DjangoView:
    """模拟 Django View，协调Model和Template"""

    def __init__(self, model: DjangoModel, template: DjangoTemplate):
        self.model = model
        self.template = template

    def user_detail(self, pk: str) -> str:
        print(f"  [View] 处理请求: user_detail pk={pk}")
        user = self.model.get_user(pk)       # 只调Model层
        if not user:
            return "<p>用户不存在</p>"
        return self.template.render("user_detail", {"user": user})  # 只调Template层

    def user_list(self, role: str) -> str:
        print(f"  [View] 处理请求: user_list role={role}")
        users = self.model.filter_users(role)
        return self.template.render("user_list", {"users": users})


# --- URL路由层：分发请求到对应View ---
class URLDispatcher:
    """模拟 Django URL路由，将路径映射到View方法"""

    def __init__(self, view: DjangoView):
        self.view = view
        self._routes = {
            "/user/<pk>": view.user_detail,
            "/users/<role>": view.user_list,
        }

    def dispatch(self, path: str, **kwargs) -> str:
        print(f"[URL路由] 匹配路径: {path}")
        handler = self._routes.get(path)
        if handler:
            return handler(**kwargs)
        return "<p>404 未找到</p>"


if __name__ == "__main__":
    model = DjangoModel()
    template = DjangoTemplate()
    view = DjangoView(model, template)
    urls = URLDispatcher(view)

    print("=" * 50)
    print("Django MTV分层: URL路由 → View → Model → Template")
    print("=" * 50)

    print("\n--- 请求1: 查看用户详情 ---")
    print(urls.dispatch("/user/<pk>", pk="alice"))

    print("\n--- 请求2: 查看管理员列表 ---")
    print(urls.dispatch("/users/<role>", role="admin"))

    print("\n--- 请求3: 未知路径 ---")
    print(urls.dispatch("/unknown"))
