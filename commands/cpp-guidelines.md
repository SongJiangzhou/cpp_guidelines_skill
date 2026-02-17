---
description: "C++ 编码规范检查和代码审查工具。提供命名检查、内存安全分析、现代 C++ 建议等功能。"
---

# cpp-guidelines 命令

## 功能

- check naming - 检查命名规范
- check include - 检查头文件保护
- check memory - 内存安全分析
- check modern - 现代 C++ 建议
- check const - const 正确性检查
- review - 代码审查提示
- refactor - 重构建议提示

## 使用方式

```
/cpp-guidelines check naming <identifier> <category>
/cpp-guidelines check memory < code.cpp
/cpp-guidelines review [general|performance|safety|readability|modern]
/cpp-guidelines refactor [cpp11|cpp14|cpp17|cpp20|cpp23]
```

详细使用说明见 SKILL.md
