# cpp-guidelines JSON 文件位置调整实施计划

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** 将 JSON 文件从 references/ 移动到 assets/ 目录，符合 skill-creator 标准

**Architecture:** JSON 数据文件属于 assets（静态资源），Markdown 文档属于 references

**Tech Stack:** 文件系统操作, Git

---

### Task 1: 创建 assets/ 目录并移动 JSON 文件

**Files:**
- Create: `assets/` directory
- Move: references/*.json → assets/
- Modify: SKILL.md

**Step 1: 创建 assets 目录**

Run: `mkdir -p /home/lv5railgun/code/cpp_guidelines_skill/assets`

**Step 2: 移动 JSON 文件**

Run: `mv references/*.json assets/`

**Step 3: 验证**

Run: `ls -la assets/`
Expected: 包含 4 个 JSON 文件

---

### Task 2: 更新 SKILL.md 中的路径引用

**Files:**
- Modify: `SKILL.md`

**Step 1: 更新 references 路径**

将 `references/*.json` 改为 `assets/*.json`

Run: `sed -i 's|references/|assets/|g' SKILL.md`

**Step 2: 验证**

Run: `grep -n "assets/" SKILL.md`
Expected: 找到 4 处引用

---

### Task 3: 验证脚本功能

**Files:**
- Test: `scripts/*.py`

**Step 1: 测试脚本仍然能读取 JSON**

Run: `python -c "import json; json.load(open('assets/naming_conventions.json'))" && echo "JSON readable"`

Expected: JSON readable

---

### Task 4: 提交更改

**Files:**
- Commit all changes

**Step 1: Git 提交**

Run: `git add -A && git commit -m "refactor: move JSON files to assets/ to match skill structure"`

---
