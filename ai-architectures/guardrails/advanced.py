"""Guardrails 进阶示例：内容安全、PII 保护与格式强制

展示三种护栏类型及其失败处理策略：
- 内容安全护栏：拦截有害内容
- PII 保护护栏：检测并脱敏个人信息
- 格式强制护栏：确保 JSON 输出包含必填字段
- 失败处理：log（记录）/ block（阻断）/ sanitize（脱敏替换）
"""


class ContentSafetyGuard:
    """内容安全护栏——拦截有害内容，策略为 block"""

    HARMFUL = ["制造武器", "危险药物配方", "网络入侵方法"]

    def check(self, response):
        for word in self.HARMFUL:
            if word in response:
                return "block", f"有害内容拦截: 含'{word}'"
        return "pass", "内容安全"


class PIIGuard:
    """PII 保护护栏——检测个人隐私信息，策略为 sanitize（脱敏）"""

    PII_PATTERNS = {
        "手机号": (r"\d{11}", "138****5678"),
        "身份证号": (r"\d{17}[\dX]", "3301**********1234"),
        "邮箱": (r"@[\w.]+", "@***.com"),
    }

    def check(self, response):
        import re
        sanitized = response
        found = []
        for label, (pattern, mask) in self.PII_PATTERNS.items():
            matches = re.findall(pattern, response)
            if matches:
                found.append(label)
                sanitized = re.sub(pattern, mask, sanitized)
        if found:
            return "sanitize", f"脱敏: {', '.join(found)}", sanitized
        return "pass", "无 PII", sanitized


class FormatGuard:
    """格式护栏——确保 JSON 输出有必填字段，策略为 block"""

    REQUIRED_FIELDS = ["answer", "confidence"]

    def check(self, response):
        try:
            import json
            data = json.loads(response)
        except (json.JSONDecodeError, TypeError):
            return "block", "格式拦截: 不是合法 JSON"
        missing = [f for f in self.REQUIRED_FIELDS if f not in data]
        if missing:
            return "block", f"格式拦截: 缺少必填字段 {missing}"
        return "pass", "格式合规"


class AdvancedGuardrailsSystem:
    """进阶护栏系统——根据策略决定 log/block/sanitize"""

    def __init__(self):
        self.guards = [ContentSafetyGuard(), PIIGuard(), FormatGuard()]
        self.log = []  # 拦截日志

    def process(self, query, response):
        result = {"original": response, "final": response, "actions": []}
        for guard in self.guards:
            action, msg, *rest = guard.check(result["final"])
            if action != "pass":
                self.log.append(f"[{guard.__class__.__name__}] {msg}")
                result["actions"].append(f"{action}: {msg}")
                if action == "block":
                    result["final"] = None
                    return result
                if action == "sanitize":
                    result["final"] = rest[0]
        return result


if __name__ == "__main__":
    print("=" * 50)
    print("Guardrails 进阶：安全 / PII / 格式三层防护")
    print("=" * 50 + "\n")

    system = AdvancedGuardrailsSystem()

    # --- 合法请求：通过所有护栏 ---
    good = '{"answer": "用 Cython 优化", "confidence": 0.85}'
    r = system.process("性能优化", good)
    print(f"【合法请求】最终输出: {r['final']}")

    # --- PII 脱敏：手机号被替换 ---
    pii = '{"answer": "联系 13812345678 咨询", "confidence": 0.7}'
    r = system.process("咨询", pii)
    print(f"【PII 脱敏】操作: {r['actions']}\n         最终: {r['final']}")

    # --- 格式拦截：缺少 confidence 字段 ---
    bad_fmt = '{"answer": "优化建议"}'
    r = system.process("优化", bad_fmt)
    print(f"【格式拦截】操作: {r['actions']}\n         最终: {r['final']}")

    # --- 内容拦截：有害内容被阻断 ---
    harmful = '{"answer": "制造武器步骤", "confidence": 0.9}'
    r = system.process("武器", harmful)
    print(f"【内容拦截】操作: {r['actions']}\n         最终: {r['final']}")
    print(f"\n拦截日志: {system.log}")
