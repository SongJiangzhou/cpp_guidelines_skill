---
name: cpp-guidelines
description: C++ 编码规范检查和代码审查工具。使用方式: /cpp-guidelines [功能] [参数]
---

# C++ 编码规范检查

提供 C++ 代码规范检查、最佳实践建议和代码审查支持。

## 快速开始

### 命令行使用

```bash
# 命名检查
python scripts/naming_checker.py <identifier> <category>

# 内存安全分析
cat code.cpp | python scripts/memory_safety.py

# 现代 C++ 建议
cat code.cpp | python scripts/modern_cpp.py cpp20

# 代码审查提示
python scripts/code_review.py safety

# 重构建议
python scripts/refactor_suggestion.py cpp17
```

### 通过命令调用

```
/cpp-guidelines check naming <identifier> <category>
/cpp-guidelines check memory < code.cpp
/cpp-guidelines review safety
/cpp-guidelines refactor cpp20
```

详细使用说明见 `commands/cpp-guidelines.md`

## 功能列表

| 功能 | 脚本 | 说明 |
|------|------|------|
| 命名检查 | naming_checker.py | 验证标识符命名规范 |
| 包含保护 | include_guard_checker.py | 检查头文件保护宏 |
| 内存安全 | memory_safety.py | 检测内存泄漏、悬空指针等 |
| 现代 C++ | modern_cpp.py | 建议使用新特性 |
| Const 检查 | const_checker.py | 检查 const 正确性 |
| 代码审查 | code_review.py | 生成审查提示 |
| 重构建议 | refactor_suggestion.py | 生成重构提示 |

## 参考文档

- 详细规范: `references/quick_reference.md`
- 命名规范: `assets/naming_conventions.json`
- 最佳实践: `assets/best_practices.json`
- C++ 标准: `assets/cpp_standards.json`
- 设计模式: `assets/design_patterns.json`
