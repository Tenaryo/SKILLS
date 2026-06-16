# C++ 代码审查指南

审查 C++ 源码变更时的审查模块索引。按优先级分层，逐层检查。每个模块简要说明审查方向。

> ⚠️ **本指南用于 Reviewer 内部推理，不得作为输出模板逐条罗列"未发现问题"。** 输出只包含：发现的问题、值得表扬的亮点、审查结论。

---

## P0 — 必须审查（影响正确性）

### Correctness
逻辑是否正确实现了设计意图。对照架构师的需求逐项核对。关注边界条件（空、零、极值）、错误路径、assert/precondition 是否正确。

### Undefined Behavior
有符号整数溢出、除零、越界访问、未初始化读取、严格别名违规、move 后访问、修改关联容器键、ODR 违规、`offsetof` 用于非标准布局类型。

### Thread Safety
数据竞争、死锁（锁顺序不一致）、条件变量虚假唤醒未用 while 循环、volatile 误用于同步、`shared_ptr` 控制块并发拷贝、无锁代码 memory order 选择是否正确。

### Lifetime
`string_view` / `span` / 引用 / 迭代器是否指向已销毁对象。容器 resize 后迭代器/指针是否仍被使用。返回局部变量引用。所有权是否清晰（返回的裸指针谁负责释放）。

---

## P1 — 强烈建议审查（影响质量和可信度）

### Testing
是否有边界测试、错误路径测试。测试是否真正验证了行为（非虚假通过）。测试间是否独立。是否有回归测试。Bug 修复是否附带对应的复现测试。

### Performance
**Hot Path Gate：先确认代码是否位于 hot path。** 不是 hot path → 优先可维护性。是 hot path 才进入性能审查。

**Performance Evidence Rule：性能建议必须有依据。** 至少满足其一：benchmark 数据、profiler 结果、complexity analysis、cache/memory model 分析、明确的 hot path 说明（调用频率/数据量级）。无法满足的标记为"待验证风险（Unvalidated Risk）"，不得标 Major/Blocker。

审查方向：不必要的拷贝、O(n²) 嵌套、容器扩容未 reserve、热路径内存分配、虚函数在热路径、缓存局部性差。

### Architecture
是否与架构师批准的设计决策一致。模块边界是否正确。接口是否破坏现有契约。是否引入了循环依赖。新增代码是否放在了正确的模块。

---

## P2 — 建议审查（影响长期可维护性）

### Maintainability
函数是否过长/嵌套过深。是否有重复代码可提取。命名是否一致。头文件 include 是否精简、是否有循环依赖。错误处理策略是否一致。异常安全保证。RAII 是否正确使用。

### Modern C++
评估是否存在更现代且**收益明确**的替代方案。注意：不盲目替换——HFT、嵌入式、ABI 边界、plugin interface 等场景中"传统"写法可能是刻意选择。关注点：裸 new/delete → 智能指针、C 风格转换 → 命名 cast、`#define` → constexpr、`NULL` → nullptr、`typedef` → using、裸 enum → enum class。

---

## P3 — 可选审查（偏好与风格）

### Style
命名风格是否符合项目约定。`const` 正确性。`[[nodiscard]]` / `noexcept` 标记。`std::endl` vs `'\n'`。魔数是否应命名。注释是否过时或无用等等。
