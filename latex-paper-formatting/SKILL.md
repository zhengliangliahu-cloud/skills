---
name: latex-paper-formatting
description: |
  LaTeX 学术论文编排与格式修正。当涉及论文排版、表格溢出修复、图表布局、
  交叉引用管理、bibtex/biblatex 引用格式、期刊模板适配（如 IEEE/Elsevier/Springer）、
  或多栏布局调整时触发。
  **模板格式转换**：当需要将论文从一个 LaTeX 模板迁移到另一个模板时，
  必须使用 workflows/latex-template-convert.md 中定义的分段转换流程。
---
# LaTeX 论文编排

## Overview

本技能专注于学术论文 LaTeX 排版的常见问题和最佳实践。
覆盖从模板选择到最终提交的全流程排版优化。

## Workflows

### 模板格式转换（长文档安全处理）
当任务涉及**将论文从一个 LaTeX 模板转换为另一个模板**时，必须执行：
→ `workflows/latex-template-convert.md`

此 workflow 通过 context_anchor 机制解决长文档上下文窗口限制问题，
确保分段处理时保持全局一致性。

## Core Workflow（排版修正）

1. **模板确认**：确认目标期刊/会议的 LaTeX 模板和提交要求。
2. **结构检查**：验证文档结构、章节层级、标签命名。
3. **表格修正**：修复溢出、优化可读性、调整列宽。
4. **图表优化**：统一图表样式、标注字号、输出格式。
5. **引用管理**：检查 .bib 完整性、引用格式一致性。
6. **最终校验**：消除编译警告、检查页面溢出。

## 表格排版（高频问题）

### 表格溢出修复策略

按优先级依次尝试：

1. **使用 `\resizebox`**（简单暴力）
```latex
\begin{table}[t]
\caption{Results}
\resizebox{\columnwidth}{!}{%
\begin{tabular}{lccc}
...
\end{tabular}}
\end{table}
```

2. **使用 `tabularx` 自适应列宽**
```latex
\usepackage{tabularx}
\begin{tabularx}{\columnwidth}{lXXX}
...
\end{tabularx}
```

3. **使用 `adjustbox` 精确控制**
```latex
\usepackage{adjustbox}
\begin{adjustbox}{max width=\columnwidth}
\begin{tabular}{lccc}
...
\end{tabular}
\end{adjustbox}
```

4. **使用 `\small` 或 `\footnotesize` 缩小字号**
```latex
\begin{table}[t]
{\small
\begin{tabular}{lccc}
...
\end{tabular}}
\end{table}
```

5. **跨双栏表格**（最后手段）
```latex
\begin{table*}[t]  % 注意是 table*
...
\end{table*}
```

### 表格美化
- 使用 `booktabs` 包（`\toprule`, `\midrule`, `\bottomrule`）替代 `\hline`。
- 避免竖线，使用适当的列间距。
- 加粗最优结果：`\textbf{}`。
- 次优结果下划线：`\underline{}`。

## 图表排版

### 推荐配置
```latex
\usepackage{graphicx}
\usepackage[caption=false]{subfig}  % 或 subcaption
\usepackage{float}

% 单栏图
\begin{figure}[t]
\centering
\includegraphics[width=\columnwidth]{figures/xxx.pdf}
\caption{Description.}
\label{fig:xxx}
\end{figure}

% 子图排列
\begin{figure}[t]
\centering
\subfloat[Sub A]{\includegraphics[width=0.48\columnwidth]{fig_a.pdf}\label{fig:a}}
\hfill
\subfloat[Sub B]{\includegraphics[width=0.48\columnwidth]{fig_b.pdf}\label{fig:b}}
\caption{Overall caption.}
\label{fig:overall}
\end{figure}
```

### 图表格式
- 论文图表优先使用 **PDF** 或 **SVG** 矢量格式。
- 位图分辨率不低于 **300 DPI**。
- 图表内文字字号应与正文接近（≥8pt）。

## 引用管理

### BibTeX 规范
- 每条引用必须有：author, title, year, booktitle/journal。
- 引用 key 命名：`<首个作者姓><年份><关键词>`，如 `wang2024riemannian`。
- 统一使用 `\cite{}`，避免混用 `\citep{}` 和 `\citet{}`（除非模板要求）。

### 常见引用问题
| 问题 | 解决 |
|------|------|
| 引用显示 `[?]` | 检查 .bib 中 key 是否一致，运行 bibtex 两次 |
| 作者名显示异常 | 使用 `{Last}, First` 格式 |
| 期刊名大小写丢失 | 用 `{IEEE}` 花括号保护缩写 |

## 通用排版检查清单

- [ ] 所有图表有 `\label{}` 且在正文中被 `\ref{}` 引用
- [ ] 无 overfull/underfull hbox 警告（或已处理至可接受范围）
- [ ] 括号匹配：所有 `\begin{}` 有对应 `\end{}`
- [ ] 数学符号统一：同一变量全文使用一致记号
- [ ] 页码在限制范围内
- [ ] 作者信息和致谢符合投稿要求
- [ ] 高亮/TODO 标记全部清理

## Execution Rules

1. 修改 LaTeX 文件前，先确认模板版本和编译方式（pdflatex/xelatex/lualatex）。
2. 每次修改后检查编译结果，确保无引入新错误。
3. 表格修改优先使用非侵入性方案（如 `resizebox`），避免重构表格结构。
4. 保持源码缩进和注释风格一致。
