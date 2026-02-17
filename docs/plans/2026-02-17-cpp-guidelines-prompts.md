# cpp_guidelines_skill Prompts 功能补充实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 补充 cpp_guidelines_skill 缺失的 code_review 和 refactor_suggestion 功能，更新 SKILL.md 文档

**Architecture:** 在现有 SKILL.md 中添加 prompts 模块的使用说明，与现有 scripts 功能保持一致的结构

**Tech Stack:** Python, Markdown

---

### Task 1: 更新 SKILL.md 添加 code_review 使用说明

**Files:**
- Modify: `SKILL.md` (在现有内容后添加新章节)

**Step 1: 添加 code_review 功能说明**

在 SKILL.md 文件末尾添加:

```markdown
### 代码审查提示

```bash
python prompts/code_review.py [general|performance|safety|readability|modern]
```

参数：
- `general`: 综合审查（默认）
- `performance`: 性能优化
- `safety`: 内存和类型安全
- `readability`: 可读性和维护性
- modern: 现代 C++ 特性使用

示例：
```bash
python prompts/code_review.py safety
python prompts/code_review.py performance
```
```

**Step 2: 验证文件修改**

Run: `grep -n "code_review" /home/lv5railgun/code/cpp_guidelines_skill/SKILL.md`
Expected: 找到 code_review 相关内容

---

### Task 2: 更新 SKILL.md 添加 refactor_suggestion 使用说明

**Files:**
- Modify: `SKILL.md` (继续添加)

**Step 1: 添加 refactor_suggestion 功能说明**

在 SKILL.md 文件中添加:

```markdown
### 重构建议提示

```bash
python prompts/refactor_suggestion.py [cpp11|cpp14|cpp17|cpp20|cpp23]
```

参数：
- 目标 C++ 标准 (默认: cpp17)

示例：
```bash
python prompts/refactor_suggestion.py cpp20
python prompts/refactor_suggestion.py cpp11
```
```

**Step 2: 验证文件修改**

Run: `grep -n "refactor_suggestion" /home/lv5railgun/code/cpp_guidelines_skill/SKILL.md`
Expected: 找到 refactor_suggestion 相关内容

---

### Task 3: 验证完整功能

**Files:**
- Test: `SKILL.md`, `prompts/`

**Step 1: 运行 code_review 脚本**

Run: `cd /home/lv5railgun/code/cpp_guidelines_skill && python prompts/code_review.py safety`
Expected: 输出包含安全性审查重点的 Markdown 文本

**Step 2: 运行 refactor_suggestion 脚本**

Run: `cd /home/lv5railgun/code/cpp_guidelines_skill && python prompts/refactor_suggestion.py cpp20`
Expected: 输出包含 C++20 特性的重构提示

**Step 3: 验证功能完整性**

Run: `ls -la /home/lv5railgun/code/cpp_guidelines_skill/prompts/`
Expected: 包含 __init__.py, code_review.py, refactor_suggestion.py
```
