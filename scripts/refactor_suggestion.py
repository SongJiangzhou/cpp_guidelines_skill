"""
C++ 代码重构建议提示模板
"""


class RefactorSuggestionPrompt:
    """代码重构建议提示生成器"""

    # C++ 标准特性定义
    STANDARD_FEATURES = {
        "cpp11": [
            "auto 类型推导",
            "nullptr",
            "范围 for 循环",
            "智能指针 (unique_ptr, shared_ptr)",
            "lambda 表达式",
            "右值引用和移动语义",
        ],
        "cpp14": [
            "泛型 lambda",
            "返回值类型推导",
            "std::make_unique",
            "二进制字面量",
        ],
        "cpp17": [
            "结构化绑定",
            "if/switch 初始化语句",
            "constexpr if",
            "std::optional",
            "std::string_view",
            "折叠表达式",
        ],
        "cpp20": [
            "Concepts (概念)",
            "Ranges (区间)",
            "Coroutines (协程)",
            "三路比较运算符 (<=>)",
            "指定初始化器",
            "std::span",
        ],
        "cpp23": [
            "std::expected",
            "std::print",
            "if consteval",
            "多维下标运算符",
            "推导 this",
        ],
    }

    @staticmethod
    def generate(target_standard: str = "cpp17") -> str:
        """
        生成代码重构建议提示模板

        参数:
            target_standard: 目标 C++ 标准
                            - cpp11: C++11
                            - cpp14: C++14
                            - cpp17: C++17
                            - cpp20: C++20
                            - cpp23: C++23

        返回:
            代码重构建议提示模板字符串
        """
        prompt = f"请将以下 C++ 代码重构为使用 {target_standard.upper()} 标准。\n\n"
        prompt += f"**可以使用的 {target_standard.upper()} 特性:**\n"

        # 包含目标及之前的所有标准特性
        standards = ["cpp11", "cpp14", "cpp17", "cpp20", "cpp23"]
        target_index = standards.index(target_standard)

        for std in standards[:target_index + 1]:
            if std in RefactorSuggestionPrompt.STANDARD_FEATURES:
                prompt += f"\n{std.upper()} 特性:\n"
                for feature in RefactorSuggestionPrompt.STANDARD_FEATURES[std]:
                    prompt += f"  • {feature}\n"

        prompt += "\n**重构要求:**\n"
        prompt += "1. 使用现代 C++ 特性替代旧式写法\n"
        prompt += "2. 提高代码可读性和安全性\n"
        prompt += "3. 保持功能不变\n"
        prompt += "4. 解释每个重构点的理由\n"
        prompt += "5. 提供前后对比代码\n"

        return prompt


def get_prompt() -> RefactorSuggestionPrompt:
    """获取代码重构建议提示生成器实例"""
    return RefactorSuggestionPrompt()


if __name__ == "__main__":
    import sys

    target = sys.argv[1] if len(sys.argv) > 1 else "cpp17"
    print(RefactorSuggestionPrompt.generate(target))
