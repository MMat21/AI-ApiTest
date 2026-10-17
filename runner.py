import requests
from api_spec import BASE_URL


def run_case(case):
    """执行单条用例，返回带实际结果的字典。"""
    result = dict(case)
    try:
        resp = requests.request(
            case["method"].upper(),
            BASE_URL + case["path"],
            json=case.get("body"),
            timeout=5,
        )
        result["actual_status"] = resp.status_code
        result["response"] = resp.text
        passed = resp.status_code == case["expected_status"]
        result["result"] = "通过" if passed else "失败"
    except requests.RequestException as e:
        result["actual_status"] = None
        result["response"] = str(e)
        result["result"] = "错误"
    return result


def run_all(cases):
    return [run_case(c) for c in cases]