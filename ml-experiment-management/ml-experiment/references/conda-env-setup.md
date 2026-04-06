# Conda 环境管理参考

## 创建环境

```bash
# 从 YAML 文件创建
conda env create -f environment.yml

# 手动创建
conda create -n <env-name> python=3.10 -y
conda activate <env-name>

# PyTorch + CUDA (根据实际 CUDA 版本调整)
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

## 导出环境

```bash
# 完整导出（含 build 信息，跨平台可能不兼容）
conda env export > environment.yml

# 仅导出手动安装的包（推荐跨平台）
conda env export --from-history > environment.yml

# 导出 pip 依赖
pip freeze > requirements.txt
```

## 环境迁移

```bash
# 从 YAML 恢复
conda env create -f environment.yml

# 更新已有环境
conda env update -f environment.yml --prune

# 克隆环境
conda create --name <new-env> --clone <old-env>
```

## 常用检查命令

```bash
# 列出所有环境
conda env list

# 当前环境的包
conda list

# 检查 CUDA
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}, Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}')"

# 检查 GPU 资源
nvidia-smi
```

## 最佳实践

1. **不要在 base 环境安装项目依赖**。
2. **PyTorch 始终通过 conda 安装**以确保 CUDA 库匹配。
3. **先 conda install 再 pip install**，避免依赖冲突。
4. **定期导出 environment.yml**，确保环境可复现。
5. **清理缓存**：`conda clean --all` 释放磁盘空间。
