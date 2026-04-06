---
name: code-quality-debug
description: |
  代码质量检查与调试排错。当涉及代码审查、性能分析、内存泄漏排查、
  异常调试、日志分析、断点调试或代码重构建议时触发。
---
# 代码质量与调试

## Overview

本技能覆盖代码质量保障和问题调试的常见方法论。
适用于 Python、JavaScript/TypeScript 和 Shell 脚本。

## Core Workflow

1. **问题定位**：收集错误信息、复现条件、影响范围。
2. **日志分析**：检查相关日志，定位错误源头。
3. **代码审查**：检查代码逻辑、边界条件、异常处理。
4. **调试验证**：通过最小复现用例验证假设。
5. **修复测试**：修复问题并验证修复有效且无副作用。
6. **复盘记录**：记录问题原因和解决方案，防止再发。

## Python 调试

### 常用调试工具
```python
# 快速调试 — 内置 pdb
import pdb; pdb.set_trace()  # Python 3.7+ 可用 breakpoint()

# 打印调试 — 带上下文
import inspect
def debug_print(var, name=None):
    frame = inspect.currentframe().f_back
    if name is None:
        name = [k for k, v in frame.f_locals.items() if v is var][0]
    print(f"[DEBUG] {frame.f_code.co_filename}:{frame.f_lineno} | {name} = {var} (type: {type(var).__name__})")
```

### 性能分析
```python
# 函数级计时
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"[TIMER] {func.__name__}: {elapsed:.4f}s")
        return result
    return wrapper

# 行级分析 — line_profiler
# pip install line_profiler
# @profile 装饰目标函数，然后 kernprof -l -v script.py

# 内存分析 — memory_profiler
# pip install memory_profiler
# @profile 装饰目标函数，然后 python -m memory_profiler script.py
```

### 常见 Python 陷阱
| 陷阱 | 说明 | 避免方式 |
|------|------|---------|
| 可变默认参数 | `def f(x=[]):` 列表在调用间共享 | 使用 `def f(x=None): x = x or []` |
| 闭包变量绑定 | 循环中的 lambda 捕获变量引用 | 使用默认参数 `lambda x=x: x` |
| 浅拷贝 vs 深拷贝 | `list.copy()` 只拷贝第一层 | 使用 `copy.deepcopy()` |
| 整数除法 | Python 3: `/` 是浮点除 | 需要整除用 `//` |
| GIL 限制 | 多线程不能利用多核 CPU | CPU 密集用 `multiprocessing` |

## 代码审查检查清单

### 正确性
- [ ] 边界条件处理（空输入、零值、极大值）
- [ ] 异常处理合理（不吞没异常、合适的异常类型）
- [ ] 资源释放（文件句柄、数据库连接、GPU 内存）
- [ ] 并发安全（共享状态保护）

### 可读性
- [ ] 变量命名清晰且一致
- [ ] 函数职责单一，长度合理（≤50 行）
- [ ] 复杂逻辑有注释说明意图
- [ ] 避免魔法数字，使用常量

### 性能
- [ ] 避免不必要的循环嵌套
- [ ] 使用合适的数据结构（set 代替 list 做查找）
- [ ] 大数据集使用生成器/迭代器
- [ ] 避免重复计算，合理缓存

### 安全
- [ ] 输入验证和清理
- [ ] 无硬编码密钥/密码
- [ ] 日志中不含敏感信息

## 错误排查方法论

### 五步定位法
1. **复现**：确认最小复现步骤。
2. **隔离**：二分法缩小问题范围。
3. **假设**：基于证据提出最可能的原因。
4. **验证**：修改代码或添加日志验证假设。
5. **修复**：实施修复并确认问题解决。

### 日志分级
```python
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler('debug.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# 使用规范
logger.debug("详细调试信息")     # 开发时使用
logger.info("正常运行状态")      # 关键节点记录
logger.warning("潜在问题")       # 需要关注但不影响运行
logger.error("错误但可恢复")     # 需要处理的错误
logger.critical("严重错误")      # 系统无法继续运行
```

## Execution Rules

1. 调试前先完整阅读错误堆栈，从底部的原始异常开始分析。
2. 避免直接猜测修复——先复现，再定位，最后修复。
3. 修复后验证修复是否引入新问题。
4. 性能优化前先 profiling，不做无测量的优化。
5. 记录复杂 bug 的根因分析，便于团队学习。
