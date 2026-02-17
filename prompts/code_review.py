"""
C++ 代码审查提示模板
"""


class CodeReviewPrompt:
    """代码审查提示生成器"""

    @staticmethod
    def generate(focus: str = "general") -> str:
        """
        生成 C++ 代码审查提示模板

        参数:
            focus: 审查重点，可选值:
                  - general: 综合审查（默认）
                  - performance: 性能优化
                  - safety: 内存和类型安全
                  - readability: 可读性和维护性
                  - modern: 现代 C++ 特性使用

        返回:
            代码审查提示模板字符串
        """
        base_prompt = "请对以下 C++ 代码进行审查，关注以下方面：\n\n"

        if focus == "performance":
            base_prompt += """
**性能审查重点:**
1. 是否存在不必要的拷贝？应使用引用或移动语义吗？
2. 容器使用是否合适？是否需要 reserve？
3. 算法复杂度是否最优？
4. 是否有内联优化机会？
5. 循环是否可以优化？
"""
        elif focus == "safety":
            base_prompt += """
**安全性审查重点:**
1. 是否有内存泄漏风险？
2. 是否有悬空指针或野指针？
3. 是否有数组越界风险？
4. 异常安全性如何？是否符合 RAII？
5. 是否使用了不安全的 C 风格函数？
6. 类型转换是否安全？
"""
        elif focus == "readability":
            base_prompt += """
**可读性审查重点:**
1. 命名是否清晰、符合规范？
2. 代码结构是否清晰？
3. 是否有足够的注释？
4. 函数是否过长？是否需要拆分？
5. 是否遵循单一职责原则？
"""
        elif focus == "modern":
            base_prompt += """
**现代 C++ 审查重点:**
1. 是否使用了智能指针替代裸指针？
2. 是否使用了 auto 类型推导？
3. 是否使用了范围 for 循环？
4. 是否使用了 constexpr 和 consteval？
5. 是否使用了 std::optional 和 std::variant？
6. 是否可以使用 Concepts 约束模板？
"""
        else:  # general
            base_prompt += """
**综合审查清单:**

1. **正确性**
   - 逻辑是否正确？
   - 边界条件是否处理？
   - 是否有潜在的 bug？

2. **安全性**
   - 内存管理是否安全？
   - 是否有未定义行为？
   - 异常处理是否完善？

3. **性能**
   - 是否有性能瓶颈？
   - 数据结构选择是否合理？
   - 是否有优化空间？

4. **可维护性**
   - 代码是否清晰易懂？
   - 命名是否规范？
   - 结构是否合理？

5. **现代 C++**
   - 是否充分利用现代 C++ 特性？
   - 是否遵循最佳实践？
"""

        base_prompt += "\n请提供具体的改进建议和示例代码。"

        return base_prompt


def get_prompt() -> CodeReviewPrompt:
    """获取代码审查提示生成器实例"""
    return CodeReviewPrompt()


if __name__ == "__main__":
    import sys

    focus = sys.argv[1] if len(sys.argv) > 1 else "general"
    print(CodeReviewPrompt.generate(focus))
