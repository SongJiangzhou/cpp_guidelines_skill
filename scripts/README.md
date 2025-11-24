# C++ Core Guidelines 工具脚本

本目录包含多个实用脚本，用于自动化 C++ 代码审查和现代化。

## 脚本概览

| 脚本 | 功能 | 适用场景 |
|------|------|----------|
| `detect_violations.py` | 检测常见违规 | 快速扫描代码问题 |
| `modernize_code.py` | 自动化现代化 | 升级代码到现代 C++ |
| `generate_report.py` | 生成审查报告 | 创建详细的分析报告 |
| `run_clang_tidy.py` | 运行 clang-tidy | 专业的静态分析 |

## 1. detect_violations.py

### 功能
检测常见的 C++ Core Guidelines 违规，包括：
- ✅ 直接使用 new/delete (R.11)
- ✅ 使用 NULL 而非 nullptr (ES.47)
- ✅ C 风格类型转换 (ES.49)
- ✅ typedef 而非 using (T.43)
- ✅ 缺少 const (Con.2)
- ✅ 手写循环 (ES.71)
- ✅ 裸指针返回值 (I.11)
- ✅ C 风格数组 (SL.con.1)

### 用法

```bash
# 检测单个文件
python detect_violations.py main.cpp

# 检测目录（递归）
python detect_violations.py src/ --recursive

# 或使用短选项
python detect_violations.py src/ -r
```

### 输出示例

```
检测到 5 个潜在问题:

================================================================================

🔴 严重 - main.cpp:15
   违反规则: R.11
   问题: 直接使用 'new'，应使用智能指针
   代码: Widget* w = new Widget();
   建议: 使用 std::make_unique<T>() 或 std::make_shared<T>()

🟡 重要 - main.cpp:23
   违反规则: ES.47
   问题: 使用 NULL，应使用 nullptr
   代码: int* ptr = NULL;
   建议: 替换为 nullptr

================================================================================

总计:
  🔴 严重问题: 2
  🟡 重要问题: 2
  🟢 改进建议: 1
```

## 2. modernize_code.py

### 功能
自动应用现代化转换：
- ✅ NULL → nullptr
- ✅ typedef → using
- ✅ 添加 explicit 到单参数构造函数
- ✅ 指针初始化 0 → nullptr

### 用法

```bash
# 预览更改（不修改文件）
python modernize_code.py main.cpp --dry-run

# 应用更改
python modernize_code.py main.cpp

# 应用更改并创建备份
python modernize_code.py main.cpp --backup
```

### 输出示例

```
📝 main.cpp:
  第 15 行: NULL → nullptr (ES.47)
    - int* ptr = NULL;
    + int* ptr = nullptr;

  第 23 行: typedef → using (T.43)
    - typedef std::vector<int> IntVec;
    + using IntVec = std::vector<int>;

  备份已创建: main.cpp.bak
  ✓ 文件已更新

✅ 现代化完成！
```

## 3. generate_report.py

### 功能
生成详细的代码审查报告，支持多种格式：
- Markdown (.md)
- HTML (.html)
- JSON (.json)

报告包含：
- 违规统计和图表
- 按严重程度分类
- 按规则分类
- 详细的问题列表
- 修复建议优先级

### 用法

```bash
# 生成 Markdown 报告
python generate_report.py src/ --output report.md

# 生成 HTML 报告
python generate_report.py src/ --output report.html --format html

# 生成 JSON 报告
python generate_report.py src/ --output report.json --format json

# 递归扫描
python generate_report.py src/ --recursive --output report.md
```

### 报告示例

生成的 Markdown 报告包含：

```markdown
# C++ Core Guidelines 代码审查报告

**生成时间:** 2025-01-15 14:30:00
**检测文件数:** 25
**发现问题数:** 47

## 📊 执行摘要

| 严重程度 | 数量 | 占比 |
|---------|------|------|
| 🔴 严重 | 12 | 25.5% |
| 🟡 重要 | 20 | 42.6% |
| 🟢 建议 | 15 | 31.9% |

## 📋 按规则统计

| 规则 | 数量 | 说明 |
|------|------|------|
| R.11 | 12 | 避免直接使用 new/delete |
| ES.47 | 8 | 使用 nullptr 而非 NULL |
...
```

## 4. run_clang_tidy.py

### 功能
运行 clang-tidy 并格式化输出，专注于 C++ Core Guidelines 检查。

### 前置要求

安装 clang-tidy：

