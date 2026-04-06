# 实验结果分析参考

## 结果汇总模板

```python
import pandas as pd
import numpy as np

def summarize_results(csv_path, group_by='method', metrics=None):
    """汇总实验结果，按方法分组计算均值±标准差"""
    df = pd.read_csv(csv_path)
    if metrics is None:
        metrics = [c for c in df.columns if c != group_by and df[c].dtype in ['float64', 'int64']]
    
    summary = df.groupby(group_by)[metrics].agg(['mean', 'std'])
    
    # 格式化为 mean±std
    formatted = pd.DataFrame(index=summary.index)
    for metric in metrics:
        formatted[metric] = summary[(metric, 'mean')].map('{:.2f}'.format) + '±' + \
                           summary[(metric, 'std')].map('{:.2f}'.format)
    return formatted

def to_latex_table(df, caption='', label=''):
    """将 DataFrame 转换为 LaTeX 表格"""
    latex = df.to_latex(escape=False, column_format='l' + 'c' * len(df.columns))
    if caption:
        latex = latex.replace('\\begin{tabular}', 
                             f'\\caption{{{caption}}}\n\\label{{{label}}}\n\\begin{{tabular}}')
    return latex
```

## 统计检验

```python
from scipy import stats

def paired_comparison(scores_a, scores_b, test='ttest'):
    """成对比较两种方法，返回 p-value 和显著性标记"""
    if test == 'ttest':
        stat, p = stats.ttest_rel(scores_a, scores_b)
    elif test == 'wilcoxon':
        stat, p = stats.wilcoxon(scores_a, scores_b)
    
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'n.s.'
    return {'statistic': stat, 'p_value': p, 'significance': sig}
```

## 可视化模板

```python
import matplotlib.pyplot as plt
import seaborn as sns

# 论文级图表设置
plt.rcParams.update({
    'font.size': 14,
    'font.family': 'serif',
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'legend.fontsize': 12,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.figsize': (8, 6),
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
})

def plot_comparison_bar(df, metric, save_path=None):
    """绘制方法对比柱状图"""
    fig, ax = plt.subplots()
    methods = df.index
    means = df[(metric, 'mean')]
    stds = df[(metric, 'std')]
    
    bars = ax.bar(methods, means, yerr=stds, capsize=5, 
                  color=sns.color_palette('Set2', len(methods)))
    ax.set_ylabel(metric)
    ax.set_title(f'{metric} Comparison')
    
    if save_path:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()
```

## Markdown 表格生成

```python
def to_markdown_table(df, bold_best=True):
    """生成 Markdown 格式表格，可选加粗最优值"""
    header = '| Method | ' + ' | '.join(df.columns) + ' |'
    separator = '|--------|' + '|'.join(['--------'] * len(df.columns)) + '|'
    rows = []
    for idx, row in df.iterrows():
        values = [str(v) for v in row]
        rows.append(f'| {idx} | ' + ' | '.join(values) + ' |')
    return '\n'.join([header, separator] + rows)
```
