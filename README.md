# C++ Core Guidelines Skill

[English](#english) | [中文](#中文)

---

## 中文

基于 [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/) 的 Claude Code Skill，用于代码审查、现代化重构和最佳实践指导。

### ✨ 功能特性

- 📋 **代码审查**：基于 Core Guidelines 的系统化审查，识别内存安全、类型安全、并发安全问题
- 🚀 **代码现代化**：将传统 C++ (C++03/11) 升级到现代 C++ (C++17/20)
- 💡 **最佳实践**：编写新代码时提供 RAII、智能指针、接口设计等指导
- 🔧 **自动化工具**：4 个实用脚本帮助自动检测违规和现代化代码

### 📦 安装

1. 下载 `cpp-guidelines.skill` 文件
2. 在 Claude Code 中安装该 Skill
3. Skill 将在以下情况自动触发：
   - 处理 C++ 代码文件时
   - 询问 C++ 最佳实践时
   - 请求代码审查时
   - 需要现代化旧代码时

### 📚 包含内容

#### 参考文档 (references/)

| 文档 | 大小 | 说明 |
|------|------|------|
| `guidelines_quick_ref.md` | 21KB | 按主题分类的关键规则快速参考（400+ 规则） |
| `code_review_checklist.md` | 13KB | 系统化的代码审查检查清单 |
| `modernization_patterns.md` | 23KB | 27 种现代化模式（传统 → 现代 C++） |
| `common_violations.md` | 19KB | 18 种最常见违规和修复示例 |

#### 工具脚本 (scripts/)

| 脚本 | 功能 | 示例 |
|------|------|------|
| `detect_violations.py` | 检测常见违规 | `python scripts/detect_violations.py src/` |
| `modernize_code.py` | 自动化现代化 | `python scripts/modernize_code.py main.cpp --backup` |
| `generate_report.py` | 生成审查报告 | `python scripts/generate_report.py src/ -o report.md` |
| `run_clang_tidy.py` | Clang-Tidy 集成 | `python scripts/run_clang_tidy.py src/` |

查看 [scripts/README.md](scripts/README.md) 了解详细用法。

### 🚀 快速开始

#### 代码审查

```bash
# 快速检测
python scripts/detect_violations.py src/ --recursive

# 生成详细报告
python scripts/generate_report.py src/ -r -o review.md
```

#### 代码现代化

```bash
# 预览更改
python scripts/modernize_code.py old_code.cpp --dry-run

# 应用更改（创建备份）
python scripts/modernize_code.py old_code.cpp --backup
```

#### 专业分析

```bash
# 运行 clang-tidy（需要预先安装）
python scripts/run_clang_tidy.py src/
```

### 📖 使用示例

#### 示例 1：代码审查

```
用户：帮我审查这个 C++ 类
Claude：[使用 code_review_checklist.md 进行系统化审查]
        发现 3 个严重问题：
        1. 直接使用 new/delete (R.11)
        2. 缺少移动语义 (C.21)
        3. 析构函数未标记 noexcept (C.36)
```

#### 示例 2：现代化代码

```
用户：将这段 C++03 代码升级到 C++17
Claude：[应用 modernization_patterns.md 中的模式]
        已应用以下现代化转换：
        - NULL → nullptr (ES.47)
        - typedef → using (T.43)
        - 裸指针 → unique_ptr (R.11)
        - 手写循环 → 范围 for (ES.71)
```

#### 示例 3：规则查询

```
用户：R.11 规则是什么意思？
Claude：[查阅 guidelines_quick_ref.md]
        R.11: 避免直接使用 new 和 delete

        原因：容易忘记释放、异常不安全

        推荐做法：
        - 使用 make_unique<T>()
        - 使用 make_shared<T>()
        - 使用标准容器
```

### 🔍 检测项目

- ✅ 直接使用 new/delete (R.11)
- ✅ NULL 而非 nullptr (ES.47)
- ✅ C 风格类型转换 (ES.49)
- ✅ typedef 而非 using (T.43)
- ✅ 缺少 const (Con.2)
- ✅ 手写循环 (ES.71)
- ✅ 裸指针返回值 (I.11)
- ✅ C 风格数组 (SL.con.1)
- ✅ 五法则不完整 (C.21)
- ✅ 资源泄漏 (P.8, R.1)
- ✅ 数据竞争 (CP.2)
- ✅ 异常安全 (E.6)

### 📋 工作流建议

**完整的代码审查流程：**

```bash
# 1. 快速扫描
python scripts/detect_violations.py src/ -r

# 2. 生成报告
python scripts/generate_report.py src/ -r -o report.md

# 3. 自动修复
python scripts/modernize_code.py src/*.cpp --backup

# 4. 深度分析
python scripts/run_clang_tidy.py src/
```

### 🛠️ 依赖

- Python 3.6+（脚本）
- clang-tidy（可选，用于 `run_clang_tidy.py`）

所有脚本使用 Python 标准库，无需额外安装包。

### 📄 许可

MIT License - 详见 [LICENSE](LICENSE)

### 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 📚 相关资源

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- [Claude Code](https://claude.com/claude-code)
- [Clang-Tidy](https://clang.llvm.org/extra/clang-tidy/)

---

## English

A Claude Code Skill based on [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/) for code review, modernization, and best practices guidance.

### ✨ Features

- 📋 **Code Review**: Systematic review based on Core Guidelines, detecting memory safety, type safety, and concurrency issues
- 🚀 **Code Modernization**: Upgrade legacy C++ (C++03/11) to modern C++ (C++17/20)
- 💡 **Best Practices**: Guidance on RAII, smart pointers, interface design when writing new code
- 🔧 **Automation Tools**: 4 utility scripts for automatic violation detection and code modernization

### 📦 Installation

1. Download `cpp-guidelines.skill` file
2. Install the Skill in Claude Code
3. The Skill will automatically trigger when:
   - Working with C++ code files
   - Asking about C++ best practices
   - Requesting code reviews
   - Modernizing legacy code

### 📚 Contents

#### Reference Documents (references/)

| Document | Size | Description |
|----------|------|-------------|
| `guidelines_quick_ref.md` | 21KB | Quick reference of key rules organized by topic (400+ rules) |
| `code_review_checklist.md` | 13KB | Systematic code review checklist |
| `modernization_patterns.md` | 23KB | 27 modernization patterns (legacy → modern C++) |
| `common_violations.md` | 19KB | 18 most common violations with fix examples |

#### Utility Scripts (scripts/)

| Script | Function | Example |
|--------|----------|---------|
| `detect_violations.py` | Detect common violations | `python scripts/detect_violations.py src/` |
| `modernize_code.py` | Automated modernization | `python scripts/modernize_code.py main.cpp --backup` |
| `generate_report.py` | Generate review reports | `python scripts/generate_report.py src/ -o report.md` |
| `run_clang_tidy.py` | Clang-Tidy integration | `python scripts/run_clang_tidy.py src/` |

See [scripts/README.md](scripts/README.md) for detailed usage.

### 🚀 Quick Start

#### Code Review

```bash
# Quick detection
python scripts/detect_violations.py src/ --recursive

# Generate detailed report
python scripts/generate_report.py src/ -r -o review.md
```

#### Code Modernization

```bash
# Preview changes
python scripts/modernize_code.py old_code.cpp --dry-run

# Apply changes (with backup)
python scripts/modernize_code.py old_code.cpp --backup
```

#### Professional Analysis

```bash
# Run clang-tidy (requires installation)
python scripts/run_clang_tidy.py src/
```

### 🔍 Detection Items

- ✅ Direct use of new/delete (R.11)
- ✅ NULL instead of nullptr (ES.47)
- ✅ C-style casts (ES.49)
- ✅ typedef instead of using (T.43)
- ✅ Missing const (Con.2)
- ✅ Manual loops (ES.71)
- ✅ Raw pointer returns (I.11)
- ✅ C-style arrays (SL.con.1)
- ✅ Incomplete Rule of Five (C.21)
- ✅ Resource leaks (P.8, R.1)
- ✅ Data races (CP.2)
- ✅ Exception safety (E.6)

### 🛠️ Dependencies

- Python 3.6+ (for scripts)
- clang-tidy (optional, for `run_clang_tidy.py`)

All scripts use Python standard library, no additional packages required.

### 📄 License

MIT License - see [LICENSE](LICENSE)

### 🤝 Contributing

Issues and Pull Requests are welcome!

### 📚 Related Resources

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
- [Claude Code](https://claude.com/claude-code)
- [Clang-Tidy](https://clang.llvm.org/extra/clang-tidy/)
