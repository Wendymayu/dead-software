"""复制粘贴编程 反模式 最小化示例

演示复制代码 vs 抽象通用方案：
- 3 个几乎相同的验证函数
- 1 个抽象后的通用验证器
"""

# --- 反模式 ---
def validate_email(text):
    if "@" not in text:
        print(f"[复制] '{text}' 邮箱验证失败: 缺少@")
        return False
    print(f"[复制] '{text}' 邮箱验证通过")
    return True

def validate_age(text):
    try:
        age = int(text)
        if age < 0 or age > 150:
            print(f"[复制] '{text}' 年龄验证失败: 范围不对")
            return False
    except ValueError:
        print(f"[复制] '{text}' 年龄验证失败: 不是数字")
        return False
    print(f"[复制] '{text}' 年龄验证通过")
    return True

def validate_name(text):
    if len(text) < 2:
        print(f"[复制] '{text}' 名称验证失败: 太短")
        return False
    print(f"[复制] '{text}' 名称验证通过")
    return True

# --- 正确做法 ---
class Validator:
    """通用验证器：规则 + 提示可配置"""
    def __init__(self, name, rule, fail_msg):
        self._name = name
        self._rule = rule
        self._fail_msg = fail_msg

    def validate(self, value):
        if not self._rule(value):
            print(f"[抽象] '{value}' {self._name}{self._fail_msg}")
            return False
        print(f"[抽象] '{value}' {self._name}验证通过")
        return True

# --- 运行演示 ---
if __name__ == "__main__":
    print("=" * 40)
    print("复制粘贴编程 反模式演示")
    print("=" * 40 + "\n")

    print("--- 反模式: 复制粘贴 ---")
    validate_email("test@example")
    validate_email("bad-email")
    validate_age("25")
    validate_age("-1")
    validate_name("Alice")
    validate_name("A")
    print()

    print("--- 正确做法: 抽象通用方案 ---")
    v_email = Validator("邮箱", lambda v: "@" in v, "验证失败: 缺少@")
    v_age = Validator("年龄", lambda v: 0 <= int(v) <= 150, "验证失败: 范围不对")
    v_name = Validator("名称", lambda v: len(v) >= 2, "验证失败: 太短")

    v_email.validate("test@example")
    v_age.validate("25")
    v_name.validate("Alice")

    print("\n关键：复制代码容易遗漏修改点")
    print("抽象后一处修改，所有验证受益")
