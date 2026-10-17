import json
import requests
from api_spec import BASE_URL, API_SPEC
from runner import run_all
from analyzer import analyze_failures
from report import generate_report


def check_server():
    """检查被测服务是否在运行。"""
    try:
        s = requests.Session()
        s.trust_env = False
        s.get(BASE_URL + "/users/1", timeout=3)
    except requests.RequestException:
        print("连接不上被测服务，请先运行 server.py")
        raise SystemExit(1)


def run_tests(spec=None, show_bugs=True, report_path="测试报告.xlsx"):
    check_server()

    with open("cases.json", encoding="utf-8") as f:
        cases = json.load(f)

    results = run_all(cases)
    failed = [r for r in results if r["result"] != "通过"]

    print(f"共 {len(results)} 条，通过 {len(results) - len(failed)} 条，"
          f"未通过 {len(failed)} 条\n")

    print("AI 正在分析失败原因，请稍等……\n")
    analysis = analyze_failures(failed, spec or API_SPEC)

    for r in failed:
        a = analysis.get(r["id"], {})
        r["category"] = a.get("category", "未分析")
        r["reason"] = a.get("reason", "")
        r["suggestion"] = a.get("suggestion", "")
        print(f"[{r['category']}] {r['id']} {r['name']}")
        print(f"    预期 {r['expected_status']}，实际 {r['actual_status']}")
        print(f"    原因：{r['reason']}")
        print(f"    建议：{r['suggestion']}\n")

    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    generate_report(results, path=report_path, show_bugs=show_bugs)


if __name__ == "__main__":
    run_tests()

import report