---
description: "C++ 编码规范检查和代码审查工具。提供命名检查、内存安全分析、现代 C++ 建议等功能。"
---

# cpp-guidelines

## 使用方式

```
/cpp-guidelines naming <identifier> [variable|function|class|constant|namespace|member_variable]
/cpp-guidelines memory
/cpp-guidelines modern [cpp17]
/cpp-guidelines const
/cpp-guidelines include
/cpp-guidelines review [general|performance|safety|readability|modern]
/cpp-guidelines refactor [cpp17|cpp20|cpp23]
```

类别参数可省略，省略时 Claude 根据标识符风格自动推断。
代码分析命令（memory/modern/const/include）读取当前上下文中的 C++ 代码。

## 执行规则

| 命令 | 脚本 | 说明 |
|------|------|------|
| `naming <id> [cat]` | `scripts/naming_checker.py` | 若省略类别，先推断再检查 |
| `memory` | `scripts/memory_safety.py` | 从 stdin 或上下文读取代码 |
| `modern [std]` | `scripts/modern_cpp.py` | 默认 cpp17 |
| `const` | `scripts/const_checker.py` | 检查 const 正确性 |
| `include` | `scripts/include_guard_checker.py` | 检查头文件保护 |
| `review [focus]` | `scripts/code_review.py` | 默认 general |
| `refactor [std]` | `scripts/refactor_suggestion.py` | 默认 cpp17 |
