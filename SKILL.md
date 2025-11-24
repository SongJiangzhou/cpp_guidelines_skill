---
name: cpp-guidelines
description: C++ Core Guidelines 专家助手，用于代码审查、现代化重构和最佳实践指导。适用场景：(1) 审查 C++ 代码并提供改进建议，(2) 编写新 C++ 代码时提供指导和模板，(3) 将传统 C++ 代码现代化为 C++11/14/17/20，(4) 解释和应用特定的 Core Guidelines 规则，(5) 检测和修复常见违规（内存安全、类型安全、并发、异常处理等）。当用户处理 C++ 代码文件、询问 C++ 最佳实践、请求代码审查或需要现代化旧代码时自动触发。
---

# C++ Core Guidelines 专家助手

基于 C++ Core Guidelines 的代码审查、现代化和最佳实践指导工具。

## 概述

本 skill 提供全面的 C++ Core Guidelines 支持，帮助编写安全、高效、可维护的现代 C++ 代码。提供：

- **代码审查**：基于 Core Guidelines 分析代码，识别违规和潜在问题
- **现代化指导**：将传统 C++ (C++03/11) 升级到现代 C++ (C++17/20)
- **最佳实践**：编写新代码时提供模板和指导
- **规则解释**：详细解释特定的 Guidelines 规则及其应用

## 工作流程

### 1. 识别任务类型

根据用户请求确定任务类型：

**代码审查场景：**
- "审查这个 C++ 类"
- "这段代码有什么问题？"
- "帮我检查是否符合 Core Guidelines"

**编写新代码场景：**
- "帮我写一个 RAII 资源管理类"
- "如何正确实现单例模式？"
- "实现一个线程安全的容器"

**现代化场景：**
- "将这段 C++03 代码升级到 C++17"
- "如何使用智能指针替换裸指针？"
- "帮我重构这个类使用移动语义"

**规则查询场景：**
- "什么是 RAII？"
- "P.8 规则是什么意思？"
- "何时使用 unique_ptr vs shared_ptr？"

### 2. 执行审查或提供指导

#### 代码审查流程

遵循以下步骤进行系统化审查：

**步骤 1：读取并理解代码**
- 读取完整的代码文件
- 理解代码意图和设计
- 识别关键组件和交互

**步骤 2：应用检查清单**

按优先级检查问题（参考 `references/code_review_checklist.md`）：

1. **严重问题（必须修复）**
   - 内存安全：裸 new/delete、资源泄漏、悬挂指针
   - 类型安全：C 风格转换、const_cast、reinterpret_cast
   - 并发安全：数据竞争、死锁、缺少同步
   - 异常安全：析构函数抛异常、资源泄漏

2. **重要问题（应该修复）**
   - 接口设计：所有权不明、弱类型、参数传递不当
   - 函数设计：参数传递、函数长度、职责分离
   - 类设计：五法则、成员初始化、const 正确性

3. **改进建议（可选优化）**
   - 性能：不必要的复制、堆分配、constexpr 机会
   - 可读性：作用域、延迟初始化、魔法数字
   - 现代性：使用现代 C++ 特性

**步骤 3：提供详细反馈**

对每个问题提供：
```markdown
## [问题严重程度] 问题描述

**位置：** 文件名:行号

**违反规则：** [具体的 Core Guidelines 规则，如 R.11, P.8]

**问题说明：**
[清晰解释问题所在]

**当前代码：**
[显示有问题的代码片段]

**修复方法：**
[提供修复后的代码]

**修复原因：**
[解释为什么这样修复，以及遵循的原则]
```

**步骤 4：提供总结**

- 列出所有发现的问题
- 按优先级排序
- 提供整体代码质量评估

#### 编写新代码流程

**步骤 1：理解需求**
- 确认用户想要实现什么
- 识别关键约束（性能、线程安全等）
- 询问不明确的需求

**步骤 2：设计方案**
- 选择合适的设计模式
- 确定资源管理策略（RAII）
- 考虑异常安全性

**步骤 3：提供实现**

遵循现代 C++ 最佳实践：
- 使用智能指针管理资源
- 使用 RAII 原则
- 明确所有权语义
- 提供移动语义
- 添加适当的 const 和 noexcept
- 使用强类型接口

