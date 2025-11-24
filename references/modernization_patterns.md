# C++ 现代化模式

将传统 C++ 代码升级到现代 C++ (C++11/14/17/20) 的模式和技巧。

## 目录

- [内存管理现代化](#内存管理现代化)
- [类型系统现代化](#类型系统现代化)
- [容器和算法现代化](#容器和算法现代化)
- [函数和Lambda现代化](#函数和lambda现代化)
- [并发现代化](#并发现代化)
- [错误处理现代化](#错误处理现代化)
- [类设计现代化](#类设计现代化)
- [常量和编译期计算现代化](#常量和编译期计算现代化)

## 内存管理现代化

### 模式 1：裸指针 → 智能指针

**传统 (C++03)：**
```cpp
class Manager {
    Widget* widget;
public:
    Manager() {
        widget = new Widget();
    }

    ~Manager() {
        delete widget;
    }

    // 需要手动定义拷贝构造函数和赋值运算符
    Manager(const Manager& other) {
        widget = new Widget(*other.widget);
    }

    Manager& operator=(const Manager& other) {
        if (this != &other) {
            delete widget;
            widget = new Widget(*other.widget);
        }
        return *this;
    }
};
```

**现代 (C++11+)：**
```cpp
class Manager {
    unique_ptr<Widget> widget;
public:
    Manager() : widget(make_unique<Widget>()) {}

    // 编译器自动生成正确的析构、移动语义
    ~Manager() = default;
    Manager(Manager&&) = default;
    Manager& operator=(Manager&&) = default;

    // 如果需要拷贝，显式定义
    Manager(const Manager& other)
        : widget(make_unique<Widget>(*other.widget)) {}

    Manager& operator=(const Manager& other) {
        if (this != &other) {
            widget = make_unique<Widget>(*other.widget);
        }
        return *this;
    }
};
```

**要点：**
- 使用 `unique_ptr` 表示独占所有权
- 使用 `shared_ptr` 表示共享所有权
- 使用 `make_unique`/`make_shared` 创建
- 让编译器生成特殊成员函数

### 模式 2：手动资源管理 → RAII

**传统：**
```cpp
void process_file(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        return;  // 错误处理
    }

    char buffer[1024];
    // 处理文件...

    fclose(file);  // 容易忘记，异常时不执行
}
```

**现代：**
```cpp
void process_file(const string& filename) {
    ifstream file(filename);
    if (!file) {
        throw runtime_error("Cannot open file");
    }

    string line;
    while (getline(file, line)) {
        // 处理...
    }
    // 文件自动关闭，异常安全
}

// 或者使用自定义 RAII 包装器
class FileHandle {
    FILE* file;
public:
    explicit FileHandle(const char* filename, const char* mode)
        : file(fopen(filename, mode)) {
        if (!file) throw runtime_error("Cannot open file");
    }

    ~FileHandle() { if (file) fclose(file); }

    // 禁止拷贝
    FileHandle(const FileHandle&) = delete;
    FileHandle& operator=(const FileHandle&) = delete;

    // 允许移动
    FileHandle(FileHandle&& other) noexcept : file(other.file) {
        other.file = nullptr;
    }

    FILE* get() { return file; }
};
```

### 模式 3：数组 → std::array 或 std::vector

**传统：**
```cpp
void process() {
    int* data = new int[100];

    for (int i = 0; i < 100; ++i) {
        data[i] = i * 2;
    }

    // 使用 data...

    delete[] data;  // 容易忘记
}

// 或者 C 风格数组
void process_c_array() {
    int data[100];  // 大小必须是编译期常量

    for (int i = 0; i < 100; ++i) {
        data[i] = i * 2;
    }

    // 传递给函数时退化为指针，丢失大小信息
    use_array(data);  // void use_array(int* arr)
}
```

**现代：**
```cpp
// 固定大小：std::array
void process_fixed() {
    array<int, 100> data;  // 栈上分配，零开销

    for (size_t i = 0; i < data.size(); ++i) {
        data[i] = i * 2;
    }

    // 或者使用范围 for
    for (int& value : data) {
        value = /* ... */;
    }

    // 传递时保留大小信息
    use_array(data);  // void use_array(array<int, 100>& arr)
}

// 动态大小：std::vector
void process_dynamic(size_t count) {
    vector<int> data(count);  // 自动管理内存

    for (size_t i = 0; i < data.size(); ++i) {
        data[i] = i * 2;
    }

    // data 自动销毁
}

// 接受任意大小数组：std::span (C++20)
void use_array(span<int> data) {
    for (int value : data) {
        // ...
    }
}
```

## 类型系统现代化

### 模式 4：NULL/0 → nullptr

**传统：**
```cpp
Widget* widget = NULL;  // 或 0
if (widget == NULL) { /* ... */ }

void f(int);
void f(char*);

f(NULL);  // 歧义！可能调用 f(int)
```

**现代 (C++11+)：**
```cpp
Widget* widget = nullptr;
if (widget == nullptr) { /* ... */ }
// 或者简写
if (!widget) { /* ... */ }

void f(int);
void f(char*);

f(nullptr);  // 明确调用 f(char*)
```

### 模式 5：typedef → using

**传统：**
```cpp
typedef std::vector<int> IntVector;
typedef std::map<std::string, int> StringIntMap;

// 模板别名需要技巧
template<typename T>
struct MyAllocator { /* ... */ };

template<typename T>
struct Vec {
    typedef std::vector<T, MyAllocator<T>> type;
};

Vec<int>::type v;  // 不直观
```

**现代 (C++11+)：**
```cpp
using IntVector = vector<int>;
using StringIntMap = map<string, int>;

// 模板别名
template<typename T>
using Vec = vector<T, MyAllocator<T>>;

Vec<int> v;  // 清晰直观
```

### 模式 6：auto 类型推导

**传统：**
```cpp
std::vector<std::string>::iterator it = vec.begin();
std::unique_ptr<ComplexType> ptr = std::unique_ptr<ComplexType>(new ComplexType());
std::pair<int, std::string> p = std::make_pair(42, "hello");
```

**现代 (C++11+)：**
```cpp
auto it = vec.begin();  // 类型显而易见
auto ptr = make_unique<ComplexType>();  // 避免重复
auto p = make_pair(42, "hello"s);  // 简洁

// 保持 const 和引用
const auto& value = expensive_function();
auto& ref = mutable_value;
```

**注意：** 不要过度使用 `auto`，在类型不明显时显式声明更好。

### 模式 7：C 风格强制转换 → C++ 风格转换

**传统：**
```cpp
double d = 3.14;
int i = (int)d;  // C 风格

Base* base = get_object();
Derived* derived = (Derived*)base;  // 危险！

const int x = 42;
int* p = (int*)&x;  // 去除 const
```

**现代：**
```cpp
double d = 3.14;
int i = static_cast<int>(d);  // 明确意图

Base* base = get_object();
Derived* derived = dynamic_cast<Derived*>(base);  // 运行时检查
if (derived) {  // 检查转换是否成功
    // 使用 derived
}

// 避免去除 const
// const_cast 应该极少使用
```

**转换选择指南：**
- `static_cast`：编译时检查的类型转换
- `dynamic_cast`：运行时类型检查（多态类型）
- `const_cast`：添加/移除 const（尽量避免）
- `reinterpret_cast`：低级类型重解释（尽量避免）

## 容器和算法现代化

### 模式 8：手写循环 → 标准算法

**传统：**
```cpp
// 查找元素
int find_index(const vector<int>& v, int target) {
    for (size_t i = 0; i < v.size(); ++i) {
        if (v[i] == target) {
            return i;
        }
    }
    return -1;
}

// 变换
vector<int> transform_data(const vector<int>& input) {
    vector<int> result;
    for (size_t i = 0; i < input.size(); ++i) {
        result.push_back(input[i] * 2);
    }
    return result;
}

// 累加
int sum(const vector<int>& v) {
    int total = 0;
    for (size_t i = 0; i < v.size(); ++i) {
        total += v[i];
    }
    return total;
}
```

**现代 (C++11+)：**
```cpp
// 查找元素
auto find_element(const vector<int>& v, int target) {
    return find(v.begin(), v.end(), target);
}

// 或者检查是否存在
bool contains(const vector<int>& v, int target) {
    return find(v.begin(), v.end(), target) != v.end();
}

// 变换
vector<int> transform_data(const vector<int>& input) {
    vector<int> result;
    result.reserve(input.size());  // 预分配
    transform(input.begin(), input.end(),
              back_inserter(result),
              [](int x) { return x * 2; });
    return result;
}

// 累加
int sum(const vector<int>& v) {
    return accumulate(v.begin(), v.end(), 0);
}

// C++20: ranges
auto sum_cpp20(const vector<int>& v) {
    return ranges::fold_left(v, 0, plus{});
}
```

### 模式 9：迭代器循环 → 范围 for

**传统：**
```cpp
vector<string> names = get_names();

// 读取
for (vector<string>::const_iterator it = names.begin();
     it != names.end(); ++it) {
    cout << *it << '\n';
}

// 修改
for (vector<string>::iterator it = names.begin();
     it != names.end(); ++it) {
    *it = to_upper(*it);
}
```

**现代 (C++11+)：**
```cpp
vector<string> names = get_names();

// 读取
for (const auto& name : names) {
    cout << name << '\n';
}

// 修改
for (auto& name : names) {
    name = to_upper(name);
}

// 只需要值（小对象）
for (auto value : small_values) {
    process(value);
}
```

### 模式 10：初始化列表

**传统：**
```cpp
vector<int> v;
v.push_back(1);
v.push_back(2);
v.push_back(3);

map<string, int> m;
m["one"] = 1;
m["two"] = 2;
m["three"] = 3;
```

**现代 (C++11+)：**
```cpp
vector<int> v = {1, 2, 3};
// 或者
vector<int> v{1, 2, 3};

map<string, int> m = {
    {"one", 1},
    {"two", 2},
    {"three", 3}
};
```

## 函数和Lambda现代化

### 模式 11：函数对象 → Lambda

**传统：**
```cpp
struct MultiplyBy {
    int factor;
    explicit MultiplyBy(int f) : factor(f) {}
    int operator()(int x) const { return x * factor; }
};

vector<int> values = {1, 2, 3, 4, 5};
int factor = 10;
transform(values.begin(), values.end(), values.begin(),
          MultiplyBy(factor));
```

**现代 (C++11+)：**
```cpp
vector<int> values = {1, 2, 3, 4, 5};
int factor = 10;
transform(values.begin(), values.end(), values.begin(),
          [factor](int x) { return x * factor; });

// C++14: 泛型 lambda
transform(values.begin(), values.end(), values.begin(),
          [factor](auto x) { return x * factor; });
```

### 模式 12：函数指针 → std::function

**传统：**
```cpp
typedef int (*BinaryOp)(int, int);

int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }

BinaryOp get_operation(bool use_add) {
    return use_add ? add : multiply;
}

// 不能存储 lambda 或函数对象
```

**现代 (C++11+)：**
```cpp
using BinaryOp = function<int(int, int)>;

int add(int a, int b) { return a + b; }
int multiply(int a, int b) { return a * b; }

BinaryOp get_operation(bool use_add) {
    if (use_add) {
        return add;
    } else {
        return [](int a, int b) { return a * b; };
    }
}

// 可以存储任何可调用对象
BinaryOp op1 = add;
BinaryOp op2 = [](int a, int b) { return a * b; };
BinaryOp op3 = multiply;
```

### 模式 13：返回多个值

**传统：**
```cpp
// 方式 1：输出参数
bool parse_int(const string& str, int& result) {
    try {
        result = stoi(str);
        return true;
    } catch (...) {
        return false;
    }
}

int value;
if (parse_int("123", value)) {
    // 使用 value
}

// 方式 2：pair
pair<bool, int> parse_int(const string& str) {
    try {
        return make_pair(true, stoi(str));
    } catch (...) {
        return make_pair(false, 0);
    }
}

pair<bool, int> result = parse_int("123");
if (result.first) {
    int value = result.second;
}
```

**现代 (C++17+)：**
```cpp
// 使用 optional
optional<int> parse_int(const string& str) {
    try {
        return stoi(str);
    } catch (...) {
        return nullopt;
    }
}

if (auto value = parse_int("123")) {
    // 使用 *value
}

// 结构化绑定
struct Result {
    bool success;
    int value;
    string error;
};

Result parse_int_detailed(const string& str) {
    try {
        return {true, stoi(str), ""};
    } catch (const exception& e) {
        return {false, 0, e.what()};
    }
}

auto [success, value, error] = parse_int_detailed("123");
if (success) {
    // 使用 value
}
```

## 并发现代化

### 模式 14：线程和同步

**传统 (pthread 或 Windows threads)：**
```cpp
#include <pthread.h>

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
int counter = 0;

void* thread_func(void* arg) {
    pthread_mutex_lock(&mutex);
    ++counter;
    pthread_mutex_unlock(&mutex);
    return NULL;
}

int main() {
    pthread_t thread;
    pthread_create(&thread, NULL, thread_func, NULL);
    pthread_join(thread, NULL);
    pthread_mutex_destroy(&mutex);
}
```

**现代 (C++11+)：**
```cpp
#include <thread>
#include <mutex>

mutex m;
int counter = 0;

void thread_func() {
    lock_guard<mutex> lock(m);  // RAII
    ++counter;
}

int main() {
    thread t(thread_func);
    t.join();
    // mutex 自动销毁
}

// C++17: scoped_lock 用于多个互斥锁
mutex m1, m2;
void safe_function() {
    scoped_lock lock(m1, m2);  // 避免死锁
    // 使用共享资源
}
```

### 模式 15：异步任务

**传统：**
```cpp
// 手动管理线程
int compute_something() {
    // 耗时计算
    return 42;
}

int result;
thread t([&result]() {
    result = compute_something();
});
// 做其他事...
t.join();
// 使用 result
```

**现代 (C++11+)：**
```cpp
// 使用 async 和 future
int compute_something() {
    // 耗时计算
    return 42;
}

future<int> result_future = async(launch::async, compute_something);
// 做其他事...
int result = result_future.get();  // 等待并获取结果
```

### 模式 16：原子操作

**传统：**
```cpp
// 使用互斥锁保护简单操作
mutex m;
int counter = 0;

void increment() {
    lock_guard<mutex> lock(m);
    ++counter;
}
```

**现代 (C++11+)：**
```cpp
// 使用原子变量
atomic<int> counter{0};

void increment() {
    ++counter;  // 原子操作，无需锁
}

// 或者显式指定内存顺序
counter.fetch_add(1, memory_order_relaxed);
```

## 错误处理现代化

### 模式 17：错误码 → 异常

**传统：**
```cpp
enum ErrorCode {
    SUCCESS = 0,
    FILE_NOT_FOUND = 1,
    PERMISSION_DENIED = 2
};

ErrorCode read_file(const char* filename, string& content) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        return FILE_NOT_FOUND;
    }

    // 读取文件...

    fclose(file);
    return SUCCESS;
}

// 使用
string content;
ErrorCode error = read_file("data.txt", content);
if (error != SUCCESS) {
    // 处理错误
}
```

**现代 (C++11+)：**
```cpp
string read_file(const string& filename) {
    ifstream file(filename);
    if (!file) {
        throw runtime_error("Cannot open file: " + filename);
    }

    stringstream buffer;
    buffer << file.rdbuf();
    return buffer.str();
}

// 使用
try {
    string content = read_file("data.txt");
    // 使用 content
} catch (const exception& e) {
    // 处理错误
}
```

### 模式 18：可选值

**传统：**
```cpp
// 使用特殊值表示"无值"
int find_value(const map<string, int>& m, const string& key) {
    auto it = m.find(key);
    if (it != m.end()) {
        return it->second;
    }
    return -1;  // -1 表示未找到，但 -1 可能是有效值
}

// 或者使用指针
int* find_value_ptr(map<string, int>& m, const string& key) {
    auto it = m.find(key);
    if (it != m.end()) {
        return &it->second;
    }
    return nullptr;
}
```

**现代 (C++17+)：**
```cpp
optional<int> find_value(const map<string, int>& m, const string& key) {
    auto it = m.find(key);
    if (it != m.end()) {
        return it->second;
    }
    return nullopt;
}

// 使用
if (auto value = find_value(m, "key")) {
    cout << "Found: " << *value << '\n';
} else {
    cout << "Not found\n";
}

// 或者提供默认值
int value = find_value(m, "key").value_or(0);
```

## 类设计现代化

### 模式 19：五法则（Rule of Five）

**传统 (C++03)：三法则**
```cpp
class Resource {
    int* data;
public:
    // 构造
    Resource() : data(new int[100]) {}

    // 析构
    ~Resource() { delete[] data; }

    // 拷贝构造
    Resource(const Resource& other)
        : data(new int[100]) {
        copy(other.data, other.data + 100, data);
    }

    // 拷贝赋值
    Resource& operator=(const Resource& other) {
        if (this != &other) {
            int* new_data = new int[100];
            copy(other.data, other.data + 100, new_data);
            delete[] data;
            data = new_data;
        }
        return *this;
    }
};
```

**现代 (C++11+)：五法则 + 移动语义**
```cpp
class Resource {
    unique_ptr<int[]> data;
public:
    // 构造
    Resource() : data(make_unique<int[]>(100)) {}

    // 默认析构即可
    ~Resource() = default;

    // 拷贝构造
    Resource(const Resource& other)
        : data(make_unique<int[]>(100)) {
        copy(other.data.get(), other.data.get() + 100, data.get());
    }

    // 拷贝赋值
    Resource& operator=(const Resource& other) {
        if (this != &other) {
            auto new_data = make_unique<int[]>(100);
            copy(other.data.get(), other.data.get() + 100, new_data.get());
            data = move(new_data);
        }
        return *this;
    }

    // 移动构造
    Resource(Resource&&) noexcept = default;

    // 移动赋值
    Resource& operator=(Resource&&) noexcept = default;
};

// 更好：如果不需要拷贝，可以删除拷贝操作
class NonCopyableResource {
    unique_ptr<int[]> data;
public:
    NonCopyableResource() : data(make_unique<int[]>(100)) {}

    ~NonCopyableResource() = default;

    // 删除拷贝
    NonCopyableResource(const NonCopyableResource&) = delete;
    NonCopyableResource& operator=(const NonCopyableResource&) = delete;

    // 默认移动
    NonCopyableResource(NonCopyableResource&&) noexcept = default;
    NonCopyableResource& operator=(NonCopyableResource&&) noexcept = default;
};
```

### 模式 20：成员初始化

**传统：**
```cpp
class Widget {
    int value;
    string name;
    vector<int> data;

public:
    Widget()
        : value(0), name("default"), data() {}

    Widget(int v)
        : value(v), name("default"), data() {}

    Widget(int v, const string& n)
        : value(v), name(n), data() {}
};
```

**现代 (C++11+)：**
```cpp
class Widget {
    int value = 0;  // 默认成员初始化器
    string name = "default";
    vector<int> data;

public:
    Widget() = default;  // 使用成员初始化器

    explicit Widget(int v) : value(v) {}  // 只覆盖需要的

    Widget(int v, const string& n)
        : value(v), name(n) {}
};
```

### 模式 21：委托构造函数

**传统：**
```cpp
class Widget {
    int value;
    string name;

    void init(int v, const string& n) {
        value = v;
        name = n;
        // 其他初始化...
    }

public:
    Widget() {
        init(0, "default");
    }

    Widget(int v) {
        init(v, "default");
    }

    Widget(int v, const string& n) {
        init(v, n);
    }
};
```

**现代 (C++11+)：**
```cpp
class Widget {
    int value;
    string name;

public:
    Widget(int v, const string& n)
        : value(v), name(n) {
        // 共同的初始化逻辑
    }

    Widget() : Widget(0, "default") {}  // 委托

    Widget(int v) : Widget(v, "default") {}  // 委托
};
```

## 常量和编译期计算现代化

### 模式 22：宏 → constexpr

**传统：**
```cpp
#define PI 3.14159
#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define SQUARE(x) ((x) * (x))

int area = PI * SQUARE(radius);  // 宏展开，无类型检查
int max_val = MAX(a++, b);  // 危险！a 可能增加两次
```

**现代 (C++11+)：**
```cpp
constexpr double pi = 3.14159;  // 类型安全

template<typename T>
constexpr T max(T a, T b) {
    return a > b ? a : b;
}

template<typename T>
constexpr T square(T x) {
    return x * x;
}

int area = pi * square(radius);  // 类型安全
int max_val = max(a++, b);  // 清晰的语义
```

### 模式 23：编译期计算

**传统：**
```cpp
// 运行时计算
int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

const int f10 = factorial(10);  // 运行时计算
```

**现代 (C++11+)：**
```cpp
// 编译期计算
constexpr int factorial(int n) {
    return n <= 1 ? 1 : n * factorial(n - 1);
}

constexpr int f10 = factorial(10);  // 编译时计算

// C++14: 更灵活的 constexpr
constexpr int factorial_cpp14(int n) {
    int result = 1;
    for (int i = 2; i <= n; ++i) {
        result *= i;
    }
    return result;
}
```

### 模式 24：const → constexpr

**传统：**
```cpp
const int size = 100;  // 运行时常量（虽然可能被优化）
int array[size];  // 可能不合法（取决于编译器）

const double pi = 3.14159;
const double circumference = 2 * pi * 5;  // 运行时计算
```

**现代 (C++11+)：**
```cpp
constexpr int size = 100;  // 编译期常量
int array[size];  // 合法

constexpr double pi = 3.14159;
constexpr double circumference = 2 * pi * 5;  // 编译期计算
```

## 杂项现代化

### 模式 25：字符串字面量

**传统：**
```cpp
const char* str = "Hello";  // C 风格字符串
string s = string("Hello");  // 冗余
```

**现代 (C++14+)：**
```cpp
auto str = "Hello"s;  // std::string，使用 operator""s
auto s = "Hello"s;    // 直接创建 string

// C++17: string_view（非拥有）
string_view sv = "Hello";  // 零拷贝
```

### 模式 26：枚举

**传统：**
```cpp
enum Color {
    RED,
    GREEN,
    BLUE
};  // 污染命名空间，可以隐式转换为 int

Color c = RED;
int value = c;  // 隐式转换
```

**现代 (C++11+)：**
```cpp
enum class Color {
    Red,
    Green,
    Blue
};  // 强类型，不污染命名空间

Color c = Color::Red;
// int value = c;  // 错误：不能隐式转换
int value = static_cast<int>(c);  // 必须显式转换
```

### 模式 27：变参函数

**传统：**
```cpp
#include <cstdarg>

void print(const char* format, ...) {
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
}

print("Values: %d %d\n", 1, 2);  // 不类型安全
```

**现代 (C++11+)：**
```cpp
// 变参模板
template<typename... Args>
void print(Args&&... args) {
    (cout << ... << args) << '\n';  // C++17 折叠表达式
}

print("Values:", 1, " ", 2);  // 类型安全

// 或者使用 initializer_list（同类型）
void print_ints(initializer_list<int> values) {
    for (int v : values) {
        cout << v << ' ';
    }
    cout << '\n';
}

print_ints({1, 2, 3, 4});
```

## 迁移策略

### 渐进式迁移

1. **从安全关键部分开始**
   - 资源管理：智能指针
   - 并发代码：标准库同步原语
   - 容器：std::array, std::vector

2. **工具辅助**
   - Clang-Tidy: `modernize-*` 检查
   - 自动化重构工具

3. **逐步替换**
   - 不要一次性重写所有代码
   - 每个模块逐步现代化
   - 保持向后兼容接口

4. **测试驱动**
   - 每次修改后运行测试
   - 添加新测试覆盖现代化部分

### 优先级建议

**高优先级（立即修复）：**
- 裸 `new`/`delete` → 智能指针
- 手动资源管理 → RAII
- `NULL` → `nullptr`
- C 风格强制转换 → C++ 转换

**中优先级（逐步迁移）：**
- 手写循环 → 标准算法
- 迭代器循环 → 范围 for
- `typedef` → `using`
- 三法则 → 五法则

**低优先级（新代码采用）：**
- 宏 → `constexpr`
- `const` → `constexpr`
- 枚举 → `enum class`
- 函数对象 → lambda
