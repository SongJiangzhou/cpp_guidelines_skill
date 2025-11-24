# C++ 代码审查检查清单

基于 C++ Core Guidelines 的代码审查检查清单。按优先级和类别组织。

## 🔴 严重问题（必须修复）

### 资源管理
- [ ] **直接使用 new/delete**：代码中是否直接调用了 `new`/`delete`？应改用智能指针或容器
  - 违反规则：R.11
  - 修复方法：使用 `make_unique`、`make_shared` 或 STL 容器

- [ ] **资源泄漏**：资源是否正确释放？
  - 违反规则：P.8, R.1
  - 修复方法：使用 RAII 包装资源

- [ ] **双重释放**：是否可能多次删除同一资源？
  - 违反规则：R.3
  - 修复方法：使用智能指针，确保明确所有权

- [ ] **悬挂指针/引用**：指针或引用是否可能指向已销毁对象？
  - 违反规则：ES.65
  - 检查要点：局部对象的引用返回、异步操作中的引用捕获

### 内存安全
- [ ] **缓冲区溢出**：数组访问是否有边界检查？
  - 违反规则：Bounds safety profile
  - 修复方法：使用 `std::span`、`std::vector` 或 `at()` 方法

- [ ] **空指针解引用**：是否检查了空指针？
  - 违反规则：ES.65
  - 修复方法：使用 `gsl::not_null` 或添加空指针检查

- [ ] **未初始化变量**：所有变量是否都已初始化？
  - 违反规则：ES.20
  - 修复方法：在声明时立即初始化

### 类型安全
- [ ] **C 风格类型转换**：是否使用了 `(Type)value` 形式的转换？
  - 违反规则：ES.49, Type safety profile
  - 修复方法：使用 `static_cast`、`dynamic_cast` 等

- [ ] **reinterpret_cast**：是否使用了 `reinterpret_cast`？
  - 违反规则：Type.1
  - 审查要点：是否真的必要？有无更安全的替代方案？

- [ ] **const_cast**：是否去除了 `const`？
  - 违反规则：ES.50
  - 修复方法：重新设计接口

### 并发安全
- [ ] **数据竞争**：多线程是否正确同步？
  - 违反规则：CP.2
  - 检查要点：共享可变数据的访问

- [ ] **死锁可能**：是否正确获取多个锁？
  - 违反规则：CP.21
  - 修复方法：使用 `std::scoped_lock` 或 `std::lock()`

- [ ] **忘记加锁**：访问共享数据是否持有锁？
  - 违反规则：CP.20
  - 修复方法：使用 RAII 锁（`lock_guard`、`unique_lock`）

### 异常安全
- [ ] **析构函数抛异常**：析构函数是否可能抛出异常？
  - 违反规则：C.36, E.16
  - 修复方法：捕获并处理所有异常

- [ ] **异常导致资源泄漏**：异常时资源是否正确释放？
  - 违反规则：E.6
  - 修复方法：使用 RAII

- [ ] **构造函数失败但没有异常**：构造失败是否抛出异常？
  - 违反规则：E.5
  - 修复方法：抛出异常或使用工厂函数

## 🟡 重要问题（应该修复）

### 接口设计
- [ ] **所有权不明确**：指针/引用参数的所有权是否明确？
  - 违反规则：I.11
  - 修复方法：使用智能指针表示所有权转移，使用引用表示借用

- [ ] **可空指针未标记**：不应为空的指针是否声明为 `not_null`？
  - 违反规则：I.12
  - 修复方法：使用 `gsl::not_null<T*>`

- [ ] **数组作为指针传递**：数组是否作为单个指针传递？
  - 违反规则：I.13
  - 修复方法：使用 `std::span<T>` 或传递容器引用

- [ ] **接口类型弱**：接口是否使用原始类型（`int`、`double`）而非强类型？
  - 违反规则：I.4
  - 代码示例：`void set_timeout(int ms)` → `void set_timeout(std::chrono::milliseconds)`

- [ ] **缺少前置/后置条件**：复杂函数是否文档化了前置和后置条件？
  - 违反规则：I.5, I.7
  - 修复方法：使用 `Expects()` 和 `Ensures()`

### 函数设计
- [ ] **参数传递不当**：参数传递方式是否正确？
  - 违反规则：F.15, F.16, F.17
  - 检查要点：
    - 便宜复制的类型（`int`、`double`）：按值
    - 昂贵复制的输入：按 `const&`
    - 输入输出：按非 `const&`
    - 输出：返回值，不用输出参数

- [ ] **使用智能指针作为参数**：函数是否不必要地使用智能指针参数？
  - 违反规则：F.7
  - 修复方法：使用 `T*` 或 `T&`，除非需要表达所有权语义

- [ ] **输出参数**：是否使用输出参数而非返回值？
  - 违反规则：F.20
  - 修复方法：返回值或结构体

- [ ] **函数过长**：函数是否过长（>50 行）？
  - 违反规则：F.3
  - 修复方法：拆分为更小的函数

- [ ] **函数做多件事**：函数是否做了多个逻辑操作？
  - 违反规则：F.2
  - 检查要点：函数名是否包含 "and"？

