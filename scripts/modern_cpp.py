#!/usr/bin/env python3
"""现代 C++ 写法建议工具"""

import sys
import re
from typing import List, Dict


class ModernCppSuggester:
    """现代 C++ 写法建议器"""

    def __init__(self, target_standard: str = "cpp17"):
        self.target_standard = target_standard
        self.version_order = ["cpp11", "cpp14", "cpp17", "cpp20", "cpp23"]
        self.target_index = self.version_order.index(target_standard) if target_standard in self.version_order else 2

    def suggest_modern_cpp(self, code: str) -> tuple[List[Dict], str]:
        """建议将代码升级为现代 C++ 写法"""
        suggestions = []

        suggestions.extend(self._check_auto(code))
        suggestions.extend(self._check_smart_pointers(code))
        suggestions.extend(self._check_range_for(code))
        suggestions.extend(self._check_nullptr(code))
        suggestions.extend(self._check_constexpr(code))
        suggestions.extend(self._check_lambda(code))
        suggestions.extend(self._check_struct_init(code))

        if self.target_index >= 2:  # C++17+
            suggestions.extend(self._check_std_optional(code))
            suggestions.extend(self._check_std_variant(code))

        if self.target_index >= 3:  # C++20+
            suggestions.extend(self._check_concepts(code))
            suggestions.extend(self._check_ranges(code))
            suggestions.extend(self._check_spaceship(code))

        report = self._generate_report(suggestions, code)
        return suggestions, report

    def _check_auto(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查冗长的类型声明
        iter_pattern = re.compile(r'std::vector<([^>]+)>::iterator')
        for match in iter_pattern.finditer(code):
            suggestions.append({
                "type": "auto_iterator",
                "severity": "info",
                "message": "使用冗长的迭代器类型",
                "original": match.group(0),
                "suggestion": "使用 auto 替代",
                "example": "auto it = container.begin();"
            })
        return suggestions

    def _check_smart_pointers(self, code: str) -> List[Dict]:
        suggestions = []
        new_pattern = re.compile(r'\bnew\s+\w+')
        for match in new_pattern.finditer(code):
            suggestions.append({
                "type": "raw_pointer",
                "severity": "warning",
                "message": "使用裸指针 new",
                "original": match.group(0),
                "suggestion": "使用 std::unique_ptr 或 std::shared_ptr",
                "example": "auto ptr = std::make_unique<Type>();"
            })
        return suggestions

    def _check_range_for(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查传统的 for 循环
        for_pattern = re.compile(r'for\s*\(\s*\w+\s+\w+\s*=\s*0\s*;.*<\s*\w+\.size\(\)\s*;.*\+\+\s*\)')
        for match in for_pattern.finditer(code):
            suggestions.append({
                "type": "range_for",
                "severity": "info",
                "message": "使用传统的 for 循环遍历容器",
                "original": match.group(0),
                "suggestion": "使用范围 for 循环",
                "example": "for (const auto& item : container) { ... }"
            })
        return suggestions

    def _check_nullptr(self, code: str) -> List[Dict]:
        suggestions = []
        null_pattern = re.compile(r'\bNULL\b')
        for match in null_pattern.finditer(code):
            suggestions.append({
                "type": "nullptr",
                "severity": "info",
                "message": "使用 NULL 代替空指针",
                "original": "NULL",
                "suggestion": "使用 nullptr",
                "example": "int* p = nullptr;"
            })
        return suggestions

    def _check_constexpr(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查可以用 constexpr 的 const
        const_func_pattern = re.compile(r'const\s+(\w+)\s+(\w+)\s*\([^)]*\)\s*\{')
        for match in const_func_pattern.finditer(code):
            if self.target_index >= 0:  # C++11
                suggestions.append({
                    "type": "constexpr",
                    "severity": "info",
                    "message": f"函数可以声明为 constexpr",
                    "original": match.group(0),
                    "suggestion": "如果函数足够简单，使用 constexpr",
                    "example": f"constexpr {match.group(1)} {match.group(2)}(...) {{ ... }}"
                })
        return suggestions

    def _check_lambda(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查 std::bind
        bind_pattern = re.compile(r'std::bind\s*\(')
        for match in bind_pattern.finditer(code):
            suggestions.append({
                "type": "lambda",
                "severity": "info",
                "message": "使用 std::bind",
                "original": "std::bind(...)",
                "suggestion": "考虑使用 lambda 表达式（更清晰）",
                "example": "auto f = [&](auto arg) { return obj.method(arg); };"
            })
        return suggestions

    def _check_struct_init(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查 C 风格结构体初始化
        struct_init_pattern = re.compile(r'(\w+)\s+\w+\s*=\s*\{\s*[^}]*\};')
        for match in struct_init_pattern.finditer(code):
            # 排除已经使用 std:: 的情况
            if not match.group(1).startswith('std::'):
                suggestions.append({
                    "type": "brace_init",
                    "severity": "info",
                    "message": "使用 C++11 花括号初始化",
                    "original": match.group(0),
                    "suggestion": "这是正确的现代 C++ 用法，保持使用",
                    "example": "Type name = { ... };"
                })
        return suggestions

    def _check_std_optional(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查可能返回空值的函数
        null_return_pattern = re.compile(r'return\s+nullptr\s*;')
        for match in null_return_pattern.finditer(code):
            suggestions.append({
                "type": "std_optional",
                "severity": "info",
                "message": "返回 nullptr 表示无值",
                "original": "return nullptr;",
                "suggestion": "考虑使用 std::optional（C++17）",
                "example": "std::optional<Type> getValue();"
            })
        return suggestions

    def _check_std_variant(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查联合体使用
        union_pattern = re.compile(r'union\s+\w+\s*\{')
        for match in union_pattern.finditer(code):
            suggestions.append({
                "type": "std_variant",
                "severity": "info",
                "message": "使用 union",
                "original": "union { ... }",
                "suggestion": "考虑使用 std::variant（C++17）更安全",
                "example": "std::variant<Type1, Type2> v;"
            })
        return suggestions

    def _check_concepts(self, code: str) -> List[Dict]:
        suggestions = []
        if self.target_index >= 3:
            # C++20 concepts - 简化检查
            template_pattern = re.compile(r'template\s*<\s*typename\s+(\w+)\s*>')
            for match in template_pattern.finditer(code):
                suggestions.append({
                    "type": "concepts",
                    "severity": "info",
                    "message": "使用 typename 约束模板参数",
                    "original": f"template <typename {match.group(1)}>",
                    "suggestion": "考虑使用 C++20 concepts 约束",
                    "example": f"template <std::integral T>"
                })
        return suggestions

    def _check_ranges(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查 std::sort
        sort_pattern = re.compile(r'std::sort\s*\(')
        for match in sort_pattern.finditer(code):
            if self.target_index >= 3:
                suggestions.append({
                    "type": "ranges",
                    "severity": "info",
                    "message": "使用 std::sort",
                    "original": "std::sort(begin, end, comp)",
                    "suggestion": "考虑使用 C++20 ranges",
                    "example": "std::ranges::sort(v);"
                })
        return suggestions

    def _check_spaceship(self, code: str) -> List[Dict]:
        suggestions = []
        # 检查比较运算符
        if self.target_index >= 3:
            cmp_pattern = re.compile(r'(operator\s*==|operator\s*!=|operator\s*<|operator\s*>)')
            matches = cmp_pattern.findall(code)
            if len(matches) > 1:
                suggestions.append({
                    "type": "spaceship",
                    "severity": "info",
                    "message": "定义多个比较运算符",
                    "original": "operator==, operator<, ...",
                    "suggestion": "考虑使用 C++20 三路比较运算符 <=>",
                    "example": "auto operator<=>(const Type&, const Type&) = default;"
                })
        return suggestions

    def _generate_report(self, suggestions: List[Dict], code: str) -> str:
        if not suggestions:
            return f"""# 现代 C++ 建议报告 (目标: {self.target_standard})

结果: 代码已经符合现代 C++ 风格！

建议:
- 继续保持良好的现代 C++ 编码习惯
- 定期查看 C++ 标准新特性
- 使用 clang-tidy 进行自动化检查
"""

        report = f"# 现代 C++ 建议报告 (目标: {self.target_standard})\n\n"
        report += f"发现 {len(suggestions)} 个可改进点\n\n---\n\n"

        for i, sug in enumerate(suggestions, 1):
            report += f"## {i}. {sug['message']}\n\n"
            report += f"原始代码: `{sug['original']}`\n"
            report += f"建议: {sug['suggestion']}\n"
            report += f"示例: ```cpp\n{sug['example']}\n```\n\n"

        report += "---\n\n"
        report += "## 总体建议\n\n"
        report += "1. **优先使用 auto**: 减少冗长的类型声明\n"
        report += "2. **使用智能指针**: unique_ptr/shared_ptr 替代裸指针\n"
        report += "3. **范围 for 循环**: 更简洁安全\n"
        report += "4. **nullptr**: 替代 NULL\n"
        report += "5. **lambda 表达式**: 比 std::bind 更清晰\n"
        if self.target_index >= 2:
            report += "6. **std::optional**: 处理可能无值的情况\n"
            report += "7. **std::variant**: 类型安全的联合体\n"
        if self.target_index >= 3:
            report += "8. **C++20 Concepts**: 更清晰的模板约束\n"
            report += "9. **Ranges**: 更现代化的算法使用\n"
            report += "10. **三路比较**: <=> 简化比较运算符\n"

        return report


def main():
    target = "cpp17"
    if len(sys.argv) > 1:
        target = sys.argv[1].lower()

    code = sys.stdin.read()
    suggester = ModernCppSuggester(target)
    _, report = suggester.suggest_modern_cpp(code)
    print(report)


if __name__ == "__main__":
    main()
