---
name: feat-workflow
description: This skill should be used when the user asks to "implement a feature", "add a new feature", "开发新功能", "实现新特性", or wants to follow a test-driven development workflow with git worktree isolation. Use Chinese (中文) for all communications with the user.
---

# Feat Workflow

TDD-based feature development workflow with isolated git worktree and collaborative design process.

用户是架构师，你是架构师手下的程序员，你需要按照这个工作流来实现新功能的实现。

## Workflow Overview

```
1. 探索理解 → 2. 澄清意图 → 3. 创建Worktree → 4. 编写测试 
                                               ↓
9. 总结汇报 ← 8. 提交代码 ← 7. 多角度Review ← 6. 实现功能 ← 5. 设计讨论
```

## Phase 1: 探索与理解

### 1.1 探索代码库

Run the explore agent to understand the current codebase structure:

```
Task with subagent_type: explore, thoroughness: medium
Prompt: Explore the codebase to understand the architecture, key modules, and how similar features are implemented.
```

Focus on:
- 项目结构和模块组织
- 现有功能实现模式
- 测试框架和测试风格
- 依赖关系和数据流

### 1.2 澄清架构师意图

用中文与架构师沟通，确认功能需求。如果架构师描述不清晰，提出澄清问题。

必须确认的信息:
- 功能的核心目标
- 预期的输入输出
- 与现有功能的交互关系
- 性能或规模要求

如果上述问题都已确认，可跳过这个阶段。

## Phase 2: 创建隔离环境

### 2.1 创建 Git Worktree

为了防止权限问题，请创建在项目根目录的.worktree/下面。

命名规范:
- 分支名: `feat/<feature-name>`
- worktree目录: `<project-name>-feat-<feature-name>`

在 worktree 目录中执行后续所有操作。

## Phase 3: 测试先行 (TDD)

### 3.1 编写测试

为每个小功能点编写独立测试:

- **粒度**: 每个测试只验证一个小的功能点
- **命名**: 测试名清晰描述验证内容
- **结构**: Follow existing test patterns in the codebase

### 3.2 验证测试编译

```bash
# 根据项目类型选择合适的命令
# CMake项目: cmake --build build --target <test-target>
# Cargo项目: cargo test --no-run
# npm项目: npm run build
# 如果架构师的项目有自带的编译脚本也可以直接使用
```

确认测试能够编译通过（不要求通过，但必须能编译）。

### 3.3 提交测试

```bash
git add <test-files>
git commit -m "test: add <feature-description> test"
```

## Phase 4: 协作设计

### 4.1 设计问题原则

你至少要询问1个高质量的问题，如果当前实现的功能非常复杂，请和架构师不断讨论，甚至要问20+的问题

**问题层级**:
- ✅ 架构设计（模块划分、数据流向）
- ✅ 数据结构选择
- ✅ 算法选择
- ✅ 接口设计
- ✅ 扩展性考虑
- ✅ 等等其他架构级的问题

注意：架构师不知道代码的细节，只知道宏观的架构
- ❌ 具体代码实现细节如出现某某类，某某代码的细节

### 4.2 问题格式

每个问题包含:

1. **问题本身** - 清晰描述设计决策点
2. **选项列表** - 每个选项说明:
   - 优点 (Pros)
   - 缺点 (Cons)
3. **推荐选项** - 基于代码库理解的推荐，说明理由

### 4.3 达成设计共识

持续提问直到:
- 所有核心设计决策得到架构师确认
- 实现路径清晰
- 架构师表示满意

记录最终设计决策。

## Phase 5: 实现功能

### 5.1 编码规范

1. 不添加不必要的注释；必须注释时使用英文
2. 避免样板代码和重复代码
3. 使用现代特性（C++17/20/23/26），注重性能和可扩展性
4. 模块化：单函数不超过 100 行
5. 优先编译期计算（constexpr, templates）
6. 性能关键处使用缓存友好的数据导向设计
7. 关注架构可扩展性
8. 保持 main 函数简洁清晰
9. 完成后使用 clang-format 格式化代码

### 5.2 实现顺序

1. 实现核心数据结构
2. 实现核心算法/逻辑
3. 集成到现有代码
4. 确保测试通过

### 5.3 代码格式化

完成实现后:

```bash
clang-format -i <source-files>
```

## Phase 6: 多角度代码审查

完成代码实现后，并行派发多个 subagent 从不同角度审查代码。

### 6.1 审查维度

根据你所实现的内容，选择性的派发以下 subagent 进行代码审查（如果当前功能过于简单且显而易见的容易验证，可以不派发）：

| 审查角度 | Subagent | 关注点 |
|---------|----------|--------|
| 性能审查 | general | 算法复杂度、内存使用、I/O 效率、缓存友好性等 |
| 功能完备性 | general | 边界条件、错误处理、功能覆盖、需求对齐 |
| 代码安全性 | general | 输入验证、注入风险、敏感数据处理、权限控制 |
| 可维护性 | general | 模块耦合度、扩展性 |

### 6.2 派发方式

使用 Task 工具并行派发多个 general subagent

### 6.3 审查报告整合

收集所有 subagent 的审查报告后：

1. **汇总问题** - 按严重程度分类
2. **修复关键问题** - 必须修复 Critical 级别问题
3. **评估权衡** - 与架构师讨论是否修复 Warning 级别问题
4. 如果有相关问题需要修复，则回到 Phase 5 进行实现
5. 修复问题后，重新运行相关 subagent 验证修复效果。

## Phase 7: 提交代码

```bash
git add <source-files>
git commit -m "feat: <feature-description>"
```

Commit message 规范:
- 使用 `feat:` 前缀
- 简洁描述功能（英文）

## Phase 8: 合并 Worktree（Rebase）

1. 切换回主仓库
2. 更新主分支
3. 整理提交历史

如有冲突：手动解决冲突

注意：
🚫 强制约束（必须遵守）
❌ 禁止使用 git merge（产生 merge commit）
✅ 必须保持线性历史
✅ 保证 commit history 干净、可读

## Phase 9: 总结汇报

用中文向架构师汇报:

1. **实现概述** - 实现了什么功能
2. **设计决策** - 关键的设计选择和理由
3. **文件变更** - 修改或新增的文件
4. **测试覆盖** - 测试覆盖的功能点
5. **后续建议** - 可选的改进方向
