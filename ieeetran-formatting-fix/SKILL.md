---
name: ieeetran-formatting-fix
description: Fixes common IEEEtran LaTeX formatting issues like large blank spaces, scattered floats, and biography displacements.
tags: [latex, ieee, format, float, biography]
---

# IEEEtran Formatting Fixer

This skill serves as the ultimate troubleshooting and repair guide for common LaTeX layout issues in **IEEE Transactions (`IEEEtran.cls`)** manuscripts. IEEEtran enforces rigorous float positioning, which often clashes with manuscript structures (e.g., placing huge tables in Appendices) and results in unpredictable whitespace blocks or text mixing up near the author biographies.

When a user complains about:
1. **"大面积空白(Large Blank Spaces)"** before the biography or on the second-to-last page.
2. **"浮动体/表格进入了传记区 (Floats overlapping Biography section)"**.
3. **"传记占据整页被推远 (Biography isolated onto a new page unnecessarily)"**.

Follow this systematic repair procedure manually or execute it over the `.tex` files.

## Protocol for Fixing IEEEtran Trailing Whitespaces & Biographies

### 1. Remove `\clearpage` Before Biographies
A hard `\clearpage` before the `\begin{IEEEbiography}` block is the #1 cause of massive blank spaces. It flushes pending floats to an entirely new page and forces the Biographies to jump away from the main text.
- **Action**: Find `\clearpage` or `\newpage` just before the Biography section and **DELETE IT**. Let the biographies naturally follow the text flow.

### 2. Isolate Floats with `\FloatBarrier` (The "Dam" Method)
When `\clearpage` is removed, floating tables/figures (like those declared in an Appendix) can drift into or after the Biography section, mangling the layout.
- **Action**: Add `\usepackage{placeins}` to the document preamble.
- **Action**: Insert `\FloatBarrier` immediately before the Biography section. This acts as an invisible dam that logically prevents any pending appendix tables/figures from bypassing the line, while avoiding the catastrophic whitespace of `\clearpage`.

```latex
% --- Appendices ---
\input{appendices}

\FloatBarrier % <--- Force pending appendix tables to print BEFORE biographies

% --- Author Biographies ---
\section*{Biography}
```

### 3. Neutralize IEEEbiography Elasticity (`\vskip` Hack)
`IEEEtran` secretly injects a stretchable glue (`\vfil`) above each `IEEEbiography` block to balance multi-column layouts. On packed pages, this glue stretches improperly, tossing a biography to the next page and destroying density.
- **Action**: Inject `\vskip 0pt plus -1fil` immediately before the `\begin{IEEEbiography}` environment to counteract the internal elasticity.
- **Action**: Optionally, add `\vspace*{-2\baselineskip}` (tweak the multiplier from -1 to -3 as needed) to physically tighten the space between multiple authors.

```latex
% Adjust spacing to forcibly eliminate white gaps between author bios
\vskip 0pt plus -1fil
\vspace*{-2\baselineskip}
\begin{IEEEbiography}[{\includegraphics[width=1in,clip,keepaspectratio]{persons/name.jpg}}]{Author Name}
...
\end{IEEEbiography}
```

### 4. Relax Float Specifiers (Avoid Over-Constraining)
Standard single-column floats should use relaxed specifiers like `[htbp]`. Users or other tools often erroneously force `[!t]` or `[!htb]` constraints combined with massive sizes, causing equations or tables to wait endlessly in the LaTeX queue. 
Double-column floats (`figure*`, `table*`) should use `[t]` or `[bp]`.
- **Action**: Let LaTeX decide optimally by switching `[!htb]` and `[!b]` back to `[htbp]` for standard `table`/`figure` environments. Do not inject aggressive custom `\topfraction` rules unless absolutely necessary.

## Quick Execution Summary
Whenever the IEEEtran formatting is structurally broken at the document tail:
1. Open the file containing the appendices and biography (`main.tex` or `manuscript_part2.tex`).
2. Wipe the hard `\clearpage` before biographies.
3. Import `placeins` and drop `\FloatBarrier`.
4. Prefix all Biographies with `\vskip 0pt plus -1fil` and `\vspace*{-2\baselineskip}`.
5. Recompile and verify the page count reduction.
