---
description: |
  将 LaTeX 论文从一个模板转换为另一个模板。适用于期刊/会议投稿时的格式迁移，
  如 IEEE → Elsevier、NeurIPS → ICML、或任意自定义模板之间的转换。
  核心机制：通过 context_anchor 文件维持全局一致性，按章节分段处理以突破上下文窗口限制。
---

# LaTeX 论文模板格式转换 Workflow

## 适用场景
- 将一篇已完成的 LaTeX 论文从模板 A 迁移至模板 B
- 论文内容不变，仅调整格式、命令、环境以适配新模板
- 论文篇幅较长，无法一次性放入上下文窗口

## 前置要求
- 用户提供：源论文 .tex 文件路径、目标模板文件（或模板名称）
- 如果目标模板是标准模板（IEEE, Elsevier, Springer, ACM, NeurIPS, ICML 等），可从模板名推断格式要求

---

## Phase 0: 全局上下文锚定（Context Anchoring）

**目标**：提取源论文的完整结构信息，生成一份 `context_anchor.md` 文件，作为后续所有分段处理的全程参考。

### 步骤

1. **通读源论文**：使用 `view_file` 分段读取源 .tex 文件，**不做任何修改**。

2. **提取并记录以下信息到 `context_anchor.md`**：

   ```markdown
   # Context Anchor: [论文标题]

   ## 源模板信息
   - documentclass: [e.g., \documentclass[conference]{IEEEtran}]
   - 编译器: [pdflatex / xelatex / lualatex]
   - 关键包列表: [逐行列出 \usepackage]
   - 自定义命令/宏: [逐行列出 \newcommand, \def 等]
   - 参考文献方式: [bibtex / biblatex, .bst 文件名]

   ## 目标模板信息
   - documentclass: [目标模板的 documentclass]
   - 编译器: [目标模板要求的编译器]
   - 关键包列表: [目标模板必须的包]
   - 元数据命令映射: [源 → 目标的命令映射表]
   - 参考文献方式: [目标模板的引用系统]

   ## 文档结构骨架
   - 元数据区: L[start]-L[end] (title, author, abstract, keywords)
   - Section 1 [标题]: L[start]-L[end]
   - Section 2 [标题]: L[start]-L[end]
   - ...
   - References: L[start]-L[end]
   - Appendix: L[start]-L[end] (如有)

   ## 全局元素清单
   ### 图表
   | ID | 类型 | 标签 | 位置(行号) | 环境 | 备注 |
   |----|------|------|-----------|------|------|
   | 1  | Figure | fig:overview | L45-L52 | figure | 单栏 |
   | 2  | Table  | tab:results  | L120-L145| table* | 跨双栏 |

   ### 数学公式（带标签的）
   | 标签 | 位置(行号) | 环境 |
   |------|-----------|------|
   | eq:loss | L78 | equation |
   | eq:grad | L85-L90 | align |

   ### 交叉引用统计
   - \ref{} 调用次数: N
   - \cite{} 调用次数: M
   - 引用 key 列表: [key1, key2, ...]

   ## 命令映射表（核心）
   | 功能 | 源模板命令 | 目标模板命令 | 备注 |
   |------|----------|------------|------|
   | 作者 | \author{} | \Author{} | 格式不同 |
   | 单位 | \affiliation | \institute | 语法不同 |
   | 摘要 | \begin{abstract} | \abstract{} | 环境→命令 |
   | ... | ... | ... | ... |
   ```

3. **将 `context_anchor.md` 保存到源论文同级目录或临时目录**。

> **关键原则**：`context_anchor.md` 是整个转换过程的"记忆外挂"。后续每个 Phase 开始前都必须先 `view_file` 读取此文件的相关部分。

---

## Phase 1: 创建目标文件骨架

**目标**：基于目标模板创建新 .tex 文件的 preamble 和文档结构。

### 步骤

1. **参考 `context_anchor.md` 中的命令映射表**。

2. **创建新文件**，写入：
   - 目标模板的 `\documentclass`
   - 必要的 `\usepackage` 声明（合并源论文需要的包 + 目标模板必须的包，去除冲突包）
   - 迁移自定义命令（`\newcommand` 等），调整为与目标模板兼容
   - 空的文档骨架：
     ```latex
     \begin{document}
     % === METADATA (Phase 2) ===
     % === SECTION: Introduction (Phase 2) ===
     % === SECTION: ... (Phase 2) ===
     % === REFERENCES (Phase 2) ===
     \end{document}
     ```

3. **记录包冲突处理**：如果源论文用了与目标模板冲突的包，在 `context_anchor.md` 中追加冲突处理记录。

---

## Phase 2: 分段内容迁移

**目标**：按章节逐段将内容从源论文迁移到目标文件。

### 执行规则

- **每次只处理一个 section**，避免上下文溢出
- **每段处理前**：先 `view_file` 读取 `context_anchor.md` 的命令映射表部分
- **处理顺序**：元数据 → 正文各 section（按顺序）→ 参考文献 → 附录

### 每个 Section 的处理流程

```
1. view_file 读取 context_anchor.md 中的命令映射表
2. view_file 读取源论文中该 section 的行范围
3. 执行格式转换：
   a. 替换模板特定命令（按映射表）
   b. 调整环境名称（如 figure* ↔ figure）
   c. 保持所有 \label{} 不变（交叉引用锚点）
   d. 保持所有 \cite{} 不变（引用 key 不变）
   e. 保持正文内容完全不变（不改写、不润色、不删减）
   f. 调整缩进和空行以符合目标模板风格
4. 将转换后的内容写入目标文件对应位置
5. 在 task.md 中标记该 section 为已完成
```

