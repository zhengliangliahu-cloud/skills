---
name: codex-worker
description: Delegate bounded coding, debugging, testing, review, repository investigation, refactor, and writing subtasks from Antigravity or a main agent to the local Codex CLI. Use when the main agent needs Codex to act as a worker/subagent for scoped code edits, bug fixes, tests, docs, or focused analysis while the main agent retains planning, diff review, validation, and final acceptance.
---

# Codex Worker

## 目的

使用这个技能，把边界清晰的子任务委派给本机 Codex CLI，让 Codex 作为 Antigravity 或主 agent 的 worker/subagent 分担 coding、改 bug、测试、代码审查、仓库调研、局部重构和技术写作任务。

Codex worker 可以在明确范围内直接修改文件，但主 agent 必须负责计划、任务拆分、写入范围控制、diff 审查、测试复核和最终验收。不要把 Codex worker 当作最终裁决者。

## 本机 CLI

优先使用 PATH 中的 `codex.exe`。当前已探测版本：

- `codex.exe`
- `codex-cli 0.119.0-alpha.28`

每个新会话第一次使用前，先确认 CLI 可用：

```powershell
Get-Command codex -ErrorAction SilentlyContinue
codex --version
codex exec --help
```

默认直接改码命令：

```powershell
codex exec -C "<repo>" --sandbox workspace-write --full-auto --ephemeral "<bounded prompt>"
```

只读调研命令：

```powershell
codex exec -C "<repo>" --sandbox read-only --ephemeral "<investigation prompt>"
```

审查当前未提交改动：

```powershell
codex review --uncommitted "<review instruction>"
```

常用参数：

- `-C "<repo>"`：指定 Codex worker 的工作目录。
- `--add-dir "<path>"`：需要读取或写入主仓库外的额外目录时使用；只添加任务必要目录。
- `--output-last-message "<file>"`：需要保存 Codex 最终回复，供主 agent 后续解析或归档时使用。
- `--json`：需要机器解析事件流或日志时使用；普通委派默认不需要。
- `--ephemeral`：默认使用，减少子任务会话残留，避免后续任务误用旧上下文。

不要默认使用 `--dangerously-bypass-approvals-and-sandbox`。只有在外部环境已经可靠隔离、用户明确要求、且任务需要绕过 sandbox 时才考虑使用。

## 适合交给 Codex 的任务

只把范围窄、目标清楚、可本地验证、可通过 diff 审查的工作交给 Codex：

- 局部 bug 修复：已有失败现象、报错、测试或复现路径。
- 聚焦功能实现：限定在明确模块、文件或目录内的小功能。
- 测试补齐：为已有行为添加或更新单元测试、回归测试、快照测试。
- 代码审查：检查当前 diff、某个 commit 或指定改动的正确性风险和缺失测试。
- 仓库调研：定位数据流、调用链、配置来源、失败原因或最小修复点。
- 局部重构：不改变公共行为，在有限路径内清理重复或调整结构。
- 技术写作：改写 README、开发文档、注释、变更说明、PR 描述或实验记录。

Codex 特别适合做主 agent 的并行分担：把一个可独立验证的小任务交出去，主 agent 继续处理不重叠的主线工作。

## 不适合交给 Codex 的任务

以下任务应保留给主 agent，或先由主 agent 拆小后再局部委派：

- 产品决策、UX 策略、架构归属、需求含糊或成功标准不清的任务。
- 大范围迁移、跨系统设计、认证/权限/安全关键改动、部署改动、数据库或数据丢失风险改动。
- 无边界的全仓重构、依赖大升级、格式化全仓、生成大量代码。
- 多个 agent 需要同时编辑同一批文件的任务。
- 主 agent 无法在事后运行验证、理解 diff 或判断正确性的任务。
- 需要长期连续上下文、复杂人类偏好判断或高风险取舍的任务。

## Codex 的短板和风险

Codex worker 是执行型 coding agent，不是最终验收者：

- 可能过度修改、顺手重构、误解任务边界或忽略本地约定。
- 可能漏跑测试，或把无法运行的测试描述成已验证风险较低。
- 可能受 sandbox、approval、网络访问或依赖安装限制影响，导致任务无法完整执行。
- 如果提示词没有写清 allowed edits 和 do not edit，可能触碰范围外文件。
- 如果多个 worker 的写入范围重叠，可能与 Antigravity、主 agent、用户或其他子 agent 的改动冲突。
- 对安全、数据、配置、API 行为和部署相关改动，不能用 Codex 的结论替代主 agent 审查。

## 必须遵守的工作流

1. 委派前检查工作区状态：

```powershell
git status --short
```

2. 定义不重叠的写入范围。明确列出 Codex 可以编辑的文件、目录或模块，也明确列出禁止触碰的范围。

3. 使用下方提示词模板发送有边界的任务。已知测试、构建或 lint 命令时，必须写入提示词。

4. Codex 返回后，先审查改动，再继续其他操作：

```powershell
git status --short
git diff --stat
git diff
```

5. 主 agent 自己运行相关测试、构建或静态检查。即使 Codex 声称测试通过，只要可行也要复核。

6. 只有理解 diff 后，才接受、继续微调或只回退 Codex 的改动。不要回退无关的用户或其他 agent 改动。

## 委派提示词模板

委派时使用这个结构：

```text
You are acting as a worker subagent for the main agent.

Goal:
- <one concrete outcome>

Allowed edits:
- <exact files/directories/modules Codex may edit>

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
- If blocked by sandbox, dependency, or missing context, stop and report the blocker.

Validation:
- Run: <test/build/lint command, or say "do not run tests; report what should be run">

Final response:
- Summarize changed files.
- Explain the fix or implementation briefly.
- Report validation commands and results.
- Mention any remaining risks or follow-up needed.
```

## 命令示例

让 Codex 直接修一个局部 bug：

```powershell
codex exec -C "D:\path\to\repo" --sandbox workspace-write --full-auto --ephemeral "You are acting as a worker subagent for the main agent. Goal: fix the failing parser edge case described in tests. Allowed edits: src/parser/** and tests/parser/** only. Do not edit package metadata, lockfiles, migrations, or unrelated modules. Keep the change minimal. Validation: run npm test -- parser. Final response: list changed files, validation result, and any risks."
```

只做只读调研：

```powershell
codex exec -C "D:\path\to\repo" --sandbox read-only --ephemeral "Investigate why the login flow can return a blank screen. Do not edit files. Return likely root causes, exact file references, and the smallest recommended fix."
```

审查当前 diff：

```powershell
codex review --uncommitted "Review the current diff for bugs or missing tests. Do not edit files. Focus on correctness regressions, edge cases, and validation gaps. Return findings with file paths and line references."
```

把最终回复保存到文件：

```powershell
codex exec -C "D:\path\to\repo" --sandbox workspace-write --full-auto --ephemeral --output-last-message "D:\path\to\repo\.codex-worker-last.md" "<bounded prompt>"
```

## 主 agent 验收规则

- 把 Codex 当作快速 worker，而不是最终审查者。
- 尽量保持同一文件同一时间只有一个写入者。
- 优先拆成短任务交给 Codex，不要一次交付大而宽的多阶段任务。
- 如果 Codex 改动过多，停止继续扩展任务，改为收窄范围重新委派。
- 如果 Codex 没有运行验证，主 agent 必须在最终回复中说明未验证项。
- 只有主 agent 复核后，才在最终回复中描述 Codex 修改了什么、是否通过验证、还有什么风险。
