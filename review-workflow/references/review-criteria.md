# Review Criteria - C++ Code Review Detailed Standards

各审查维度的详细检查清单和评估标准。

## Table of Contents

- [1. Performance (性能)](#1-performance)
- [2. Modern C++ Style (现代C++风格)](#2-modern-c-style)
- [3. Safety (安全性)](#3-safety)
- [4. Extensibility (可扩展性)](#4-extensibility)
- [5. Code Quality (代码质量)](#5-code-quality)

---

## 1. Performance

### 1.1 内存分配

- [ ] 是否存在热路径上的频繁堆分配（`new`, `malloc`, `std::vector::push_back` 未 reserve）
- [ ] 字符串拼接是否使用 `std::string::reserve` 或 `std::ostringstream`
- [ ] 容器是否预知大小并调用了 `reserve()`
- [ ] 是否可用对象池或自定义分配器替代频繁分配
- [ ] 小对象是否使用 `std::optional` 或栈分配替代堆分配

### 1.2 不必要的拷贝

- [ ] 函数参数是否使用了不必要的值传递（应使用 `const&` 或 `string_view`）
- [ ] 返回值是否使用了不必要的拷贝（应依赖 RVO 或返回 `&&`）
- [ ] 是否有可替换为移动语义的拷贝操作
- [ ] range-for 循环中是否使用了不必要的拷贝 `for (auto x : vec)` 应改为 `for (const auto& x : vec)`

### 1.3 缓存友好性

- [ ] 数据结构是否是 SoA vs AoS 的合理选择
- [ ] 热路径数据是否紧凑排列（避免 cache miss）
- [ ] 是否有不必要的虚函数调用（虚表指针导致缓存行失效）
- [ ] 多线程访问的数据是否避免了 false sharing

### 1.4 算法复杂度

- [ ] 是否有 O(n²) 可优化为 O(n log n) 或 O(n) 的算法
- [ ] 查找操作是否使用了合适的容器（`unordered_map` vs `map`）
- [ ] 排序后是否可以用二分查找替代线性查找
- [ ] 循环中是否有不变量的重复计算

### 1.5 编译期计算

- [ ] 常量是否可用 `constexpr` 或 `consteval`
- [ ] 模板元编程是否可替代运行时分支
- [ ] 查找表是否可编译期生成
- [ ] `if constexpr` 是否可替代 SFINAE 或运行时 if

## 2. Modern C++ Style

### 2.1 C++17 特性

- [ ] `std::optional` 替代指针表示可能缺失的值
- [ ] `std::variant` 替代联合体或类型标签枚举
- [ ] `std::string_view` 替代 `const std::string&` 参数
- [ ] 结构化绑定 `auto [key, value] = pair`
- [ ] `if constexpr` 替代 SFINAE
- [ ] `std::filesystem` 替代平台特定的文件操作
- [ ] 折叠表达式替代递归模板

### 2.2 C++20 特性

- [ ] Concepts 替代 SFINAE 和 `static_assert`
- [ ] Ranges 替代手写循环和 `<algorithm>` 组合
- [ ] Coroutines 用于异步代码简化
- [ ] `std::format` 替代 `sprintf` / `std::stringstream`
- [ ] 三路比较运算符 `<=>`
- [ ] `consteval` 和 `constinit`
- [ ] `std::span` 替代指针+长度参数对
- [ ] 指定初始化器 `Named{.x=1, .y=2}`

### 2.3 C++23/26 特性

- [ ] `std::expected` 替代异常或错误码（C++23）
- [ ] `std::print` 替代 `std::cout` / `printf`（C++23）
- [ ] `std::flat_map` / `std::flat_set` 替代小数据量的 map/set（C++23）
- [ ] `std::generator` 用于协程生成器（C++23）
- [ ] Deducing `this` 綈除 const/non-const 成员函数重复（C++23）
- [ ] `std::simd` 数据并行（C++26）
- [ ] 反射（Reflection）元编程（C++26）

### 2.4 通用现代风格

- [ ] 智能指针替代裸指针（`unique_ptr`, `shared_ptr`）
- [ ] RAII 管理所有资源
- [ ] 枚举使用 `enum class` 而非 `enum`
- [ ] `auto` 推导类型（但不滥用）
- [ ] `[[nodiscard]]`, `[[deprecated]]` 等属性标注
- [ ] `std::make_unique` / `std::make_shared` 替代 `new`

## 3. Safety

### 3.1 内存安全

- [ ] 是否存在悬空指针或悬空引用
- [ ] 是否存在 use-after-free
- [ ] 是否存在数组越界访问（应使用 `at()` 或边界检查）
- [ ] 是否存在未初始化的变量
- [ ] 是否存在内存泄漏（`new` 无对应 `delete`）
- [ ] 智能指针是否避免了循环引用

### 3.2 类型安全

- [ ] 是否存在 C 风格强制转换（应用 `static_cast` 等）
- [ ] 是否存在 `void*` 的不当使用
- [ ] 是否存在隐式类型转换导致的精度丢失
- [ ] `reinterpret_cast` 是否确实必要

### 3.3 并发安全

- [ ] 共享数据是否正确加锁
- [ ] 锁的粒度是否合理（不宜过粗或过细）
- [ ] 是否存在死锁风险（锁的获取顺序）
- [ ] 是否存在数据竞争
- [ ] 原子操作是否使用了正确的 memory order

### 3.4 异常安全

- [ ] 析构函数是否 `noexcept`
- [ ] 是否提供了基本异常安全保证
- [ ] 资源获取是否在构造函数中完成（RAII）
- [ ] 移动构造/移动赋值是否 `noexcept`

### 3.5 输入验证

- [ ] 外部输入是否有边界检查
- [ ] 文件路径是否有路径遍历检查
- [ ] 整数运算是否有溢出检查

## 4. Extensibility

### 4.1 模块化

- [ ] 模块职责是否单一明确
- [ ] 模块间依赖是否最小化
- [ ] 头文件是否使用了前向声明减少编译依赖
- [ ] 是否使用了 Pimpl 模式隐藏实现细节

### 4.2 开放-封闭原则

- [ ] 新功能是否可以通过扩展而非修改现有代码添加
- [ ] 是否使用了策略模式、模板方法等消除条件分支
- [ ] 回调/观察者是否替代了紧耦合的调用

### 4.3 配置化

- [ ] 硬编码值是否可提取为配置参数
- [ ] 平台相关代码是否通过抽象隔离
- [ ] 魔法数字是否提取为命名常量

### 4.4 接口设计

- [ ] 接口是否最小化（接口隔离原则）
- [ ] 接口是否稳定，不因实现变化而变化
- [ ] 是否存在过度设计（YAGNI）

## 5. Code Quality

### 5.1 重复代码

- [ ] 是否存在复制粘贴的代码（应提取为公共函数）
- [ ] 相似逻辑是否可通过模板或泛型统一
- [ ] 是否有可通过继承或组合消除的重复

### 5.2 函数复杂度

- [ ] 单函数是否超过 100 行（应拆分）
- [ ] 嵌套层级是否过深（超过 3 层应重构）
- [ ] 圈复杂度是否过高（超过 10 应重构）
- [ ] 参数数量是否过多（超过 4 个应使用结构体）

### 5.3 命名规范

- [ ] 变量名是否清晰表达意图
- [ ] 函数名是否是动词或动词短语
- [ ] 类型名是否是名词
- [ ] 命名是否与代码库中现有风格一致
- [ ] 是否避免了缩写（除公认的如 `idx`, `ptr`, `len`）

### 5.4 注释质量

- [ ] 注释是否解释"为什么"而非"做了什么"
- [ ] 是否存在过时或误导性注释
- [ ] TODO 注释是否有关联的 issue 或时间表
- [ ] 公共 API 是否有文档注释

### 5.5 文件组织

- [ ] 头文件是否有 include guards 或 `#pragma once`
- [ ] 是否使用了前向声明减少头文件依赖
- [ ] 每个文件是否职责单一
- [ ] 头文件包含顺序是否规范（本项目 → 第三方 → 标准库）
