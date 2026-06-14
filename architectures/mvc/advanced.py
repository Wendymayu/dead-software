"""MVC 进阶示例：模拟 Ruby on Rails 请求生命周期

展示 Rails MVC 核心流程：
- Router: config/routes.rb 将 URL 映射到 Controller#action
- Controller: 调用 Model 获取数据，选择 View 渲染
- Model (ActiveRecord): 数据查询 + 业务规则
- View (ERB 模板): 数据嵌入 HTML
- 请求: GET /users/1 → Router → UsersController#show → UserModel.find → View
"""


class Router:
    """模拟 Rails config/routes.rb: URL → Controller#action"""
    def __init__(self):
        self._routes = {}

    def draw(self, url, controller_cls, action):
        self._routes[url] = (controller_cls, action)

    def dispatch(self, url, params=None):
        if url not in self._routes:
            print(f"[Router] 404: 无匹配路由 {url}")
            return "404"
        cls, action = self._routes[url]
        print(f"[Router] {url} → {cls.__name__}#{action}")
        return getattr(cls(), action)(params or {})


class UserModel:
    """模拟 Rails ActiveRecord: 数据查询"""
    _db = [{"id": 1, "name": "Alice", "role": "admin"},
           {"id": 2, "name": "Bob", "role": "user"}]

    @classmethod
    def find(cls, id):
        r = next((u for u in cls._db if u["id"] == id), None)
        print(f"  [Model] ActiveRecord.find(id={id}) → {r['name'] if r else 'nil'}")
        return r

    @classmethod
    def all(cls):
        print(f"  [Model] ActiveRecord.all() → {len(cls._db)} 条")
        return cls._db


class UsersController:
    """模拟 Rails Controller: 协调 Model 和 View"""
    def index(self, params):
        print("[Controller] UsersController#index")
        users = UserModel.all()
        rows = "".join(f"<tr><td>{u['id']}</td><td>{u['name']}</td><td>{u['role']}</td></tr>\n" for u in users)
        print(f"  [View] 渲染 users/index.html.erb:\n<table>\n{rows}</table>")
        return rows

    def show(self, params):
        print(f"[Controller] UsersController#show(id={params.get('id')})")
        user = UserModel.find(params.get("id"))
        if not user:
            print("  [Controller] 记录未找到 → 404")
            return "404"
        html = f"<h1>{user['name']}(ID:{user['id']})</h1><p>角色: {user['role']}</p>"
        print(f"  [View] 渲染 users/show.html.erb:\n{html}")
        return html


if __name__ == "__main__":
    router = Router()
    # 模拟 Rails: resources :users
    router.draw("/users", UsersController, "index")
    router.draw("/users/:id", UsersController, "show")

    print("=" * 50)
    print("Rails MVC 请求生命周期模拟")
    print("=" * 50 + "\n")

    print("--- GET /users (列表页) ---")
    router.dispatch("/users")
    print()

    print("--- GET /users/1 (详情页) ---")
    router.dispatch("/users/:id", {"id": 1})
    print()

    print("--- GET /users/99 (不存在) ---")
    router.dispatch("/users/:id", {"id": 99})
