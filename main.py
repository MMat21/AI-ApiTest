import argparse
import json
from api_spec import API_SPEC
from generator import generate_cases
from run_tests import run_tests


def save_cases(cases):
    with open("cases.json", "w", encoding="utf-8") as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)
    print(f"已生成 {len(cases)} 条用例，已保存到 cases.json")


def generate():
    """调用 AI 生成测试用例，保存到 cases.json。"""
    save_cases(generate_cases(API_SPEC))


def custom():
    """用户输入自己的测试要求，AI 生成用例并执行。"""
    print("可测试的接口：")
    for i, api in enumerate(API_SPEC, start=1):
        print(f"  {i}. {api['name']}  {api['method']} {api['path']}")

    choice = input("请选择接口编号：").strip()
    if not choice.isdigit() or not 1 <= int(choice) <= len(API_SPEC):
        print("编号不正确。")
        return

    requirement = input("请输入测试要求（例如：商品数量不能大于10，超出返回400）：").strip()
    if not requirement:
        print("测试要求不能为空！")
        return

    api = dict(API_SPEC[int(choice) - 1])
    api["rules"] = requirement  # 用你的要求替换原来的规则
    spec = [api]

    print("\nAI 正在生成用例，请稍等……")
    save_cases(generate_cases(spec))
    run_tests(spec=spec, show_bugs=False, report_path="测试报告_自定义.xlsx")


def main():
    parser = argparse.ArgumentParser(description="AI 接口自动化测试助手")
    parser.add_argument(
        "command", nargs="?", default="all",
        choices=["generate", "run", "all", "custom"],
        help="generate=只生成用例，run=只执行并出报告，"
             "all=全部（默认），custom=输入自己的测试要求",
    )
    args = parser.parse_args()

    if args.command in ("generate", "all"):
        generate()
    if args.command in ("run", "all"):
        run_tests()
    if args.command == "custom":
        custom()


if __name__ == "__main__":
    main()