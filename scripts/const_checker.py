#!/usr/bin/env python3
"""C++ Const 正确性检查工具"""

import sys
import re
from typing import List, Dict


class ConstChecker:
    """Const 正确性检查器"""

    def check_const_correctness(self, code: str) -> tuple[List[Dict], str]:
        """检查代码中的 const 正确性"""
        issues = []

        issues.extend(self._check_nonconst_pointers(code))
        issues.extend(self._check_missing_const(code))
        issues.extend(self._check_const_methods(code))
        issues.extend(self._check_value_params(code))

        report = self._generate_report(issues, code)
        return issues, report

    def _check_nonconst_pointers(self, code: str) -> List[Dict]:
        issues = []
        # 检查可能应该是 const 的指针参数
        pointer_param_pattern = re.compile(r'(void|\w+)\s+\*(\w+)\s*\(')
        for match in pointer_param_pattern.finditer(code):
            # 在函数参数中，检查非 const 指针
            issues.append({
                "type": "nonconst_pointer",
                "severity": "info",
                "message": f"函数参数使用非 const 指针: {match.group(1)}* {match.group(2)}",
                "suggestion": "如果不需要修改，考虑改为 const 指针",
                "location": match.group(0),
                "line": code[:match.start()].count('\n') + 1
            })
        return issues

    def _check_missing_const(self, code: str) -> List[Dict]:
        issues = []
        # 检查可能被 const 修饰的变量
        # 查找在声明后未被修改的变量
        var_decl_pattern = re.compile(r'(int|double|float|char|bool|string|auto)\s+(\w+)\s*=')
        for match in var_decl_pattern.finditer(code):
            var_name = match.group(2)
            # 简化检查：查找后续是否有修改操作
            rest_code = code[match.end():]
            # 排除赋值给同名变量的情况 (如 x = x + 1)
            if not re.search(rf'\b{var_name}\s*[\+\-\*/]=', rest_code[:200]):
                # 检查是否是函数参数
                before = code[:match.start()]
                last_paren = before.rfind('(')
                if last_paren != -1 and before[last_paren:].find(')') == -1:
                    continue  # 是函数参数的一部分，跳过

                issues.append({
                    "type": "missing_const",
                    "severity": "info",
                    "message": f"变量可能应该是 const: {var_name}",
                    "suggestion": "如果变量初始化后不会被修改，使用 const",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })
        return issues

    def _check_const_methods(self, code: str) -> List[Dict]:
        issues = []
        # 检查 getter 方法是否应该 const
        getter_pattern = re.compile(r'(const\s+)?(\w+)\s+get\w+\s*\([^)]*\)\s*\{[^}]*return\s+\w+')
        for match in getter_pattern.finditer(code):
            if not match.group(1):  # 没有 const
                issues.append({
                    "type": "nonconst_getter",
                    "severity": "info",
                    "message": f"Getter 方法应该 const: {match.group(2)} getXxx()",
                    "suggestion": "不修改成员变量的 getter 方法应声明为 const",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })
        return issues

    def _check_value_params(self, code: str) -> List[Dict]:
        issues = []
        # 检查大型对象是否应该使用 const 引用
        large_types = ['std::string', 'std::vector', 'std::map', 'std::set', 'std::unordered_map']
        for lt in large_types:
            pattern = re.compile(rf'{re.escape(lt)}\s+(\w+)\s*\(')
            for match in pattern.finditer(code):
                issues.append({
                    "type": "value_param",
                    "severity": "info",
                    "message": f"使用值传递大型对象: {lt} {match.group(1)}",
                    "suggestion": "考虑使用 const 引用传递",
                    "location": match.group(0),
                    "line": code[:match.start()].count('\n') + 1
                })
        return issues

    def _generate_report(self, issues: List[Dict], code: str) -> str:
        if not issues:
            return """# Const 正确性检查报告

结果: 未发现明显的 const 正确性问题！

建议:
- 尽可能使用 const（变量、参数、返回值）
- Getter 方法应声明为 const
- 使用 const 成员函数
- 对于大型对象，使用 const 引用传递
"""

        errors = [i for i in issues if i['severity'] == 'error']
        warnings = [i for i in issues if i['severity'] == 'warning']
        infos = [i for i in issues if i['severity'] == 'info']

        report = "# Const 正确性检查报告\n\n"
        report += f"检查结果: 发现 {len(issues)} 个可改进点\n"
        report += f"- 错误: {len(errors)}\n"
        report += f"- 警告: {len(warnings)}\n"
        report += f"- 信息: {len(infos)}\n\n---\n\n"

        if infos:
            report += "## 建议改进\n\n"
            for i, issue in enumerate(infos, 1):
                report += f"### {i}. {issue['message']}\n\n"
                if issue.get('line', 0) > 0:
                    report += f"位置: 第 {issue['line']} 行\n"
                report += f"建议: {issue['suggestion']}\n\n"

        report += "---\n\n"
        report += "## 总体建议\n\n"
        report += "1. **尽可能使用 const**: 让代码意图更清晰，帮助编译器优化\n"
        report += "2. **const 成员函数**: 不修改对象状态的成员函数应声明为 const\n"
        report += "3. **const 引用传递**: 大型对象使用 const 引用避免拷贝\n"
        report += "4. **const 正确性**: const 是最低权限原则的体现\n"
        report += "5. **使用 constexpr**: 编译期常量使用 constexpr\n"

        return report


def main():
    code = sys.stdin.read()
    checker = ConstChecker()
    _, report = checker.check_const_correctness(code)
    print(report)


if __name__ == "__main__":
    main()
