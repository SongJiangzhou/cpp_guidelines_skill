# cpp-guidelines Skill 重构实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 cpp_guidelines_skill 重构为符合 skill-creator 标准的 skill 格式，通过 /cpp-guidelines 命令调用

**Architecture:** 按照 skill-creator 标准重构：精简 SKILL.md + 添加 commands/ + 优化 references/

**Tech Stack:** Python, Markdown, Skill 格式

---

### Task 1: 创建 commands/ 目录和命令定义

**Files:**
- Create: `commands/cpp-guidelines.md`

**Step 1: 创建 commands 目录**

Run: `mkdir -p /home/lv5railgun/code/cpp_guidelines_skill/commands`

**Step 2: 创建命令定义文件**

```markdown
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
```

**Step 3: 验证目录结构**

Run: `ls -la /home/lv5railgun/code/cpp_guidelines_skill/commands/`
Expected: 包含 cpp-guidelines.md

---

### Task 2: 精简 SKILL.md

**Files:**
- Modify: `SKILL.md`

**Step 1: 重写 SKILL.md frontmatter**

修改 name 为 `cpp-guidelines`，更新 description

**Step 2: 精简 SKILL.md 内容**

保留：
- 快速开始（简化）
- 各功能的简要说明
- 参考文档指引

移除或简化：
- 详细的参数说明 → 指向 references/
- 冗余的示例 → 保留核心示例

**Step 3: 添加 commands 引用**

在 SKILL.md 中说明通过 /cpp-guidelines 命令调用

---

### Task 3: 优化 references/ 目录

**Files:**
- Create: `references/quick_reference.md`

**Step 1: 创建快速参考文档**

创建简洁的快速参考卡片，包含所有功能的简要用法

**Step 2: 验证 JSON 文件**

确保现有的 JSON 文件格式正确

---

### Task 4: 验证脚本功能

**Files:**
- Test: `scripts/*.py`

**Step 1: 测试各脚本**

```bash
python scripts/naming_checker.py UserName class
python scripts/code_review.py safety
python scripts/refactor_suggestion.py cpp17
```

**Step 2: 验证输出**

确认所有脚本正常工作

---

### Task 5: 提交更改

**Files:**
- Commit all changes

**Step 1: Git 提交**

```bash
git add -A
git commit -m "refactor: restructure to standard skill format with commands/"
```