**步骤 4：解释设计决策**
- 说明为什么这样设计
- 引用相关的 Core Guidelines 规则
- 指出可能的权衡

#### 现代化代码流程

**步骤 1：分析现有代码**
- 识别使用的 C++ 版本特性
- 找出可以现代化的模式
- 评估现代化的影响

**步骤 2：应用现代化模式**

参考 `references/modernization_patterns.md`，应用相关模式：

**常见现代化转换：**
- 裸指针 → 智能指针
- 手动资源管理 → RAII
- 数组 → std::array / std::vector
- NULL/0 → nullptr
- typedef → using
- 手写循环 → 标准算法 / 范围 for
- 函数对象 → lambda
- C 风格转换 → C++ 转换

**步骤 3：保持功能等价**
- 确保重构后行为一致
- 保留重要的注释
- 维护 API 兼容性（如果需要）

**步骤 4：提供迁移建议**
- 说明每个更改的原因
- 标注优先级（高/中/低）
- 提供渐进式迁移路径

### 3. 使用参考资料

skill 提供四个详细的参考文档，根据需要查阅：

#### `references/guidelines_quick_ref.md`
快速参考指南，包含按主题分类的关键规则。

**何时使用：**
- 需要快速查找特定主题的规则
- 提供规则编号的快速解释
- 作为代码审查的速查表

**内容包括：**
- 哲学、接口、函数、类、资源管理
- 表达式、性能、并发、错误处理
- 常量、模板
- 按主题快速查找索引

**使用方法：**
```
需要资源管理指导时 → 查看 "资源管理 (Resource Management)" 章节
需要并发规则时 → 查看 "并发 (Concurrency)" 章节
需要某个特定规则时 → 使用规则编号搜索（如 R.11, P.8）
```

#### `references/code_review_checklist.md`
系统化的代码审查检查清单。

**何时使用：**
- 执行完整的代码审查
- 需要结构化的审查流程
- 想要确保不遗漏常见问题

**内容包括：**
- 按严重程度分类的检查项（严重/重要/改进）
- 特定场景检查清单（智能指针、异常安全、并发、类定义）
- 常见违规模式和修复
- 自动化工具建议

**使用方法：**
```
完整审查 → 按严重程度顺序检查所有项
审查智能指针使用 → 查看 "审查智能指针使用" 清单
审查并发代码 → 查看 "审查并发代码" 清单
```

#### `references/modernization_patterns.md`
从传统 C++ 到现代 C++ 的迁移模式。

**何时使用：**
- 现代化旧代码库
- 学习现代 C++ 特性
- 对比传统和现代实现

**内容包括：**
- 内存管理现代化（裸指针 → 智能指针等）
- 类型系统现代化（NULL → nullptr 等）
- 容器和算法现代化（手写循环 → 标准算法）
- 函数和 Lambda 现代化
- 并发现代化
- 错误处理现代化
- 类设计现代化
- 常量和编译期计算现代化

**使用方法：**
```
每个模式包含：
- 传统代码示例（标记为 "传统"）
- 现代代码示例（标记为 "现代"）
- 要点说明
- C++ 版本标注
```

#### `references/common_violations.md`
最常见的违规及其修复示例。

**何时使用：**
- 识别到特定违规模式
- 需要修复示例
- 学习常见陷阱

**内容包括：**
- 内存管理违规
- 类型安全违规
- 接口设计违规
- 资源管理违规
- 并发违规
- 异常安全违规
- const 正确性违规
- 最常见的 10 个违规总结

**使用方法：**
```
每个违规包含：
- ❌ 违规代码示例
- 问题说明和违反的规则
- ✅ 正确代码示例
- 详细解释
```

### 4. 示例对话

#### 示例 1：代码审查

**用户：** "帮我审查这个资源管理类"

**Claude 应该：**
1. 读取代码文件
2. 应用 `code_review_checklist.md` 中的检查项
3. 识别问题（如：缺少移动语义、五法则不完整等）
4. 对每个问题：
   - 说明违反了哪个规则（如 C.21, R.11）
   - 显示有问题的代码
   - 提供修复建议
   - 参考 `common_violations.md` 中的相关示例
