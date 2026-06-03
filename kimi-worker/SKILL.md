---
name: kimi-worker
description: Delegate bounded coding, debugging, test, local refactor, code review, and repository-investigation subtasks from Codex or Antigravity to the local Kimi Code CLI. Use when the main agent needs Kimi to act as a worker or subagent for direct code edits or focused analysis while the main agent remains responsible for scoping, diff review, tests, and final acceptance.
---

# Kimi Worker

## 目的

用这个技能把边界清晰的 coding 子任务委派给本机 Kimi Code CLI。Kimi 默认可以在明确范围内直接修改文件，但主 agent 必须负责计划、协调、diff 审查、测试验证和最终验收。

当 Codex 或 Antigravity 需要一个 worker agent 分担实现、修 bug、仓库调研、测试补齐或局部重构时，优先使用这个技能。

## 本机 CLI

优先使用 `kimi`；只有 `kimi` 不可用时才回退到 `kimi-cli`。

本机已探测到：

- `kimi.exe`: `C:\Users\pairl\.local\bin\kimi.exe`
- `kimi-cli.exe`: `C:\Users\pairl\.local\bin\kimi-cli.exe`
- 已探测版本：`1.39.0`

每个新会话第一次使用前先确认 CLI 可用：

```powershell
Get-Command kimi,kimi-cli -ErrorAction SilentlyContinue
kimi --version
```

默认直接改码命令：

```powershell
kimi --work-dir "<repo>" --quiet --max-steps-per-turn 20 --prompt "<bounded task prompt>"
```

如果 Kimi 需要读取或编辑额外目录，追加 `--add-dir "<path>"`。不要随意使用 `--continue`，除非明确要恢复同一个仓库、同一个任务的上一段 Kimi 会话。

## 适合交给 Kimi 的任务

只把范围窄、可本地验证、可通过 diff 审查的工作交给 Kimi：

- 已知失败行为后的局部 bug 修复。
- 在指定模块或文件集合中实现清晰的小功能。
- 为已有行为添加或更新聚焦测试。
- 在有限路径列表内做重复性、机械性改动。
- 调研代码流、定位可能原因，或做第二视角代码审查。
- 在不改变公共行为的前提下重构一个小区域。

## 不适合交给 Kimi 的任务

当任务高度依赖意图判断、风险较高或协调成本过高时，保留给主 agent：

- 产品决策、UX 策略、架构归属或需求含糊的任务。
- 跨系统设计、大范围迁移、数据库或数据丢失风险、认证/安全关键改动、部署改动。
- 无边界的全仓重构或依赖升级。
- 多个 agent 需要同时编辑同一批文件的任务。
- 主 agent 无法在事后运行验证或判断正确性的改动。

## Kimi 的短板和风险

Kimi 适合作为快速 coding worker，不是最终裁决者。

- `--quiet` 会进入 print mode，并隐式批准动作；调用前必须收窄范围。
- Kimi 可能过度修改、忽略本地约定、误读过期上下文，或漏跑测试。
- 如果提示词不够窄，Kimi 可能修改预期范围外的文件。
- 如果写入范围重叠，Kimi 可能与 Codex、Antigravity 或用户的改动冲突。
- 对安全、数据、配置、API 行为相关改动，不能用 Kimi 的结论替代主 agent 审查。

## 必须遵守的工作流

1. 委派前先检查工作区状态：

```powershell
git status --short
```

2. 定义不重叠的写入范围。明确列出 Kimi 可以编辑的文件、目录或模块，也明确列出禁止触碰的范围。

3. 使用下面的模板给 Kimi 发送有边界的任务提示词。已知测试命令时必须写入提示词。

4. Kimi 返回后，先审查改动，再继续其他操作：

```powershell
git status --short
git diff --stat
git diff
```

5. 主 agent 自己运行相关测试、构建或静态检查。即使 Kimi 声称测试通过，只要可行也要复核。

6. 只有理解 diff 后，才接受、继续微调或只回退 Kimi 的改动。不要回退无关的用户或其他 agent 改动。

## 委派提示词模板

委派时使用这个结构：

```text
You are acting as a worker subagent for the main agent.

Goal:
- <one concrete outcome>

Allowed edits:
- <exact files/directories/modules Kimi may edit>

Do not edit:
- <paths, generated files, lockfiles, migrations, unrelated modules, or user-owned changes>

Context:
- <bug symptoms, current behavior, expected behavior, relevant commands, important constraints>

Implementation constraints:
- Follow existing project style and patterns.
- Keep changes minimal and scoped.
- Do not perform unrelated refactors.
- Do not change public APIs unless explicitly requested.
- Do not overwrite unrelated worktree changes.

Validation:
- Run: <test/build/lint command, or say "do not run tests; report what should be run">

Final response:
- Summarize changed files.
- Explain the fix or implementation briefly.
- Report validation commands and results.
- Mention any remaining risks or follow-up needed.
```

## 命令示例

让 Kimi 直接修一个局部 bug：

```powershell
kimi --work-dir "D:\path\to\repo" --quiet --max-steps-per-turn 20 --prompt "You are acting as a worker subagent for the main agent. Goal: fix the failing parser edge case described in tests. Allowed edits: src/parser/** and tests/parser/** only. Do not edit package metadata or unrelated modules. Keep the change minimal. Run: npm test -- parser. Final response: list changed files, validation result, and any risks."
```

只做只读调研：

```powershell
kimi --work-dir "D:\path\to\repo" --quiet --plan --prompt "Investigate why the login flow can return a blank screen. Do not edit files. Return likely root causes, exact file references, and the smallest recommended fix."
```

做第二视角代码审查：

```powershell
kimi --work-dir "D:\path\to\repo" --quiet --prompt "Review the current diff for bugs or missing tests. Do not edit files. Focus on correctness regressions, edge cases, and validation gaps. Return findings with file paths and line references."
```

## 主 agent 验收规则

- 把 Kimi 当作快速 coding worker，而不是最终审查者。
- 尽量保持一个文件同一时间只有一个写入者。
- 优先拆成短任务交给 Kimi，不要一次交付大而宽的多阶段任务。
- 如果 Kimi 改动过多，停止继续扩展任务，改为收窄范围重新委派。
- 只有主 agent 验证后，才在最终回复中描述 Kimi 修改了什么。
