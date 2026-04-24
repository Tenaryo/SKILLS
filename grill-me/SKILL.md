---
name: grill-me
description: This skill should be used when the user explicitly says "grill me", requesting the assistant to proactively ask questions about any ambiguity, decision point, or unclear requirement during task execution.
---

# Grill Me

遇到任何不确定的事，直接问用户。不要猜，不要假设，不要自作主张。

## 核心原则

- **宁可多问，不要少问** — 任何拿不准的细节都值得确认
- **不要替用户做决定** — 涉及选择和取舍时，把选项呈现给用户
- **尽早问** — 遇到问题立刻问，不要先做再问
- **任何时间问** — 不一定要一开始一股脑全问完，而是中途任何时间遇到问题都要立刻停止手中工作直接询问

## 什么时候必须问

- 需求描述模糊或有歧义
- 存在多种可行的实现方案
- 涉及命名、结构、风格等主观选择
- 不确定用户的意图或偏好
- 遇到报错或异常，原因不唯一
- 任何自己"猜"了的地方

## 怎么问

使用 question 工具提问，遵循以下规范：

1. **一次问一个问题** — 不要把多个问题塞进一个 question 调用
2. **给够上下文** — 在正文里说清楚现状和背景，question 工具里只放简短的问题本身
3. **给出选项** — 能列举选项时就列出来，包括推荐的选项，但不要替用户选
4. **等回答再继续** — 问完一个问题，拿到回复后再决定是否还有下一个问题
