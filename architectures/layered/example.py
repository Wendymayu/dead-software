"""分层架构 (Layered Architecture) 最小化示例

演示三层分离：展示层(Presentation) → 业务层(Business) → 数据层(Data)
每层只与相邻层交互，不跨层调用。
"""


# --- 数据层：负责数据存取 ---
class DataLayer:
    def __init__(self):
        self._users = {
            "alice": {"name": "Alice", "age": 30},
            "bob": {"name": "Bob", "age": 25},
        }

    def get_user(self, user_id):
        print(f"  [DataLayer] 查询用户: {user_id}")
        return self._users.get(user_id)

    def save_user(self, user_id, data):
        print(f"  [DataLayer] 保存用户: {user_id}")
        self._users[user_id] = data


# --- 业务层：负责业务逻辑 ---
class BusinessLayer:
    def __init__(self, data_layer):
        self.data = data_layer

    def get_user_info(self, user_id):
        print(f" [BusinessLayer] 处理用户查询: {user_id}")
        user = self.data.get_user(user_id)
        if user:
            return f"{user['name']}, 年龄 {user['age']}"
        return "用户不存在"

    def update_age(self, user_id, new_age):
        print(f" [BusinessLayer] 处理年龄更新: {user_id} → {new_age}")
        user = self.data.get_user(user_id)
        if user:
            user["age"] = new_age
            self.data.save_user(user_id, user)
            return f"已更新 {user_id} 的年龄为 {new_age}"
        return "用户不存在"


# --- 展示层：负责用户交互 ---
class PresentationLayer:
    def __init__(self, business_layer):
        self.business = business_layer

    def show_user(self, user_id):
        print(f"[PresentationLayer] 展示用户: {user_id}")
        result = self.business.get_user_info(user_id)
        print(f"[PresentationLayer] 结果: {result}\n")

    def change_age(self, user_id, new_age):
        print(f"[PresentationLayer] 请求修改年龄: {user_id} → {new_age}")
        result = self.business.update_age(user_id, new_age)
        print(f"[PresentationLayer] 结果: {result}\n")


# --- 运行演示 ---
if __name__ == "__main__":
    data = DataLayer()
    business = BusinessLayer(data)
    presentation = PresentationLayer(business)

    print("=" * 40)
    print("分层架构演示：请求从展示层→业务层→数据层流转")
    print("=" * 40 + "\n")

    presentation.show_user("alice")
    presentation.show_user("unknown")
    presentation.change_age("bob", 26)
    presentation.show_user("bob")