### 类设计
- [ ] **五法则不完整**：如果定义了析构函数/拷贝/移动，是否定义了全部？
  - 违反规则：C.21
  - 修复方法：定义或删除所有五个特殊成员函数

- [ ] **单参数构造函数未 explicit**：是否可能发生意外的隐式转换？
  - 违反规则：C.46
  - 修复方法：添加 `explicit`

- [ ] **成员初始化顺序错误**：初始化列表顺序是否与成员声明顺序一致？
  - 违反规则：C.47
  - 修复方法：按声明顺序初始化

- [ ] **默认构造函数仅初始化**：默认构造函数是否只是初始化成员？
  - 违反规则：C.45
  - 修复方法：使用成员初始化器 `int x = 0;`

- [ ] **虚基类析构函数**：多态基类的析构函数是否为 `virtual`？
  - 违反规则：C.35
  - 修复方法：`virtual ~Base() = default;`

- [ ] **struct/class 使用不当**：有不变式的类型是否使用 `class`？
  - 违反规则：C.2
  - 指导建议：简单数据聚合用 `struct`，有不变式用 `class`

### const 正确性
- [ ] **应该 const 的成员函数**：不修改对象的成员函数是否标记为 `const`？
  - 违反规则：Con.2
  - 修复方法：添加 `const`

- [ ] **应该 const 的参数**：只读参数是否声明为 `const`？
  - 违反规则：Con.3
  - 修复方法：使用 `const T&` 或 `const T*`

- [ ] **应该 const 的局部变量**：不修改的变量是否声明为 `const`？
  - 违反规则：Con.1, Con.4
  - 修复方法：添加 `const`

### 现代 C++ 使用
- [ ] **使用 NULL 或 0 表示空指针**：是否使用 `nullptr`？
  - 违反规则：ES.47
  - 修复方法：使用 `nullptr`

- [ ] **手写循环**：是否可以使用标准算法或范围 for？
  - 违反规则：ES.1, ES.71
  - 修复方法：使用 `std::find`、`std::transform`、范围 for 等

- [ ] **typedef 而非 using**：是否使用 `using` 定义类型别名？
  - 违反规则：T.43
  - 修复方法：`using IntVec = vector<int>;`

- [ ] **冗余类型声明**：是否可以使用 `auto`？
  - 违反规则：ES.11
  - 代码示例：`auto p = make_unique<Widget>();`

## 🟢 改进建议（可选优化）

### 性能
- [ ] **不必要的复制**：是否有不必要的对象复制？
  - 改进建议：使用移动语义或引用

- [ ] **不必要的堆分配**：是否可以使用栈对象？
  - 违反规则：R.5
  - 改进建议：优先使用作用域对象

- [ ] **可以 constexpr**：函数是否可以在编译时求值？
  - 违反规则：Per.11, F.4
  - 改进建议：添加 `constexpr`

- [ ] **可以 noexcept**：函数是否保证不抛异常？
  - 违反规则：F.6
  - 改进建议：添加 `noexcept`

### 可读性
- [ ] **复杂初始化**：const 变量的初始化是否复杂？
  - 违反规则：ES.28
  - 改进建议：使用立即调用的 lambda

- [ ] **作用域过大**：变量作用域是否可以更小？
  - 违反规则：ES.5
  - 改进建议：在最小作用域声明

- [ ] **延迟初始化**：变量声明和初始化是否分离？
  - 违反规则：ES.22
  - 改进建议：声明时立即初始化

- [ ] **魔法数字**：是否使用未命名的数字常量？
  - 改进建议：定义命名常量

### 表达性
- [ ] **意图不明确**：代码意图是否清晰？
  - 违反规则：P.1, P.3
  - 改进建议：使用类型、算法和命名表达意图

- [ ] **注释过多**：是否可以通过代码本身表达？
  - 违反规则：P.1
  - 改进建议：改进代码结构和命名

## 特定场景检查清单

### 审查智能指针使用
```cpp
// ❌ 不好
Widget* create() { return new Widget(); }
void use(shared_ptr<Widget> w);

// ✅ 好
unique_ptr<Widget> create() { return make_unique<Widget>(); }
void use(Widget& w);
```

检查项：
- [ ] 所有权转移使用 `unique_ptr` 返回
- [ ] 共享所有权使用 `shared_ptr`
- [ ] 非所有使用 `T*` 或 `T&`
- [ ] 使用 `make_unique`/`make_shared`
- [ ] 优先 `unique_ptr` 而非 `shared_ptr`

### 审查异常安全性
```cpp
// ❌ 不好 - 异常不安全
void process() {
    Resource* r = acquire();
    use(r);  // 可能抛异常
    release(r);  // 可能不执行
}

// ✅ 好 - RAII
void process() {
    auto r = ResourceHandle(acquire());
    use(r);  // 异常安全
}  // 自动释放
```

检查项：
- [ ] 所有资源使用 RAII 管理
- [ ] 析构函数不抛异常（或捕获所有异常）
- [ ] 构造失败时抛出异常
- [ ] 没有裸资源管理