5. 提供总结和优先级建议

#### 示例 2：现代化代码

**用户：** "将这段 C++03 代码升级到 C++17"

**Claude 应该：**
1. 分析代码，识别传统模式
2. 查阅 `modernization_patterns.md`
3. 应用相关模式：
   - 裸指针 → unique_ptr/shared_ptr
   - NULL → nullptr
   - typedef → using
   - 手写循环 → 范围 for 或算法
   - 等等
4. 逐项说明每个更改及其原因
5. 提供优先级建议

#### 示例 3：编写新代码

**用户：** "帮我写一个 RAII 文件句柄类"

**Claude 应该：**
1. 理解需求（管理 FILE*）
2. 查阅 `guidelines_quick_ref.md` 的资源管理章节
3. 设计并实现：
   ```cpp
   class FileHandle {
       FILE* file;
   public:
       explicit FileHandle(const char* filename, const char* mode);
       ~FileHandle() noexcept;
       FileHandle(const FileHandle&) = delete;
       FileHandle& operator=(const FileHandle&) = delete;
       FileHandle(FileHandle&&) noexcept;
       FileHandle& operator=(FileHandle&&) noexcept;
       FILE* get() const noexcept;
   };
   ```
4. 解释设计决策：
   - 遵循 RAII (R.1)
   - 禁止拷贝（避免双重释放）
   - 支持移动（所有权转移）
   - noexcept 析构函数 (C.36)

#### 示例 4：规则查询

**用户：** "R.11 规则是什么？"

**Claude 应该：**
1. 查阅 `guidelines_quick_ref.md`
2. 找到 R.11：避免显式调用 new 和 delete
3. 提供：
   - 规则说明
   - 原因
   - 正确做法（使用 make_unique/make_shared）
   - 代码示例
4. 引用 `common_violations.md` 中的相关违规示例

## 代码示例模板

### RAII 资源管理类模板

```cpp
class ResourceHandle {
    // 使用适当的资源类型
    std::unique_ptr<Resource> resource;

public:
    // 构造：获取资源
    explicit ResourceHandle(/* 参数 */)
        : resource(acquire_resource(/* ... */)) {
        if (!resource) {
            throw std::runtime_error("Cannot acquire resource");
        }
    }

    // 析构：自动释放（noexcept）
    ~ResourceHandle() noexcept = default;

    // 禁止拷贝（避免双重释放）
    ResourceHandle(const ResourceHandle&) = delete;
    ResourceHandle& operator=(const ResourceHandle&) = delete;

    // 允许移动（所有权转移）
    ResourceHandle(ResourceHandle&&) noexcept = default;
    ResourceHandle& operator=(ResourceHandle&&) noexcept = default;

    // 访问器
    Resource* get() const noexcept { return resource.get(); }
    Resource& operator*() const noexcept { return *resource; }
    Resource* operator->() const noexcept { return resource.get(); }
};
```

### 接口设计模板

```cpp
// 好的接口设计示例

// 1. 明确所有权
std::unique_ptr<Widget> create_widget();  // 返回所有权
void use_widget(Widget& w);               // 借用，不拥有
void consume_widget(std::unique_ptr<Widget> w);  // 获取所有权

// 2. 强类型参数
void set_timeout(std::chrono::milliseconds duration);  // 不是 int

// 3. 使用 span 而非指针+大小
void process(std::span<const int> data);  // 不是 int*, size_t

// 4. const 正确性
void read_only(const Widget& w);
void modify(Widget& w);

// 5. noexcept 用于不抛异常的函数
int compute(int x) noexcept;
```

### 现代 C++ 类模板

```cpp
class ModernWidget {
    // 使用成员初始化器
    int value = 0;
    std::string name = "default";
    std::unique_ptr<Data> data;

public:
    // 默认构造函数
    ModernWidget() = default;

    // 自定义构造函数
    explicit ModernWidget(int v, std::string n)
        : value(v), name(std::move(n)), data(std::make_unique<Data>()) {}

    // 五法则（根据需要）
    ~ModernWidget() = default;

    // 如果包含 unique_ptr，通常删除拷贝
    ModernWidget(const ModernWidget&) = delete;
    ModernWidget& operator=(const ModernWidget&) = delete;

    // 默认移动即可
    ModernWidget(ModernWidget&&) noexcept = default;
    ModernWidget& operator=(ModernWidget&&) noexcept = default;

    // const 成员函数
    int get_value() const noexcept { return value; }
    const std::string& get_name() const noexcept { return name; }

    // 非 const 成员函数
    void set_value(int v) noexcept { value = v; }
};
```

