"""Guardrails（护栏）最小化示例

演示 GuardrailsSystem 在 LLM 的输入和输出端设置验证关卡：
- InputGuard: 拒绝不当查询
- OutputGuard: 检查响应格式与安全性
- BusinessGuard: 强制业务规则（如禁止泄露内部定价）
"""


class InputGuard:
    """输入护栏——拒绝不当查询进入 LLM"""

    BLOCKED = ["暴力", "非法", "攻击"]

    def check(self, query):
        for word in self.BLOCKED:
            if word in query:
                return False, f"输入拦截: 查询包含不当内容'{word}'"
        return True, "输入验证通过"


class OutputGuard:
    """输出护栏——检查 LLM 响应的格式与安全性"""

    def check(self, response):
        # 格式检查：响应必须以结论开头
        if not response.startswith("结论:"):
            return False, "输出拦截: 响应缺少'结论:'前缀，格式不符"
        return True, "输出验证通过"


class BusinessGuard:
    """业务护栏——强制业务规则，如禁止泄露内部定价"""

    def check(self, response):
        if "内部定价" in response or "成本价" in response:
            return False, "业务拦截: 响应泄露了内部定价信息"
        return True, "业务规则验证通过"


class GuardrailsSystem:
    """护栏系统——请求依次通过输入→输出→业务三层验证"""

    def __init__(self):
        self.guards = [InputGuard(), OutputGuard(), BusinessGuard()]

    def process(self, query, response):
        """依次检查三层护栏，任一拦截则阻断"""
        for guard in self.guards:
            if isinstance(guard, InputGuard):
                ok, msg = guard.check(query)
            else:
                ok, msg = guard.check(response)
            if not ok:
                return {"status": "blocked", "reason": msg}
        return {"status": "approved", "reason": "所有护栏验证通过"}


if __name__ == "__main__":
    print("=" * 45)
    print("Guardrails 护栏系统演示")
    print("=" * 45 + "\n")

    system = GuardrailsSystem()

    # --- 合法请求：通过所有护栏 ---
    result = system.process("Python 性能优化建议", "结论: 使用 Cython 可提升计算速度")
    print(f"【合法请求】{result['status']} — {result['reason']}")

    # --- 非法请求：被输入护栏拦截 ---
    result = system.process("如何发起暴力攻击", "结论: 不提供此类信息")
    print(f"【非法请求】{result['status']} — {result['reason']}")