### 特殊处理项

#### 元数据区
- 作者、单位、邮箱的格式通常差异最大，需逐命令对照映射
- 注意 corresponding author、equal contribution 等标记的语法差异

#### 图表
- 检查 `figure` vs `figure*`（单栏 vs 跨栏）是否需要调整
- 检查 `\includegraphics` 的宽度参数是否需要从 `\columnwidth` 改为 `\textwidth` 或反之
- 子图包：`subfig` vs `subcaption` vs `subfigure`，按目标模板选择

#### 数学公式
- 通常不需要修改，但注意：
  - 某些模板有自定义的 theorem 环境
  - `amsmath` vs 模板自带的数学环境

#### 参考文献
- `\bibliographystyle{}` → 替换为目标模板的 .bst
- 如需从 bibtex 切换到 biblatex（或反之），需重构引用导入方式
- 保持 .bib 文件路径正确

#### 算法
- `algorithm2e` vs `algorithmic` vs `algorithm` 环境差异可能很大
- 如遇到包冲突，优先使用目标模板推荐的算法包

---

## Phase 3: 全局验证

**目标**：确保转换后的论文完整、一致、可编译。

### 逐项检查

1. **结构完整性**
   - 对照 `context_anchor.md` 的文档结构骨架，确认所有 section 已迁移
   - 未遗漏：acknowledgment, appendix, supplementary 等

2. **交叉引用完整性**
   - 所有 `\label{}` 在目标文件中存在
   - 所有 `\ref{}` / `\eqref{}` 引用的 label 在目标文件中存在
   - 统计数量与 `context_anchor.md` 中记录的一致

3. **引用完整性**
   - 所有 `\cite{}` 中的 key 在 .bib 文件中存在
   - `\bibliographystyle` 和 `\bibliography` 命令正确

4. **格式一致性**
   - 无残留的源模板专用命令
   - grep 搜索源模板特征命令，确认全部替换

5. **编译测试**（如环境允许）
   - 运行 pdflatex/xelatex 编译，检查错误和警告
   - 重点关注：undefined control sequence, missing package, label multiply defined

### 验证命令示例
```bash
# 检查是否有残留的源模板命令（以 IEEE 为例）
grep -n "\\IEEEauthorblockN\|\\IEEEauthorblockA" target_paper.tex

# 检查所有 label 都有对应的 ref
grep -oP '\\label\{[^}]+\}' target_paper.tex | sort > labels.txt
grep -oP '\\ref\{[^}]+\}|\\eqref\{[^}]+\}' target_paper.tex | sort > refs.txt

# 编译测试
pdflatex -interaction=nonstopmode target_paper.tex
bibtex target_paper
pdflatex -interaction=nonstopmode target_paper.tex
pdflatex -interaction=nonstopmode target_paper.tex
```

---

## Phase 4: 清理与交付

1. 删除 `context_anchor.md`（如果是临时文件）或保留作为转换记录
2. 通知用户转换完成，提供：
   - 目标文件路径
   - 已知的需要人工检查的项（如特殊格式无法自动映射）
   - 编译测试结果（如已执行）

---

## 防护规则（贯穿全流程）

1. **内容零修改原则**：绝对不修改论文的文字内容、数据、公式。仅修改格式相关命令。
2. **存疑则问**：遇到无法确定的命令映射，记录到 `context_anchor.md` 并询问用户，不要猜测。
3. **逐段提交**：每完成一个 section 就写入目标文件，不要在内存中累积多个 section。
4. **锚点文件常读**：每个新 section 处理前必须重新读取 `context_anchor.md` 的映射表，防止上下文遗忘。

---

## 常见模板转换速查

### IEEE → Elsevier
| 元素 | IEEE | Elsevier (elsarticle) |
|------|------|----------------------|
| 文档类 | `\documentclass[conference]{IEEEtran}` | `\documentclass[preprint,review,12pt]{elsarticle}` |
| 作者 | `\author{\IEEEauthorblockN{Name}...}` | `\author[label]{Name}` |
| 单位 | `\IEEEauthorblockA{...}` | `\affiliation[label]{...}` / `\address{}` |
| 摘要 | `\begin{abstract}...\end{abstract}` | `\begin{abstract}...\end{abstract}` |
| 关键词 | `\begin{IEEEkeywords}...\end{IEEEkeywords}` | `\begin{keyword}...\end{keyword}` |
| 参考文献 | `\bibliographystyle{IEEEtran}` | `\bibliographystyle{elsarticle-num}` |

### NeurIPS → ICML
| 元素 | NeurIPS | ICML |
|------|---------|------|
| 文档类 | `\documentclass{article}` + `\usepackage{neurips_20xx}` | `\documentclass{article}` + `\usepackage{icml20xx}` |
| 作者 | `\author{Name \\ Affiliation}` | `\icmlauthor{Name}{aff}` + `\icmlaffiliation{aff}{...}` |
| 摘要 | `\begin{abstract}...\end{abstract}` | `\begin{abstract}...\end{abstract}` |
| 参考文献 | `\bibliographystyle{plainnat}` | `\bibliographystyle{icml20xx}` |

### 任意期刊 → Springer (svjour3)
| 元素 | 通用 | Springer |
|------|------|---------|
| 文档类 | varies | `\documentclass[smallextended]{svjour3}` |
| 作者 | varies | `\author{Name1 \and Name2}` |
| 单位 | varies | `\institute{Aff1 \at email \and Aff2 \at email}` |
| 关键词 | varies | `\keywords{kw1 \cdot kw2}` |
