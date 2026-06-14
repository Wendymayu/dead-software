"""绞杀者模式进阶示例：GitHub 的 Rails 单体迁移

模拟 GitHub 的 strangler 迁移过程：
- 旧系统(Rails单体)处理所有请求
- 路由层(Facade)决定请求由旧系统还是新服务处理
- 新服务(Go)逐步接管特定路由
- 迁移阶段：100% Rails → 混合 → 100% 新服务
"""


class RailsMonolith:
    """旧系统：Rails单体，处理所有业务"""
    def __init__(self):
        self._users = {"u1": {"name": "alice"}, "u2": {"name": "bob"}}
        self._repos = {"r1": {"name": "project-x", "owner": "u1"}}
        self._auth_tokens = {"token_alice": "u1"}

    def handle(self, route, data):
        print(f"    [Rails单体] 处理 {route}")
        if route == "/users":
            return list(self._users.values())
        elif route == "/repos":
            return list(self._repos.values())
        elif route == "/auth":
            return {"user_id": self._auth_tokens.get(data.get("token"))}
        elif route == "/git/push":
            repo = self._repos.get(data["repo_id"])
            return {"pushed": True, "repo": repo["name"], "by": "Rails"}
        return {"error": "unknown route"}


class GoService:
    """新服务：Go实现，逐步接管高负载路由"""
    def __init__(self):
        self._git_data = {"r1": {"commits": 42}}

    def handle(self, route, data):
        print(f"    [Go服务] 处理 {route} (高性能)")
        if route == "/git/push":
            repo_id = data["repo_id"]
            self._git_data[repo_id]["commits"] += 1
            return {"pushed": True, "repo": repo_id, "commits": self._git_data[repo_id]["commits"], "by": "Go"}
        elif route == "/auth":
            return {"user_id": "u1", "service": "GoAuth"}
        return {"error": "unknown route"}


class StranglerFacade:
    """绞杀者路由层：决定请求由旧系统还是新服务处理"""
    def __init__(self, legacy, new_service):
        self._legacy = legacy
        self._new = new_service
        self._routes = {}  # route → "new" | "legacy"

    def migrate_route(self, route):
        """迁移路由到新服务"""
        self._routes[route] = "new"
        print(f"  [路由层] {route} → 迁移到Go服务")

    def handle(self, route, data):
        target = self._routes.get(route, "legacy")
        handler = self._new if target == "new" else self._legacy
        print(f"  [路由层] {route} → {target}")
        return handler.handle(route, data)


if __name__ == "__main__":
    rails = RailsMonolith()
    go = GoService()
    facade = StranglerFacade(rails, go)

    print("=" * 50)
    print("GitHub 绞杀者迁移：Rails单体 → Go微服务")
    print("=" * 50 + "\n")

    print("--- 阶段1: 100% Rails单体 ---")
    facade.handle("/users", {})
    facade.handle("/git/push", {"repo_id": "r1"})
    print()

    print("--- 阶段2: 迁移git路由(Git操作→Go) ---")
    facade.migrate_route("/git/push")
    facade.handle("/users", {})            # 仍→Rails
    facade.handle("/git/push", {"repo_id": "r1"})  # →Go
    print()

    print("--- 阶段3: 迁移auth路由(认证→Go) ---")
    facade.migrate_route("/auth")
    facade.handle("/auth", {"token": "token_alice"})  # →GoAuth
    facade.handle("/users", {})                       # 仍→Rails
    print()

    print("--- 阶段4: 最终状态(Git+Auth已迁移) ---")
    print("  Rails单体可逐步缩减，最终只保留UI和轻量逻辑")
    print("  GitHub真实案例：git操作→Go，认证→独立服务，API→新系统")

    print("\n--- 核心洞察 ---")
    print("  绞杀者模式的关键：路由层(Facade)是迁移的枢纽")
    print("  每次只迁移一个路由，新旧并存，逐步替换——零停机迁移")
