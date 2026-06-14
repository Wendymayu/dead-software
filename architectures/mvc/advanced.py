"""MVC 进阶示例：模拟 Spring MVC 请求生命周期

展示 Spring MVC 核心流程：
- DispatcherServlet: 前端控制器，统一接收所有请求
- HandlerMapping: 将 URL 映射到 Controller 方法
- Controller: 调用 Service → Repository，返回逻辑视图名
- ViewResolver: 将逻辑视图名解析为模板
- 请求: GET /users/1 → DispatcherServlet → UserController#show → UserService → UserRepository → View
"""


class DispatcherServlet:
    """Spring MVC 前端控制器：所有请求入口"""
    def __init__(self):
        self._handler_mappings = {}
        self._view_resolver = None

    def register_handler(self, url, controller, method):
        self._handler_mappings[url] = (controller, method)

    def set_view_resolver(self, resolver):
        self._view_resolver = resolver

    def do_dispatch(self, url, params=None):
        print(f"[DispatcherServlet] 收到请求: {url}")
        if url not in self._handler_mappings:
            print(f"[DispatcherServlet] 404: 无匹配Handler -> {url}")
            return "404"
        controller, method = self._handler_mappings[url]
        print(f"[DispatcherServlet] HandlerMapping: {url} -> "
              f"{controller.__class__.__name__}#{method}")
        # Controller 返回逻辑视图名 + 数据
        view_name, model = getattr(controller, method)(params or {})
        # ViewResolver 解析视图
        view = self._view_resolver.resolve(view_name)
        print(f"[DispatcherServlet] ViewResolver: '{view_name}' -> {view}")
        print(f"[DispatcherServlet] 渲染视图: {view}, 数据: {model}")
        return model


class UserRepository:
    """Spring Repository 层：数据访问（模拟 JPA/Hibernate）"""
    _db = [{"id": 1, "name": "Alice", "role": "ADMIN"},
           {"id": 2, "name": "Bob", "role": "USER"}]

    @classmethod
    def findById(cls, id):
        r = next((u for u in cls._db if u["id"] == id), None)
        print(f"  [Repository] JPA findById(id={id}) -> {r['name'] if r else 'null'}")
        return r

    @classmethod
    def findAll(cls):
        print(f"  [Repository] JPA findAll() -> {len(cls._db)} 条记录")
        return cls._db


class UserService:
    """Spring Service 层：业务逻辑"""

    @classmethod
    def getUser(cls, id):
        print(f" [Service] UserService.getUser(id={id})")
        user = UserRepository.findById(id)
        if not user:
            return None
        # Service 层做业务转换（如角色描述）
        return {**user, "role_desc": "管理员" if user["role"] == "ADMIN" else "普通用户"}

    @classmethod
    def listUsers(cls):
        print(f" [Service] UserService.listUsers()")
        return [{"id": u["id"], "name": u["name"]} for u in UserRepository.findAll()]


class UserController:
    """Spring @RestController: 协调 Service，返回视图名和数据"""

    def show(self, params):
        print(f"[Controller] @GetMapping(\"/users/{{id}}\") id={params.get('id')}")
        user = UserService.getUser(params.get("id"))
        if not user:
            print(f"[Controller] 用户不存在 -> 返回视图 'error/404'")
            return "error/404", {"msg": "用户不存在"}
        return "users/detail", {"user": user}

    def list(self, params):
        print(f"[Controller] @GetMapping(\"/users\")")
        users = UserService.listUsers()
        return "users/list", {"users": users}


class ViewResolver:
    """Spring ViewResolver: 逻辑视图名 -> 模板路径"""
    def __init__(self):
        self._prefix = "templates/"
        self._suffix = ".html"

    def resolve(self, view_name):
        # "users/detail" -> "templates/users/detail.html"
        return f"{self._prefix}{view_name}{self._suffix}"


if __name__ == "__main__":
    dispatcher = DispatcherServlet()
    dispatcher.set_view_resolver(ViewResolver())
    dispatcher.register_handler("/users", UserController(), "list")
    dispatcher.register_handler("/users/1", UserController(), "show")

    print("=" * 50)
    print("Spring MVC 请求生命周期模拟")
    print("=" * 50 + "\n")

    print("--- GET /users (用户列表) ---")
    dispatcher.do_dispatch("/users")
    print()

    print("--- GET /users/1 (用户详情) ---")
    dispatcher.do_dispatch("/users/1", {"id": 1})
    print()

    print("--- GET /users/99 (不存在) ---")
    dispatcher.do_dispatch("/users/1", {"id": 99})
