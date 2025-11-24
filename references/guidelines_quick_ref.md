# C++ Core Guidelines 快速参考

本文档提供 C++ Core Guidelines 的快速参考，按主题分类。

## 目录

- [哲学 (Philosophy)](#哲学-philosophy)
- [接口 (Interfaces)](#接口-interfaces)
- [函数 (Functions)](#函数-functions)
- [类和类层次 (Classes)](#类和类层次-classes)
- [资源管理 (Resource Management)](#资源管理-resource-management)
- [表达式和语句 (Expressions & Statements)](#表达式和语句-expressions--statements)
- [性能 (Performance)](#性能-performance)
- [并发 (Concurrency)](#并发-concurrency)
- [错误处理 (Error Handling)](#错误处理-error-handling)
- [常量和不可变性 (Constants)](#常量和不可变性-constants)
- [模板 (Templates)](#模板-templates)

## 哲学 (Philosophy)

### P.1: 在代码中直接表达想法
- 使用类型系统表达意图
- 优先使用标准库算法而非手写循环
- 使用强类型而非原始类型

### P.2: 使用 ISO 标准 C++
- 避免编译器特定扩展
- 使用现代 C++ (C++17/20) 特性

### P.3: 表达意图
- 使用有意义的名称
- 使用 `const` 表示不变性
- 使用 `constexpr` 表示编译期常量

### P.4: 理想情况下，程序应该是静态类型安全的
- 避免类型转换
- 使用 `variant` 而非 `union`
- 使用 `any` 而非 `void*`

### P.5: 优先编译期检查而非运行时检查
- 使用 `constexpr` 函数
- 使用 `static_assert`
- 使用模板和概念

### P.8: 不要泄漏任何资源
- 使用 RAII
- 使用智能指针
- 避免裸 `new`/`delete`

### P.10: 优先使用不可变数据
- 使用 `const` 和 `constexpr`
- 减少可变状态

## 接口 (Interfaces)

### I.1: 使接口显式化
```cpp
// 好
void draw(Canvas& canvas, const Shape& shape);

// 不好 - 隐式依赖全局状态
void draw(const Shape& shape);
```

### I.2: 避免非 const 全局变量
- 全局变量破坏模块化
- 难以测试和理解

### I.4: 使接口精确且强类型化
```cpp
// 好
void set_timeout(std::chrono::milliseconds ms);

// 不好
void set_timeout(int ms);
```

### I.11: 永远不要通过裸指针或引用转移所有权
```cpp
// 好 - 明确所有权转移
std::unique_ptr<Widget> create_widget();

// 不好 - 所有权不明确
Widget* create_widget();  // 谁负责删除？
```

### I.12: 将不能为空的指针声明为 `not_null`
```cpp
void process(gsl::not_null<Widget*> widget);
```

### I.13: 不要将数组作为单个指针传递
```cpp
// 好
void process(std::span<int> data);

// 不好
void process(int* data, size_t size);
```

## 函数 (Functions)

### F.1: 将有意义的操作"打包"为精心命名的函数
```cpp
// 好
bool is_valid_email(const string& email);

// 不好 - 内联复杂逻辑
if (email.find('@') != string::npos && email.find('.') != string::npos) { ... }
```

### F.2: 函数应该执行单一逻辑操作
- 每个函数只做一件事
- 如果函数名包含 "and"，考虑拆分

### F.3: 保持函数简短
- 一般不超过 40-50 行
- 如果太长，考虑拆分

### F.7: 对于一般用途，使用 `T*` 或 `T&` 参数而非智能指针
```cpp
// 好 - 不假设所有权
void use(Widget& w);

// 不好 - 不必要的所有权假设
void use(shared_ptr<Widget> w);
```

### F.15: 优先使用简单和传统的信息传递方式

**输入参数：**
- 便宜复制的类型：按值传递 (`int`, `double`, 小对象)
- 其他类型：按 `const&` 传递

**输出参数：**
- 优先返回值（使用移动语义）
- 避免输出参数

**输入输出参数：**
- 按非 `const` 引用传递

```cpp
// 好
string process(const string& input);

// 不好
void process(const string& input, string& output);
```

### F.16: 对于"输入"参数，便宜复制的类型按值传递，其他按 `const&` 传递
```cpp
void f(int x);                    // 便宜复制
void f(const string& s);          // 昂贵复制
void f(const vector<int>& v);     // 昂贵复制
```

### F.17: 对于"输入输出"参数，按非 `const` 引用传递
```cpp
void update(Widget& w);
```

### F.20: 对于"输出"值，优先返回值而非输出参数
```cpp
// 好
vector<int> compute();

// 不好
void compute(vector<int>& result);
```

### F.21: 要返回多个"输出"值，优先返回结构体或元组
```cpp
// 好
struct Result { int value; bool success; };
Result compute();

// 或者
std::pair<int, bool> compute();

// 不好
bool compute(int& result);
```

## 类和类层次 (Classes)

### C.2: 如果类有不变式，使用 `class`；如果数据成员可以独立变化，使用 `struct`
```cpp
// 类有不变式
class Date {
    int year, month, day;  // 必须保持有效日期
public:
    Date(int y, int m, int d);
};

// 简单数据聚合
struct Point {
    double x, y;
};
```

### C.4: 仅当函数需要直接访问类的内部表示时才使其成为成员
```cpp
class Widget {
    void internal_operation();  // 需要访问私有数据
};

// 不需要访问内部，使用非成员函数
void draw(const Widget& w);
```

### C.9: 最小化成员的暴露
- 默认 `private`
- 只在必要时 `public`

### C.21: 如果定义或 `=delete` 任何复制、移动或析构函数，定义或 `=delete` 它们全部（五法则）
```cpp
class Resource {
public:
    Resource();
    ~Resource();
    Resource(const Resource&);
    Resource& operator=(const Resource&);
    Resource(Resource&&) noexcept;
    Resource& operator=(Resource&&) noexcept;
};

// 或者全部使用默认/删除
class Resource {
public:
    ~Resource() = default;
    Resource(const Resource&) = delete;
    Resource& operator=(const Resource&) = delete;
    Resource(Resource&&) = default;
    Resource& operator=(Resource&&) = default;
};
```

### C.30: 如果类需要显式对象销毁时的行为，定义析构函数
```cpp
class FileHandle {
    FILE* file;
public:
    ~FileHandle() { if (file) fclose(file); }
};
```

### C.31: 类获取的所有资源必须在析构函数中释放
- 遵循 RAII 原则

### C.35: 基类析构函数应该是 `public` 且 `virtual`，或者是 `protected` 且非 `virtual`
```cpp
// 多态基类
class Base {
public:
    virtual ~Base() = default;
};

// 非多态基类（不打算通过基类指针删除）
class Base {
protected:
    ~Base() = default;
};
```

### C.45: 不要定义仅初始化数据成员的默认构造函数；使用成员初始化器
```cpp
// 好
class Widget {
    int value = 0;
    string name = "default";
};

// 不好
class Widget {
    int value;
    string name;
public:
    Widget() : value(0), name("default") {}
};
```

### C.46: 默认情况下，将单参数构造函数声明为 `explicit`
```cpp
class String {
public:
    explicit String(int size);  // 防止隐式转换
};
```

### C.47: 按成员声明的顺序定义和初始化成员变量
```cpp
class Widget {
    int x;
    int y;
public:
    Widget() : x(0), y(0) {}  // 按声明顺序
};
```

## 资源管理 (Resource Management)

### R.1: 使用资源句柄和 RAII 自动管理资源
```cpp
// 好
void use() {
    auto file = std::ifstream("data.txt");
    // 自动关闭
}

// 不好
void use() {
    FILE* file = fopen("data.txt", "r");
    // ... 容易忘记 fclose
    fclose(file);
}
```

### R.3: 裸指针 (`T*`) 不拥有所有权
```cpp
void process(Widget* w);  // 不拥有，只使用
```

### R.5: 优先使用作用域对象，不要进行不必要的堆分配
```cpp
// 好
Widget w;

// 不好 - 不必要的堆分配
auto w = make_unique<Widget>();
```

### R.10: 避免 `malloc()` 和 `free()`
- 使用 `new`/`delete`（更好：使用智能指针）

### R.11: 避免显式调用 `new` 和 `delete`
```cpp
// 好
auto p = make_unique<Widget>();
auto s = make_shared<Widget>();

// 不好
Widget* p = new Widget();
delete p;
```

### R.12: 立即将显式资源分配的结果交给管理对象
```cpp
// 好
auto p = unique_ptr<Widget>(new Widget());

// 更好
auto p = make_unique<Widget>();
```

### R.20: 使用 `unique_ptr` 或 `shared_ptr` 表示所有权
```cpp
unique_ptr<Widget> create_widget();     // 独占所有权
shared_ptr<Widget> get_shared_widget(); // 共享所有权
```

### R.21: 优先使用 `unique_ptr` 而非 `shared_ptr`，除非需要共享所有权
- `unique_ptr` 更轻量
- `shared_ptr` 有引用计数开销

### R.22: 使用 `make_shared()` 创建 `shared_ptr`
```cpp
// 好 - 一次分配
auto p = make_shared<Widget>();

// 不好 - 两次分配
auto p = shared_ptr<Widget>(new Widget());
```

### R.23: 使用 `make_unique()` 创建 `unique_ptr`
```cpp
auto p = make_unique<Widget>();
```

## 表达式和语句 (Expressions & Statements)

### ES.1: 优先使用标准库而非其他库和"手工代码"
```cpp
// 好
auto it = find(v.begin(), v.end(), x);

// 不好
for (int i = 0; i < v.size(); ++i) {
    if (v[i] == x) { ... }
}
```

### ES.5: 保持作用域小
```cpp
// 好
void f() {
    {
        auto lock = std::lock_guard(mutex);
        // 使用共享资源
    }  // lock 立即释放
}
```

### ES.6: 在 for 语句的初始化和条件中声明名称，限制作用域
```cpp
for (int i = 0; i < 100; ++i) { ... }
```

### ES.10: 每次声明只声明一个名称
```cpp
// 好
int x = 0;
int y = 0;

// 不好
int x = 0, y = 0;
```

### ES.11: 使用 `auto` 避免类型名称的冗余重复
```cpp
// 好
auto p = make_unique<Widget>();
auto it = v.begin();

// 不好
unique_ptr<Widget> p = make_unique<Widget>();
vector<int>::iterator it = v.begin();
```

### ES.20: 总是初始化对象
```cpp
// 好
int x = 0;
string s = "hello";

// 不好
int x;  // 未初始化
```

### ES.22: 在有值初始化之前不要声明变量
```cpp
// 好
auto x = compute_value();

// 不好
int x;
// ... 很多代码
x = compute_value();
```

### ES.23: 优先使用 `{}` 初始化器语法
```cpp
int x{7};
vector<int> v{1, 2, 3};
Widget w{arg1, arg2};
```

### ES.25: 如果必须使对象可变，声明为 `const`
```cpp
const int max_value = 100;
```

### ES.28: 使用 lambda 进行复杂初始化，特别是 `const` 变量
```cpp
const auto value = [&] {
    if (condition) return compute_a();
    else return compute_b();
}();
```

### ES.46: 避免有损（缩窄、截断）算术转换
```cpp
// 不好
double d = 7.9;
int i = d;  // 截断

// 好
int i = static_cast<int>(d);  // 显式
```

### ES.47: 使用 `nullptr` 而非 `0` 或 `NULL`
```cpp
Widget* p = nullptr;  // 好
Widget* p = NULL;     // 不好
Widget* p = 0;        // 不好
```

### ES.50: 不要强制转换掉 `const`
```cpp
// 不好
const int x = 42;
int& y = const_cast<int&>(x);
```

### ES.56: 仅在需要将对象显式移动到另一作用域时使用 `std::move()`
```cpp
vector<string> v1;
vector<string> v2 = std::move(v1);  // v1 被移动
```

### ES.60: 避免在资源管理函数之外使用 `new` 和 `delete`
- 使用智能指针和容器

### ES.65: 不要解引用无效指针
```cpp
// 不好
int* p = nullptr;
*p = 42;  // 崩溃
```

### ES.70: 当有选择时，优先使用 switch 语句而非 if 语句
```cpp
// 好
switch (x) {
    case 1: ...; break;
    case 2: ...; break;
    default: ...;
}
```

### ES.71: 当有选择时，优先使用范围 for 语句而非普通 for 语句
```cpp
// 好
for (auto& x : v) { ... }

// 不好
for (int i = 0; i < v.size(); ++i) {
    auto& x = v[i];
    ...
}
```

## 性能 (Performance)

### Per.1: 不要无理由地进行优化
- 首先保证正确性
- 测量后再优化

### Per.2: 不要过早优化
- 先让代码工作
- 然后测量
- 最后优化瓶颈

### Per.3: 不要优化非关键性能的部分
- 使用性能分析器找到瓶颈

### Per.5: 不要假设复杂代码一定比简单代码快
- 简单代码通常更快
- 编译器很聪明

### Per.7: 设计以支持优化
```cpp
// 好 - 可以优化
void process(span<int> data);

// 不好 - 难以优化
void process(int* begin, int* end);
```

### Per.10: 依赖静态类型系统
- 避免运行时类型检查
- 使用模板和重载

### Per.11: 将计算从运行时移到编译时
```cpp
// 好
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

// 编译时计算
constexpr int f10 = factorial(10);
```

### Per.19: 可预测的内存访问
- 顺序访问优于随机访问
- 数据局部性很重要

## 并发 (Concurrency)

### CP.1: 假设你的代码将作为多线程程序的一部分运行
- 考虑线程安全

### CP.2: 避免数据竞争
```cpp
// 不好
int counter = 0;
void increment() { ++counter; }  // 数据竞争

// 好
atomic<int> counter{0};
void increment() { ++counter; }
```

### CP.3: 最小化可写数据的显式共享
- 优先使用消息传递
- 减少共享状态

### CP.4: 以任务的方式思考，而非线程
```cpp
// 好
auto future = async(launch::async, []{ return compute(); });

// 不好 - 手动管理线程
thread t(compute);
t.join();
```

### CP.8: 不要使用 `volatile` 进行同步
```cpp
// 不好
volatile bool ready = false;

// 好
atomic<bool> ready{false};
```

### CP.20: 使用 RAII，永远不要直接使用 `lock()`/`unlock()`
```cpp
// 好
void f() {
    lock_guard<mutex> lock(m);
    // 使用共享数据
}  // 自动解锁

// 不好
void f() {
    m.lock();
    // 使用共享数据
    m.unlock();  // 可能忘记或异常时跳过
}
```

### CP.21: 使用 `std::lock()` 或 `std::scoped_lock` 获取多个互斥锁
```cpp
// 好 - 避免死锁
scoped_lock lock(m1, m2);

// 不好 - 可能死锁
lock_guard lock1(m1);
lock_guard lock2(m2);
```

### CP.22: 持有锁时永远不要调用未知代码
```cpp
// 不好
lock_guard lock(m);
user_callback();  // 可能做任何事
```

### CP.24: 将线程视为全局容器
- 线程生命周期管理很重要

### CP.25: 优先使用 `gsl::joining_thread` 而非 `std::thread`
- 防止线程泄漏

### CP.26: 不要分离线程
```cpp
// 不好
thread(work).detach();

// 好
thread t(work);
t.join();
```

### CP.31: 在线程之间传递少量数据按值传递，而非按引用或指针
```cpp
// 好
thread t([data = my_data]{ process(data); });

// 不好 - 可能悬挂
thread t([&my_data]{ process(my_data); });
```

### CP.32: 要在不相关的线程之间共享所有权，使用 `shared_ptr`
```cpp
auto data = make_shared<Data>();
thread t1([data]{ use(data); });
thread t2([data]{ use(data); });
```

### CP.41: 最小化线程创建和销毁
- 使用线程池

### CP.42: 不要在没有条件的情况下等待
```cpp
// 好
unique_lock lock(m);
cv.wait(lock, []{ return ready; });

// 不好 - 虚假唤醒
cv.wait(lock);
```

### CP.43: 最小化在临界区中花费的时间
```cpp
// 好
{
    lock_guard lock(m);
    data = shared_data;  // 快速复制
}
process(data);  // 在锁外处理

// 不好
lock_guard lock(m);
process(shared_data);  // 长时间持有锁
```

### CP.44: 记住命名你的 `lock_guard` 和 `unique_lock`
```cpp
// 不好 - 临时对象立即销毁
lock_guard(m);  // 没用！

// 好
lock_guard lock(m);
```

## 错误处理 (Error Handling)

### E.1: 在设计早期制定错误处理策略
- 决定使用异常还是错误码

### E.2: 抛出异常以表示无法执行函数的契约
```cpp
double sqrt(double x) {
    if (x < 0) throw domain_error("sqrt: negative argument");
    return std::sqrt(x);
}
```

### E.3: 仅将异常用于错误处理
- 不要用于正常控制流

### E.5: 让构造函数建立不变式，如果不能则抛出异常
```cpp
class File {
    FILE* f;
public:
    File(const char* name) {
        f = fopen(name, "r");
        if (!f) throw runtime_error("cannot open file");
    }
};
```

### E.6: 使用 RAII 防止资源泄漏
```cpp
void f() {
    auto file = ifstream("data.txt");
    // 即使抛出异常也会关闭
    process(file);
}
```

### E.12: 当因不允许或无法使用异常时，使用 `noexcept`
```cpp
void critical_function() noexcept;
```

### E.13: 永远不要在对象的直接拥有者中抛出异常
- 析构函数不应抛出异常

### E.14: 使用专门设计的用户定义类型作为异常（而非内置类型）
```cpp
// 好
class FileError : public runtime_error { ... };

// 不好
throw "file not found";  // 字符串字面量
```

### E.15: 使用引用从层次结构中捕获异常
```cpp
// 好
try { ... }
catch (const exception& e) { ... }

// 不好 - 切片
catch (exception e) { ... }
```

### E.16: 析构函数、释放、`swap` 和异常类型复制/移动构造永远不应失败
```cpp
~Widget() noexcept;
```

### E.17: 不要尝试在每个函数中捕获每个异常
- 让异常传播

### E.18: 最小化显式 `try`/`catch` 的使用
- 优先使用 RAII

### E.19: 如果合适，使用 `final_action` 对象表示清理
```cpp
auto cleanup = finally([&]{ close(fd); });
```

### E.25: 如果无法抛出异常，模拟 RAII 进行资源管理
```cpp
// 无异常环境
if (!acquire_resource(&r)) return error_code;
auto cleanup = [&]{ release_resource(r); };
```

### E.27: 如果无法抛出异常，系统性地使用错误码
```cpp
error_code process(Data& out);
```

### E.28: 避免基于全局状态的错误处理（如 `errno`）
```cpp
// 不好
int result = some_function();
if (errno) { ... }

// 好
auto [result, error] = some_function();
if (error) { ... }
```

## 常量和不可变性 (Constants)

### Con.1: 默认情况下，使对象不可变
```cpp
const int x = 42;
const string name = "widget";
```

### Con.2: 默认情况下，使成员函数为 `const`
```cpp
class Widget {
public:
    int value() const { return value_; }  // 不修改对象
private:
    int value_;
};
```

### Con.3: 默认情况下，通过 `const*` 或 `const&` 传递指针和引用
```cpp
void use(const Widget& w);
void process(const int* data, size_t size);
```

### Con.4: 使用 `const` 定义在构造后值不变的对象
```cpp
const int max_retries = 3;
const auto pi = 3.14159;
```

### Con.5: 对可以在编译时计算的值使用 `constexpr`
```cpp
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

constexpr int f5 = factorial(5);  // 编译时计算
```

## 模板 (Templates)

### T.1: 使用模板提高代码的抽象层次
```cpp
template<typename T>
T max(T a, T b) {
    return a > b ? a : b;
}
```

### T.2: 使用模板表达适用于多种参数类型的算法
```cpp
template<typename Container>
void sort(Container& c) {
    std::sort(c.begin(), c.end());
}
```

### T.3: 使用模板表达容器和范围
```cpp
template<typename T>
class Vector { ... };
```

### T.10: 为所有模板参数指定概念
```cpp
template<typename T>
  requires Sortable<T>
void sort(vector<T>& v);
```

### T.11: 尽可能使用标准概念
```cpp
template<std::copyable T>
void process(T value);
```

### T.40: 使用函数对象向算法传递操作
```cpp
sort(v.begin(), v.end(), [](int a, int b) { return a > b; });
```

### T.41: 仅对概念要求简单的泛型算法使用模板
```cpp
template<typename T>
T square(T x) { return x * x; }
```

### T.42: 使用模板别名简化表示法并隐藏实现细节
```cpp
template<typename T>
using Vec = std::vector<T, MyAllocator<T>>;
```

### T.43: 优先使用 `using` 而非 `typedef` 定义别名
```cpp
// 好
using IntVector = vector<int>;

// 不好
typedef vector<int> IntVector;
```

### T.44: 使用函数模板推导类模板参数类型（如果可行）
```cpp
auto p = make_pair(1, "hello");  // 推导类型
```

### T.46: 要求模板参数至少是半正规的
- 支持复制构造
- 支持析构

### T.47: 避免使用在通用名称上高度可见的无约束模板
```cpp
// 不好 - 太泛化
template<typename T> void process(T);

// 好 - 有约束
template<typename T>
  requires Processable<T>
void process(T);
```

### T.48: 如果编译器不支持概念，使用 `enable_if` 伪造它们
```cpp
template<typename T>
enable_if_t<is_integral_v<T>, T>
square(T x) { return x * x; }
```

### T.49: 尽可能避免类型擦除
- 有性能成本

## 按主题快速查找

### 智能指针
- R.20: 使用 `unique_ptr` 或 `shared_ptr` 表示所有权
- R.21: 优先使用 `unique_ptr` 而非 `shared_ptr`
- R.22: 使用 `make_shared()` 创建 `shared_ptr`
- R.23: 使用 `make_unique()` 创建 `unique_ptr`
- F.7: 一般使用 `T*` 或 `T&` 而非智能指针

### RAII
- R.1: 使用资源句柄和 RAII 自动管理资源
- E.6: 使用 RAII 防止资源泄漏
- CP.20: 使用 RAII，永远不要直接 `lock()`/`unlock()`

### 初始化
- ES.20: 总是初始化对象
- ES.22: 在有值之前不要声明变量
- ES.23: 优先使用 `{}` 初始化器
- C.45: 使用成员初始化器
- C.47: 按声明顺序初始化

### const 和 constexpr
- P.10: 优先使用不可变数据
- Con.1: 默认使对象不可变
- Con.2: 默认使成员函数为 `const`
- Con.5: 使用 `constexpr` 用于编译时值

### 现代 C++ 特性
- ES.11: 使用 `auto` 避免冗余
- ES.47: 使用 `nullptr` 而非 `0` 或 `NULL`
- ES.71: 优先使用范围 for
- T.43: 优先使用 `using` 而非 `typedef`

### 异常安全
- E.2: 抛出异常表示无法满足契约
- E.5: 让构造函数建立不变式
- E.6: 使用 RAII
- E.16: 析构函数等永远不应失败
- E.18: 最小化显式 `try`/`catch`

### 并发
- CP.2: 避免数据竞争
- CP.20: 使用 RAII 管理锁
- CP.21: 使用 `std::lock()` 获取多个锁
- CP.42: 不要在没有条件的情况下等待
- CP.43: 最小化临界区时间
