import json
from ai_client import client
from api_spec import API_SPEC

SYSTEM_PROMPT = """你是资深测试开发工程师。下面给出接口规则和一批未通过的测试用例
（含请求、预期状态码、实际状态码、响应内容）。
请逐条判断：该用例的预期状态码，能否直接由接口规则明确推出？
只输出json：
{"analyses": [{"id": "TC011", "rule_defined": true, "reason": "...", "suggestion": "..."}]}
rule_defined：规则中有明确条文能推出该预期状态码填true；
规则没有提到该情况、预期是自行假设的填false。
reason 用一句话说明依据（引用接口规则），suggestion 用一句话给出建议。
不要判断是不是缺陷，只回答规则是否明确。"""


def analyze_failures(failed, spec=API_SPEC):
    """请求报错归环境问题；其余让AI判断规则是否明确，类别由代码决定。"""
    result = {}
    for c in failed:
        if c["result"] == "错误":
            result[c["id"]] = {
                "category": "环境问题",
                "reason": "请求未收到响应：" + str(c["response"])[:80],
                "suggestion": "检查被测服务是否启动、网络和端口是否正常",
            }

    to_analyze = [c for c in failed if c["result"] != "错误"]
    if not to_analyze:
        return result

    items = [{
        "id": c["id"], "name": c["name"], "method": c["method"],
        "path": c["path"], "body": c["body"],
        "expected_status": c["expected_status"],
        "actual_status": c["actual_status"],
        "response": str(c["response"])[:200],
    } for c in to_analyze]

    payload = {"api_spec": spec, "failed_cases": items}
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
    )
    analyses = json.loads(response.choices[0].message.content)["analyses"]
    by_id = {c["id"]: c for c in to_analyze}

    for a in analyses:
        c = by_id.get(a["id"])
        if not c:
            continue
        # 类别由代码按固定规则决定，不交给AI
        if c["actual_status"] >= 500 or a.get("rule_defined") is True:
            a["category"] = "接口缺陷"
        else:
            a["category"] = "用例预期不合理"
        if c["actual_status"] >= 500:
            a["suggestion"] = "服务端出现500异常，需修复代码，非法输入应返回4xx而不是崩溃"
        result[a["id"]] = a
    return result