## 常见问题处理

### 用户要求审查大型代码库

1. 建议分模块审查
2. 优先审查关键模块（资源管理、并发代码）
3. 提供渐进式改进计划

### 用户代码有多个严重问题

1. 按优先级排序（严重 → 重要 → 改进）
2. 先修复严重问题（内存安全、并发安全）
3. 提供分阶段修复计划

### 用户询问规则冲突

1. 解释规则的意图和上下文
2. 说明权衡和例外情况
3. 提供具体场景的建议

### 用户需要向后兼容

1. 识别必须保留的接口
2. 提供内部现代化方案
3. 建议使用适配器模式

## 重要原则

在使用本 skill 时，始终遵循以下原则：

1. **安全第一**：优先关注内存安全、类型安全、并发安全
2. **清晰优于聪明**：代码应该易于理解和维护
3. **现代但实用**：使用现代特性，但不过度工程化
4. **渐进式改进**：不要期望一次性重写所有代码
5. **基于规则**：所有建议都应有 Core Guidelines 规则支持

## 工具脚本

本 skill 包含四个实用的 Python 脚本，用于自动化代码分析和现代化：

### 1. detect_violations.py - 违规检测

快速检测常见的 Core Guidelines 违规：

```bash
# 检测单个文件
python scripts/detect_violations.py main.cpp

# 递归检测目录
python scripts/detect_violations.py src/ --recursive
```

**检测项目：**
- 直接使用 new/delete (R.11)
- NULL 而非 nullptr (ES.47)
- C 风格类型转换 (ES.49)
- typedef 而非 using (T.43)
- 缺少 const、手写循环等

### 2. modernize_code.py - 自动现代化

自动应用现代化转换：

```bash
# 预览更改
python scripts/modernize_code.py main.cpp --dry-run

# 应用更改（创建备份）
python scripts/modernize_code.py main.cpp --backup
```

**转换项目：**
- NULL → nullptr
- typedef → using
- 添加 explicit 到构造函数
- 0 → nullptr（指针）

### 3. generate_report.py - 生成报告

生成详细的代码审查报告：

```bash
# 生成 Markdown 报告
python scripts/generate_report.py src/ -r -o report.md

# 生成 HTML 报告
python scripts/generate_report.py src/ -r -o report.html --format html
```

**报告内容：**
- 违规统计和分类
- 按规则和文件统计
- 详细问题列表
- 修复优先级建议

### 4. run_clang_tidy.py - Clang-Tidy 集成

运行 clang-tidy 并格式化输出：

```bash
# 分析代码
python scripts/run_clang_tidy.py src/

# 自动修复
python scripts/run_clang_tidy.py main.cpp --fix
```

**注意：** 需要安装 clang-tidy

### 使用建议

**日常开发：**
1. 使用 `detect_violations.py` 快速检测
2. 使用 `modernize_code.py` 自动修复简单问题
3. 使用 `run_clang_tidy.py` 进行深度分析

**代码审查：**
使用 `generate_report.py` 生成完整报告

**详细文档：**
查看 `scripts/README.md` 了解完整用法

## 参考资料说明

本 skill 不直接包含完整的 CppCoreGuidelines.md（该文件约 23000 行），而是提供精心整理的参考文档：

- **guidelines_quick_ref.md**：按主题分类的关键规则快速参考
- **code_review_checklist.md**：系统化的代码审查流程
- **modernization_patterns.md**：传统到现代 C++ 的迁移模式
- **common_violations.md**：最常见的违规和修复示例

这些文档涵盖了 Core Guidelines 中最重要和最常用的内容，足以处理绝大多数实际场景。

如果需要查阅原始 Core Guidelines 的详细内容，可以参考用户工作目录中的 CppCoreGuidelines.md 文件（如果存在）。
