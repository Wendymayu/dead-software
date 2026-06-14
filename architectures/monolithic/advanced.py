"""单体架构进阶示例：模拟 WordPress 单体结构
展示 WordPress 的单体+插件机制：
一个类同时处理路由、模板、数据库、认证、内容管理，插件通过钩子扩展功能。"""


# --- WordPress 单体应用 ---
class WordPressApp:
    """模拟 WordPress：路由+模板+数据库+认证+内容 全在一个类"""

    def __init__(self):
        self._db = {"posts": [], "users": {"admin": {"password": "p@ss", "role": "admin"}}}
        self._hooks = {"actions": {}, "filters": {}}

    # --- 钩子系统：单体内的扩展机制 ---
    def add_action(self, hook_name: str, callback):
        """注册动作钩子（如 'init', 'publish_post'）"""
        self._hooks["actions"].setdefault(hook_name, []).append(callback)

    def add_filter(self, hook_name: str, callback):
        """注册过滤器钩子（修改数据，如 'the_content'）"""
        self._hooks["filters"].setdefault(hook_name, []).append(callback)

    def _do_action(self, hook_name: str, *args):
        for cb in self._hooks["actions"].get(hook_name, []):
            cb(*args)

    def _apply_filters(self, hook_name: str, value):
        for cb in self._hooks["filters"].get(hook_name, []):
            value = cb(value)
        return value

    # --- 路由 ---
    def route(self, path: str, **kwargs) -> str:
        print(f"[路由] 请求路径: {path}")
        self._do_action("init")
        if path == "/post/new":
            return self.create_post(**kwargs)
        elif path == "/post/list":
            return self.list_posts()
        return "404 未找到"

    # --- 用户认证 ---
    def _authenticate(self, username: str) -> bool:
        print(f"[认证] 检查用户: {username}")
        return username in self._db["users"]

    # --- 内容管理 ---
    def create_post(self, title: str, content: str, author: str = "admin") -> str:
        if not self._authenticate(author):
            return "未授权"
        content = self._apply_filters("the_content", content)
        post = {"title": title, "content": content, "author": author}
        self._db["posts"].append(post)
        self._do_action("publish_post", post)
        return self._render("post_detail", post)

    def list_posts(self) -> str:
        return self._render("post_list", {"posts": self._db["posts"]})

    # --- 模板渲染 ---
    def _render(self, template: str, data: dict) -> str:
        print(f"[模板] 渲染: {template}")
        if template == "post_detail":
            return f"<h1>{data['title']}</h1><p>{data['content']}</p>"
        elif template == "post_list":
            items = "".join(f"<li>{p['title']}</li>" for p in data["posts"])
            return f"<ul>{items}</ul>"
        return ""


# --- 插件：通过钩子扩展单体 ---
def seo_plugin(content: str) -> str:
    """过滤器插件：为内容添加SEO元数据"""
    return f"{content}\n<meta name='seo'>已优化"

def notify_plugin(post: dict):
    """动作插件：发布文章时发送通知"""
    print(f"[通知插件] 文章已发布: {post['title']}")


if __name__ == "__main__":
    wp = WordPressApp()

    print("=" * 50 + "\nWordPress单体: 路由+认证+内容+模板+钩子\n" + "=" * 50)
    wp.add_filter("the_content", seo_plugin)
    wp.add_action("publish_post", notify_plugin)

    # 创建文章
    print("\n--- 创建文章 ---")
    print(wp.route("/post/new", title="Python架构", content="分层设计很重要"))

    # 列出文章
    print("\n--- 列出文章 ---")
    print(wp.route("/post/list"))