### 审查并发代码
```cpp
// ❌ 不好
mutex m;
int counter = 0;
void increment() {
    m.lock();
    ++counter;  // 如果抛异常，锁不释放
    m.unlock();
}

// ✅ 好
mutex m;
int counter = 0;
void increment() {
    lock_guard lock(m);
    ++counter;  // 异常安全
}
```

检查项：
- [ ] 共享可变数据使用同步
- [ ] 使用 RAII 锁（不直接 `lock()`/`unlock()`）
- [ ] 多个锁使用 `scoped_lock` 或 `std::lock()`
- [ ] 条件变量有判断条件
- [ ] 不在锁内调用未知代码
- [ ] 临界区尽可能小

### 审查类定义
```cpp
// ❌ 不好
class Widget {
public:
    Widget() { }  // 成员未初始化
    ~Widget();    // 未定义拷贝/移动
    int* data;    // 裸指针
};

// ✅ 好
class Widget {
public:
    Widget() = default;
    ~Widget() = default;
    Widget(const Widget&) = delete;
    Widget& operator=(const Widget&) = delete;
    Widget(Widget&&) = default;
    Widget& operator=(Widget&&) = default;
private:
    unique_ptr<int[]> data;  // 智能指针
    int size = 0;            // 成员初始化器
};
```

检查项：
- [ ] 五法则完整（或全部默认/删除）
- [ ] 成员变量有初始化器
- [ ] 资源成员使用智能指针或 RAII 包装
- [ ] 单参数构造函数是 `explicit`
- [ ] 虚基类析构函数是 `virtual`
- [ ] public 接口最小
- [ ] 不变式在构造函数中建立

## 常见违规模式和修复

### 模式 1：所有权混乱
```cpp
// ❌ 问题：所有权不明确
void process(Widget* w);  // 谁拥有？谁删除？

// ✅ 修复：明确所有权
void process(Widget& w);              // 借用，不拥有
unique_ptr<Widget> create();          // 转移所有权
void consume(unique_ptr<Widget> w);   // 获取所有权
```

### 模式 2：异常不安全
```cpp
// ❌ 问题：资源泄漏
void f() {
    int* p = new int[100];
    process(p);  // 可能抛异常
    delete[] p;  // 可能不执行
}

// ✅ 修复：RAII
void f() {
    auto p = make_unique<int[]>(100);
    process(p.get());
}  // 自动清理
```

### 模式 3：数据竞争
```cpp
// ❌ 问题：无同步
int counter = 0;
void increment() { ++counter; }  // 多线程不安全

// ✅ 修复 1：原子变量
atomic<int> counter{0};
void increment() { ++counter; }

// ✅ 修复 2：互斥锁
int counter = 0;
mutex m;
void increment() {
    lock_guard lock(m);
    ++counter;
}
```

### 模式 4：类型不安全
```cpp
// ❌ 问题：弱类型
void sleep_for(int milliseconds);
sleep_for(5);  // 5 什么？秒？毫秒？

// ✅ 修复：强类型
void sleep_for(chrono::milliseconds duration);
sleep_for(chrono::milliseconds(5));
sleep_for(5ms);  // C++14
```

### 模式 5：过度使用 shared_ptr
```cpp
// ❌ 问题：不必要的共享所有权
void process(shared_ptr<Widget> w);  // 暗示共享，但实际不需要

// ✅ 修复：按需选择
void process(Widget& w);              // 只使用，不拥有
void process(unique_ptr<Widget> w);   // 独占所有权
void process(shared_ptr<Widget> w);   // 真正需要共享时
```

### 模式 6：const 不正确
```cpp
// ❌ 问题：应该 const 但不是
class Widget {
    int value;
public:
    int get() { return value; }  // 应该是 const
};

void use(Widget& w);  // 应该是 const&

// ✅ 修复
class Widget {
    int value;
public:
    int get() const { return value; }
};

void use(const Widget& w);
```

### 模式 7：手写循环
```cpp
// ❌ 问题：手写 find
int find_index(const vector<int>& v, int target) {
    for (int i = 0; i < v.size(); ++i) {
        if (v[i] == target) return i;
    }
    return -1;
}

// ✅ 修复：使用算法
auto find_element(const vector<int>& v, int target) {
    return find(v.begin(), v.end(), target);
}

// 或者范围 for
bool contains(const vector<int>& v, int target) {
    for (int value : v) {
        if (value == target) return true;
    }
    return false;
}
```

## 自动化工具建议

以下工具可以自动检测许多违规：

1. **Clang-Tidy**
   - 配置：启用 `cppcoreguidelines-*` 检查
   - 检测：大部分 Core Guidelines 规则

2. **CppCheck**
   - 检测：内存泄漏、缓冲区溢出、空指针解引用

3. **AddressSanitizer (ASan)**
   - 检测：内存错误（使用后释放、缓冲区溢出等）

4. **ThreadSanitizer (TSan)**
   - 检测：数据竞争

5. **Clang Static Analyzer**
   - 检测：资源泄漏、空指针解引用等

建议在 CI/CD 中集成这些工具。
