---
name: cpp-style-guide
description: C++ 编码规范检查和最佳实践建议工具。用于：(1) 检查命名规范 (2) 检查头文件包含保护 (3) 内存安全分析 (4) 现代 C++ 写法建议 (5) const 正确性检查 (6) 代码审查支持
---

# C++ 编码规范检查

提供 C++ 代码规范检查、最佳实践建议和代码审查支持。

## 快速开始

所有检查功能通过 `scripts/` 目录下的 Python 脚本提供。直接运行脚本进行代码检查。

### 命名规范检查

```bash
python scripts/naming_checker.py <identifier> <category>
```

参数：
- `identifier`: 要检查的标识符名称
- `category`: 标识符类别 (variable/constant/function/class/namespace/member_variable/template_parameter/file_naming)

示例：
```bash
python scripts/naming_checker.py UserName class
python scripts/naming_checker.py MAX_SIZE constant
```

### 包含保护检查

```bash
python scripts/include_guard_checker.py <filepath>
```

示例：
```bash
python scripts/include_guard_checker.py my_header.h < code.cpp
```

### 内存安全分析

```bash
python scripts/memory_safety.py
```

从 stdin 读取 C++ 代码进行分析。

示例：
```bash
cat my_code.cpp | python scripts/memory_safety.py
```

### 现代 C++ 建议

```bash
python scripts/modern_cpp.py [cpp11|cpp14|cpp17|cpp20|cpp23]
```

从 stdin 读取代码，默认为 cpp17。

示例：
```bash
cat old_code.cpp | python scripts/modern_cpp.py cpp20
```

### Const 正确性检查

```bash
python scripts/const_checker.py
```

从 stdin 读取代码进行 const 检查。

示例：
```bash
cat my_code.cpp | python scripts/const_checker.py
```

## 提示模板 (Prompts)

### 代码审查提示

```bash
python scripts/code_review.py [general|performance|safety|readability|modern]
```

参数：
- `general`: 综合审查（默认）
- `performance`: 性能优化
- `safety`: 内存和类型安全
- `readability`: 可读性和维护性
- `modern`: 现代 C++ 特性使用

示例：
```bash
python scripts/code_review.py safety
python scripts/code_review.py performance
```

### 重构建议提示

```bash
python scripts/refactor_suggestion.py [cpp11|cpp14|cpp17|cpp20|cpp23]
```

参数：
- 目标 C++ 标准 (默认: cpp17)

示例：
```bash
python scripts/refactor_suggestion.py cpp20
python scripts/refactor_suggestion.py cpp11
```

## 详细功能

- **命名检查**: 验证标识符是否符合 C++ 命名规范
- **包含保护**: 检查头文件的 #ifndef/#define 保护
- **内存安全**: 检测裸指针、内存泄漏、悬空指针等问题
- **现代 C++**: 建议使用智能指针、auto、范围 for 等新特性
- **Const 检查**: 检查缺失的 const 声明

## 参考文档

- 命名规范: `references/naming_conventions.json`
- 最佳实践: `references/best_practices.json`
- C++ 标准特性: `references/cpp_standards.json`
- 设计模式: `references/design_patterns.json`