```bash
# Ubuntu/Debian
sudo apt install clang-tidy

# macOS
brew install llvm

# Arch Linux
sudo pacman -S clang
```

### 用法

```bash
# 检查单个文件
python run_clang_tidy.py main.cpp

# 检查目录
python run_clang_tidy.py src/

# 自动应用修复（谨慎！）
python run_clang_tidy.py main.cpp --fix

# 指定额外检查规则
python run_clang_tidy.py src/ --checks="bugprone-*,cert-*"
```

### 输出示例

```
找到 15 个 C++ 文件

正在运行 clang-tidy...
检查规则: cppcoreguidelines-*, modernize-*, readability-*

[1/15] 检查 main.cpp... 3 个问题
[2/15] 检查 utils.cpp... ✓
[3/15] 检查 widget.cpp... 2 个问题
...

================================================================================

发现 12 个问题:

### cppcoreguidelines-owning-memory (4 个)

📍 main.cpp:25:15
   initializing non-owner 'Widget *' with a newly created 'gsl::owner<>'

📍 main.cpp:42:8
   deleting a pointer through a type that is not marked 'gsl::owner<>'
   ... 还有 2 个类似问题

### modernize-use-nullptr (3 个)
...

统计信息:
  cppcoreguidelines-owning-memory: 4
  modernize-use-nullptr: 3
  readability-identifier-naming: 5

总计: 12 个问题

提示: 使用 --fix 选项自动修复部分问题
```

## 工作流建议

### 1. 日常开发流程

```bash
# 1. 快速检测
python detect_violations.py src/

# 2. 如果有问题，生成详细报告
python generate_report.py src/ -r -o review.md

# 3. 自动修复简单问题
python modernize_code.py src/*.cpp --backup

# 4. 运行专业分析
python run_clang_tidy.py src/
```

### 2. 代码审查流程

```bash
# 生成完整的审查报告
python generate_report.py src/ --recursive \
    --output code_review_$(date +%Y%m%d).md
```

### 3. 现代化旧代码

```bash
# 1. 首先创建备份
git checkout -b modernize

# 2. 预览更改
python modernize_code.py old_code.cpp --dry-run

# 3. 应用更改
python modernize_code.py old_code.cpp

# 4. 验证
python detect_violations.py old_code.cpp

# 5. 提交
git add old_code.cpp
git commit -m "Modernize: NULL → nullptr, typedef → using"
```

### 4. CI/CD 集成

在 CI/CD 管道中使用：

```yaml
# .github/workflows/code-quality.yml
name: Code Quality

on: [push, pull_request]

jobs:
  cpp-guidelines:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Install dependencies
        run: |
          sudo apt-get install -y clang-tidy python3

      - name: Check C++ Guidelines
        run: |
          python scripts/detect_violations.py src/ --recursive
          python scripts/run_clang_tidy.py src/

      - name: Generate report
        run: |
          python scripts/generate_report.py src/ -r -o report.md

      - name: Upload report
        uses: actions/upload-artifact@v2
        with:
          name: code-review-report
          path: report.md
```

## 脚本依赖

所有脚本使用标准库，无需额外安装 Python 包。

- Python 3.6+
- clang-tidy（仅用于 `run_clang_tidy.py`）

## 注意事项

### 误报
自动检测可能产生误报。建议：
1. 人工审查结果
2. 使用 `--dry-run` 预览更改
3. 创建备份 (`--backup`)

### 性能
- 大型代码库扫描可能较慢
- clang-tidy 尤其耗时
- 建议使用 `--no-recursive` 限制范围

### 限制
这些脚本提供基本检测，无法替代：
- 完整的静态分析工具
- 人工代码审查
- 编译器警告

## 扩展

### 添加新的检测规则

编辑 `detect_violations.py`，添加新方法：

```python
def _detect_your_rule(self, filepath: str, lines: List[str]):
    """检测你的规则"""
    for i, line in enumerate(lines, 1):
        if your_condition(line):
            self.violations.append(Violation(
                file=filepath,
                line=i,
                column=0,
                severity=Severity.IMPORTANT,
                rule="X.Y",
                message="你的消息",
                code_snippet=line.strip(),
                suggestion="你的建议"
            ))
```

然后在 `detect_file` 中调用它。

## 获取帮助

每个脚本都支持 `--help` 选项：

```bash
python detect_violations.py --help
python modernize_code.py --help
python generate_report.py --help
python run_clang_tidy.py --help
```

## 许可

这些脚本作为 C++ Core Guidelines skill 的一部分发布。
