# 常见违规和修复示例

本文档收集了在 C++ 代码中最常见的 Core Guidelines 违规模式及其修复方法。

## 目录

- [内存管理违规](#内存管理违规)
- [类型安全违规](#类型安全违规)
- [接口设计违规](#接口设计违规)
- [资源管理违规](#资源管理违规)
- [并发违规](#并发违规)
- [异常安全违规](#异常安全违规)
- [const 正确性违规](#const-正确性违规)

## 内存管理违规

### 违规 1：使用裸 new/delete

**❌ 违规代码：**
```cpp
void process_data() {
    Widget* w = new Widget();
    w->use();
    delete w;  // 容易忘记，异常不安全
}

class Container {
    Widget* widget;
public:
    Container() : widget(new Widget()) {}
    ~Container() { delete widget; }
    // 忘记定义拷贝构造和赋值运算符！
};
```

**问题说明：**
- 违反 R.11, P.8
- 容易忘记 `delete`
- 异常时不释放
- 拷贝语义错误

**✅ 正确代码：**
```cpp
void process_data() {
    auto w = make_unique<Widget>();
    w->use();
    // 自动销毁
}

class Container {
    unique_ptr<Widget> widget;
public:
    Container() : widget(make_unique<Widget>()) {}
    // 编译器自动生成正确的析构和移动语义
    ~Container() = default;
    Container(Container&&) = default;
    Container& operator=(Container&&) = default;
    // 如果需要拷贝，显式定义
    Container(const Container& other)
        : widget(make_unique<Widget>(*other.widget)) {}
};
```

### 违规 2：手动管理数组

**❌ 违规代码：**
```cpp
void process() {
    int* data = new int[100];

    for (int i = 0; i <= 100; ++i) {  // 缓冲区溢出！
        data[i] = i;
    }

    if (error_condition) {
        return;  // 内存泄漏！
    }

    delete[] data;
}
```

**问题说明：**
- 违反 R.11, Bounds.1
- 缓冲区溢出
- 内存泄漏
- 忘记 `[]`

**✅ 正确代码：**
```cpp
void process() {
    vector<int> data(100);

    for (size_t i = 0; i < data.size(); ++i) {  // 安全
        data[i] = i;
    }

    if (error_condition) {
        return;  // 自动清理
    }
    // data 自动销毁
}

// 或者使用 std::array（固定大小）
void process_fixed() {
    array<int, 100> data;

    for (auto& value : data) {  // 更安全
        value = /* ... */;
    }
}
```

### 违规 3：悬挂指针

**❌ 违规代码：**
```cpp
int* get_value() {
    int x = 42;
    return &x;  // 返回局部变量的地址！
}

string& get_name() {
    return string("temporary");  // 返回临时对象的引用！
}

void use() {
    int* p = get_value();
    *p = 10;  // 未定义行为！
}
```

**问题说明：**
- 违反 F.43
- 返回悬挂指针/引用
- 访问已销毁对象

**✅ 正确代码：**
```cpp
int get_value() {
    int x = 42;
    return x;  // 按值返回
}

string get_name() {
    return "temporary";  // 返回值（移动优化）
}

void use() {
    int value = get_value();
    value = 10;  // 安全
}

// 如果需要返回引用，确保生命周期
class Cache {
    string data;
public:
    const string& get() const { return data; }  // 安全：成员引用
};
```

## 类型安全违规

### 违规 4：C 风格强制转换

**❌ 违规代码：**
```cpp
double d = 3.14;
int i = (int)d;  // C 风格，隐藏意图

Base* base = get_object();
Derived* derived = (Derived*)base;  // 不安全！

const int x = 42;
int* p = (int*)&x;  // 去除 const！
```

**问题说明：**
- 违反 ES.49, Type.4
- 隐藏转换意图
- 无运行时检查
- 可能去除 const

**✅ 正确代码：**
```cpp
double d = 3.14;
int i = static_cast<int>(d);  // 明确数值转换

Base* base = get_object();
Derived* derived = dynamic_cast<Derived*>(base);  // 运行时检查
if (derived) {  // 检查转换是否成功
    // 使用 derived
}

// 避免去除 const
// 如果真的需要（极少情况），使用 const_cast 并注释原因
```

### 违规 5：使用 NULL 或 0 表示空指针

**❌ 违规代码：**
```cpp
Widget* w = NULL;  // 或 0
if (w == NULL) { /* ... */ }

void f(int);
void f(Widget*);

f(NULL);  // 歧义！可能调用 f(int)
```

**问题说明：**
- 违反 ES.47
- NULL 是宏
- 重载解析问题

**✅ 正确代码：**
```cpp
Widget* w = nullptr;
if (w == nullptr) { /* ... */ }
// 或者简写
if (!w) { /* ... */ }

void f(int);
void f(Widget*);

f(nullptr);  // 明确调用 f(Widget*)
```

### 违规 6：未检查的窄化转换

**❌ 违规代码：**
```cpp
int64_t large = 1000000000000;
int small = large;  // 截断！

double d = 3.9;
int i = d;  // 丢失小数部分

unsigned int u = -1;  // 意外的大数值
```

**问题说明：**
- 违反 ES.46
- 数据丢失
- 溢出

**✅ 正确代码：**
```cpp
int64_t large = 1000000000000;
if (large > INT_MAX || large < INT_MIN) {
    // 处理溢出
}
int small = static_cast<int>(large);  // 明确转换

double d = 3.9;
int i = static_cast<int>(d);  // 显式截断

// 使用 GSL 的窄化检查
int safe = gsl::narrow<int>(large);  // 溢出时抛异常
```

## 接口设计违规

### 违规 7：所有权不明确

**❌ 违规代码：**
```cpp
// 谁负责删除返回的指针？
Widget* create_widget();

// 这个函数会删除指针吗？
void process(Widget* w);

// 调用者困惑
Widget* w = create_widget();
process(w);
// 应该 delete w 吗？
```

**问题说明：**
- 违反 I.11
- 所有权语义不明确
- 容易内存泄漏或双重释放

**✅ 正确代码：**
```cpp
// 明确转移所有权
unique_ptr<Widget> create_widget();

// 借用，不拥有
void process(Widget& w);

// 获取所有权
void consume(unique_ptr<Widget> w);

// 使用
auto w = create_widget();  // 拥有所有权
process(*w);                // 借用
consume(move(w));           // 转移所有权
// w 现在为空
```

### 违规 8：数组作为指针传递

**❌ 违规代码：**
```cpp
void process(int* data, size_t size);  // 容易不匹配

int data[100];
process(data, 100);  // 手动传递大小
process(data, 50);   // 可能错误
```

**问题说明：**
- 违反 I.13
- 丢失大小信息
- 容易传递错误大小

**✅ 正确代码：**
```cpp
// C++20: std::span
void process(span<int> data);

int data[100];
process(data);  // 自动推导大小

vector<int> v = {1, 2, 3};
process(v);  // 也可以

// C++17 之前：使用容器
void process(const vector<int>& data);

// 或模板
template<size_t N>
void process(array<int, N>& data);
```

### 违规 9：弱类型接口

**❌ 违规代码：**
```cpp
// 不清楚单位是什么
void sleep_for(int duration);
void set_timeout(double time);

sleep_for(5);  // 秒？毫秒？
set_timeout(1.5);  // 什么单位？

// 布尔陷阱
void create_file(const string& name, bool overwrite);
create_file("data.txt", true);  // true 代表什么？
```

**问题说明：**
- 违反 I.4
- 接口不明确
- 容易误用

**✅ 正确代码：**
```cpp
// 使用强类型
void sleep_for(chrono::milliseconds duration);
void set_timeout(chrono::seconds time);

sleep_for(5ms);
sleep_for(chrono::milliseconds(5));
set_timeout(1.5s);

// 使用枚举类
enum class FileMode { CreateNew, Overwrite };
void create_file(const string& name, FileMode mode);
create_file("data.txt", FileMode::Overwrite);  // 清晰

// 或者使用命名参数（通过结构体）
struct FileOptions {
    bool overwrite = false;
    bool create_dirs = false;
};
void create_file(const string& name, FileOptions options = {});
create_file("data.txt", {.overwrite = true});  // C++20
```

## 资源管理违规

### 违规 10：忘记释放资源

**❌ 违规代码：**
```cpp
void process_file(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) return;

    // 处理文件...

    if (error) {
        return;  // 忘记 fclose！
    }

    fclose(file);
}

void use_mutex() {
    mutex.lock();

    do_work();  // 如果抛异常？

    mutex.unlock();  // 可能不执行
}
```

**问题说明：**
- 违反 P.8, R.1
- 资源泄漏
- 异常不安全

**✅ 正确代码：**
```cpp
void process_file(const string& filename) {
    ifstream file(filename);
    if (!file) throw runtime_error("Cannot open file");

    // 处理文件...

    if (error) {
        throw runtime_error("Error");  // 文件自动关闭
    }
    // 文件自动关闭
}

// 或自定义 RAII 包装器
class FileHandle {
    FILE* file;
public:
    explicit FileHandle(const char* filename, const char* mode)
        : file(fopen(filename, mode)) {
        if (!file) throw runtime_error("Cannot open file");
    }
    ~FileHandle() { if (file) fclose(file); }
    FileHandle(const FileHandle&) = delete;
    FILE* get() { return file; }
};

void use_mutex() {
    lock_guard<mutex> lock(mutex);  // RAII

    do_work();  // 异常安全

    // 自动解锁
}
```

### 违规 11：五法则不完整

**❌ 违规代码：**
```cpp
class Resource {
    int* data;
public:
    Resource() : data(new int[100]) {}
    ~Resource() { delete[] data; }
    // 缺少拷贝构造和赋值！
};

Resource r1;
Resource r2 = r1;  // 浅拷贝！双重释放！
```

**问题说明：**
- 违反 C.21
- 浅拷贝导致双重释放
- 移动语义缺失

**✅ 正确代码：**
```cpp
class Resource {
    unique_ptr<int[]> data;
public:
    Resource() : data(make_unique<int[]>(100)) {}

    // 五法则
    ~Resource() = default;

    Resource(const Resource& other)
        : data(make_unique<int[]>(100)) {
        copy(other.data.get(), other.data.get() + 100, data.get());
    }

    Resource& operator=(const Resource& other) {
        if (this != &other) {
            auto new_data = make_unique<int[]>(100);
            copy(other.data.get(), other.data.get() + 100, new_data.get());
            data = move(new_data);
        }
        return *this;
    }

    Resource(Resource&&) noexcept = default;
    Resource& operator=(Resource&&) noexcept = default;
};

// 或者禁止拷贝（更常见）
class NonCopyableResource {
    unique_ptr<int[]> data;
public:
    NonCopyableResource() : data(make_unique<int[]>(100)) {}

    ~NonCopyableResource() = default;

    NonCopyableResource(const NonCopyableResource&) = delete;
    NonCopyableResource& operator=(const NonCopyableResource&) = delete;

    NonCopyableResource(NonCopyableResource&&) noexcept = default;
    NonCopyableResource& operator=(NonCopyableResource&&) noexcept = default;
};
```

## 并发违规

### 违规 12：数据竞争

**❌ 违规代码：**
```cpp
class Counter {
    int count = 0;
public:
    void increment() {
        ++count;  // 数据竞争！
    }

    int get() const {
        return count;  // 数据竞争！
    }
};

// 多线程调用
Counter counter;
thread t1([&] { counter.increment(); });
thread t2([&] { counter.increment(); });
```

**问题说明：**
- 违反 CP.2
- 多线程访问共享可变数据
- 未定义行为

**✅ 正确代码：**
```cpp
// 方案 1：使用互斥锁
class Counter {
    int count = 0;
    mutable mutex m;
public:
    void increment() {
        lock_guard<mutex> lock(m);
        ++count;
    }

    int get() const {
        lock_guard<mutex> lock(m);
        return count;
    }
};

// 方案 2：使用原子变量（更高效）
class Counter {
    atomic<int> count{0};
public:
    void increment() {
        ++count;  // 原子操作
    }

    int get() const {
        return count.load();
    }
};
```

### 违规 13：死锁

**❌ 违规代码：**
```cpp
mutex m1, m2;

void thread1() {
    lock_guard<mutex> lock1(m1);
    // ... 一些操作
    lock_guard<mutex> lock2(m2);  // 死锁风险！
    // 使用共享资源
}

void thread2() {
    lock_guard<mutex> lock2(m2);
    // ... 一些操作
    lock_guard<mutex> lock1(m1);  // 以相反顺序获取！
    // 使用共享资源
}
```

**问题说明：**
- 违反 CP.21
- 以不同顺序获取多个锁
- 可能死锁

**✅ 正确代码：**
```cpp
mutex m1, m2;

// 方案 1：使用 std::scoped_lock（C++17）
void thread1() {
    scoped_lock lock(m1, m2);  // 原子获取，避免死锁
    // 使用共享资源
}

void thread2() {
    scoped_lock lock(m1, m2);  // 顺序无关紧要
    // 使用共享资源
}

// 方案 2：使用 std::lock（C++11）
void thread1() {
    unique_lock<mutex> lock1(m1, defer_lock);
    unique_lock<mutex> lock2(m2, defer_lock);
    lock(lock1, lock2);  // 原子获取
    // 使用共享资源
}
```

### 违规 14：忘记同步

**❌ 违规代码：**
```cpp
bool ready = false;
int data = 0;

void producer() {
    data = 42;
    ready = true;  // 无同步！
}

void consumer() {
    while (!ready) {  // 可能永远看不到 ready = true
        // 等待
    }
    cout << data;  // 可能看到旧值
}
```

**问题说明：**
- 违反 CP.2
- 缺少内存同步
- 编译器/CPU 可能重排序

**✅ 正确代码：**
```cpp
// 方案 1：使用原子变量
atomic<bool> ready{false};
int data = 0;

void producer() {
    data = 42;
    ready.store(true, memory_order_release);  // 同步
}

void consumer() {
    while (!ready.load(memory_order_acquire)) {  // 同步
        this_thread::yield();
    }
    cout << data;  // 保证看到最新值
}

// 方案 2：使用互斥锁
mutex m;
bool ready = false;
int data = 0;

void producer() {
    lock_guard<mutex> lock(m);
    data = 42;
    ready = true;
}

void consumer() {
    unique_lock<mutex> lock(m);
    while (!ready) {
        lock.unlock();
        this_thread::yield();
        lock.lock();
    }
    cout << data;
}

// 方案 3：使用条件变量（更好）
mutex m;
condition_variable cv;
bool ready = false;
int data = 0;

void producer() {
    {
        lock_guard<mutex> lock(m);
        data = 42;
        ready = true;
    }
    cv.notify_one();
}

void consumer() {
    unique_lock<mutex> lock(m);
    cv.wait(lock, [] { return ready; });  // 等待条件
    cout << data;
}
```

## 异常安全违规

### 违规 15：析构函数抛异常

**❌ 违规代码：**
```cpp
class Resource {
public:
    ~Resource() {
        if (cleanup_failed()) {
            throw runtime_error("Cleanup failed");  // 危险！
        }
    }
};

void use() {
    Resource r;
    throw exception();  // 析构时又抛异常 -> std::terminate
}
```

**问题说明：**
- 违反 C.36, E.16
- 析构时抛异常导致 terminate
- 栈展开时的异常

**✅ 正确代码：**
```cpp
class Resource {
public:
    ~Resource() noexcept {  // 明确标记
        try {
            if (cleanup_failed()) {
                // 记录错误，但不抛异常
                log_error("Cleanup failed");
            }
        } catch (...) {
            // 捕获所有异常
        }
    }
};

// 如果清理失败需要通知，使用显式方法
class Resource {
    bool closed = false;
public:
    void close() {  // 可以抛异常
        if (!closed) {
            cleanup();  // 可能抛异常
            closed = true;
        }
    }

    ~Resource() noexcept {
        if (!closed) {
            try {
                cleanup();
            } catch (...) {
                // 记录但不抛出
            }
        }
    }
};
```

### 违规 16：异常导致资源泄漏

**❌ 违规代码：**
```cpp
void process() {
    Resource* r = acquire_resource();

    use_resource(r);  // 可能抛异常

    release_resource(r);  // 可能不执行
}

void process_two() {
    Resource* r1 = acquire_resource();
    Resource* r2 = acquire_resource();  // 如果这里抛异常？

    use_resources(r1, r2);

    release_resource(r2);
    release_resource(r1);
}
```

**问题说明：**
- 违反 E.6
- 异常时资源不释放
- 异常安全保证弱

**✅ 正确代码：**
```cpp
void process() {
    auto r = ResourceHandle(acquire_resource());  // RAII

    use_resource(r.get());  // 异常安全

    // 自动释放
}

void process_two() {
    auto r1 = ResourceHandle(acquire_resource());
    auto r2 = ResourceHandle(acquire_resource());  // 异常安全

    use_resources(r1.get(), r2.get());

    // 自动释放
}

// RAII 包装器
class ResourceHandle {
    Resource* resource;
public:
    explicit ResourceHandle(Resource* r) : resource(r) {}
    ~ResourceHandle() { release_resource(resource); }

    ResourceHandle(const ResourceHandle&) = delete;
    ResourceHandle& operator=(const ResourceHandle&) = delete;

    Resource* get() { return resource; }
};
```

## const 正确性违规

### 违规 17：应该 const 但不是

**❌ 违规代码：**
```cpp
class Widget {
    int value;
public:
    int get_value() {  // 应该是 const
        return value;
    }

    void print() {  // 应该是 const
        cout << value;
    }
};

void use(Widget& w) {  // 应该是 const&
    cout << w.get_value();
}

int compute(vector<int>& data) {  // 应该是 const&
    return accumulate(data.begin(), data.end(), 0);
}
```

**问题说明：**
- 违反 Con.2, Con.3
- 无法用于 const 对象
- 接口不明确

**✅ 正确代码：**
```cpp
class Widget {
    int value;
public:
    int get_value() const {  // const 成员函数
        return value;
    }

    void print() const {
        cout << value;
    }
};

void use(const Widget& w) {  // const 引用
    cout << w.get_value();
}

int compute(const vector<int>& data) {  // const 引用
    return accumulate(data.begin(), data.end(), 0);
}
```

### 违规 18：去除 const

**❌ 违规代码：**
```cpp
void modify(const string& str) {
    string& mutable_str = const_cast<string&>(str);
    mutable_str += " modified";  // 违反 const 契约！
}

const int x = 42;
int* p = const_cast<int*>(&x);
*p = 100;  // 未定义行为！
```

**问题说明：**
- 违反 ES.50
- 破坏 const 保证
- 未定义行为

**✅ 正确代码：**
```cpp
// 如果需要修改，不要接受 const
void modify(string& str) {
    str += " modified";
}

// 或者返回新值
string modify(const string& str) {
    return str + " modified";
}

// 绝对避免修改 const 对象
```

## 总结：最常见的 10 个违规

1. **使用裸 new/delete** → 使用智能指针
2. **所有权不明确** → 使用 `unique_ptr`/`shared_ptr`/引用明确所有权
3. **缺少 const** → 添加 `const` 到成员函数和参数
4. **数据竞争** → 使用互斥锁或原子变量
5. **异常不安全** → 使用 RAII
6. **C 风格强制转换** → 使用 C++ 转换
7. **手动资源管理** → 使用 RAII 包装器
8. **五法则不完整** → 定义或删除全部五个函数
9. **使用 NULL** → 使用 `nullptr`
10. **手写循环** → 使用标准算法或范围 for

修复这些最常见的违规将大大提高代码质量和安全性。
