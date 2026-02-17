# C++ 编码规范快速参考

## 命名检查

```bash
python scripts/naming_checker.py <identifier> <category>
```

**类别**: variable, constant, function, class, namespace, member_variable, template_parameter, file_naming

## 包含保护检查

```bash
python scripts/include_guard_checker.py <filepath>
```

## 内存安全分析

```bash
cat code.cpp | python scripts/memory_safety.py
```

**检测问题**:
- 裸指针 (raw pointers)
- 内存泄漏 (memory leaks)
- 悬空指针 (dangling pointers)
- 不安全函数 (strcpy, sprintf 等)

## 现代 C++ 建议

```bash
cat code.cpp | python scripts/modern_cpp.py [cpp11|cpp14|cpp17|cpp20|cpp23]
```

**建议特性**:
- 智能指针 (unique_ptr, shared_ptr)
- auto 类型推导
- 范围 for 循环
- std::optional, std::variant

## Const 正确性检查

```bash
cat code.cpp | python scripts/const_checker.py
```

## 代码审查提示

```bash
python scripts/code_review.py [general|performance|safety|readability|modern]
```

## 重构建议

```bash
python scripts/refactor_suggestion.py [cpp11|cpp14|cpp17|cpp20|cpp23]
```
