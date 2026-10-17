import json
from ai_client import client

SYSTEM_PROMPT = """你是一名资深测试开发工程师。
根据用户给出的接口规则，生成接口测试用例，只输出json，格式如下：
{"cases": [{"id": "TC001", "name": "用例名称", "method": "POST",
 "path": "/login", "body": {"username": "admin", "password": "123456"},
 "expected_status": 200}]}
要求：
1. path 必须是可直接请求的路径，{user_id}要替换成具体数字，
   GET 的查询参数直接拼在 path 里，例如 /products?page=1&size=10
2. GET 请求的 body 填 null
3. 每个接口都要覆盖：正常场景、边界值（最小值-1、最小值、最大值、最大值+1）、
   参数缺失、类型错误
4. 严格按照接口规则确定 expected_status，不要编造规则里没有的内容
5. id 从 TC001 开始连续编号"""


def generate_cases(spec):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(spec, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)["cases"]