---
name: docker-deployment
description: |
  Docker 容器化部署与调试。当涉及 Docker/Docker Compose 编排、Dockerfile 编写、
  容器网络配置、日志排查、端口映射、数据卷管理或多服务编排时触发。
---
# Docker 部署管理

## Overview

本技能覆盖项目容器化部署的常见操作和最佳实践。
优先保证部署可复现性、服务稳定性和快速故障排查。

## Core Workflow

1. **项目分析**：确认项目技术栈、依赖和运行要求。
2. **Dockerfile 编写/检查**：确认基础镜像、构建步骤和优化策略。
3. **Compose 编排**：配置多服务协作、网络和数据卷。
4. **环境配置**：管理 `.env` 文件和敏感配置。
5. **构建部署**：构建镜像、启动服务、验证运行状态。
6. **故障排查**：日志分析、网络调试、资源监控。

## Dockerfile 最佳实践

### 多阶段构建
```dockerfile
# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci --production=false
COPY . .
RUN npm run build

# 运行阶段
FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY package*.json ./
RUN npm ci --production
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Python 项目
```dockerfile
FROM python:3.10-slim
WORKDIR /app
# 先复制依赖文件，利用缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "main.py"]
```

### 优化要点
1. **利用构建缓存**：将不常变化的层（如依赖安装）放在前面。
2. **使用 `-slim` 或 `-alpine` 基础镜像**减小镜像体积。
3. **使用 `.dockerignore`** 排除不必要文件（node_modules, .git, __pycache__）。
4. **不在镜像中存储敏感信息**，使用环境变量或 secrets。

## Docker Compose 编排

### 标准结构
```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    env_file:
      - .env
    depends_on:
      - db
    restart: unless-stopped
    
  db:
    image: postgres:15-alpine
    volumes:
      - db_data:/var/lib/postgresql/data
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    restart: unless-stopped

volumes:
  db_data:
```

### 常用命令速查
```bash
# 构建并启动（后台）
docker compose up -d --build

# 查看日志（实时跟踪）
docker compose logs -f <service-name>

# 查看服务状态
docker compose ps

# 进入容器
docker compose exec <service-name> sh

# 停止并删除
docker compose down

# 停止并删除（含数据卷）
docker compose down -v

# 重建单个服务
docker compose up -d --build <service-name>
```

## 故障排查

### 诊断流程
1. `docker compose ps` — 检查服务状态
2. `docker compose logs <service>` — 查看错误日志
3. `docker compose exec <service> sh` — 进入容器检查
4. `docker network ls` / `docker network inspect` — 检查网络
5. `docker stats` — 检查资源使用

### 常见问题

| 问题 | 排查 |
|------|------|
| 端口冲突 | `netstat -tlnp` 检查占用，修改映射端口 |
| 容器启动即退出 | 查看 `docker logs <id>`，检查 CMD/ENTRYPOINT |
| 服务间无法通信 | 确认在同一 network，使用服务名作为 hostname |
| 构建缓存失效 | 检查 COPY 指令顺序，依赖文件是否变化 |
| 磁盘空间不足 | `docker system df` 查看，`docker system prune` 清理 |

## 安全规范

1. **不在 Dockerfile 中硬编码密钥**，使用 `env_file` 或 Docker secrets。
2. **使用非 root 用户运行容器**。
3. **定期更新基础镜像**。
4. **限制容器资源**（memory, CPU）。

## Execution Rules

1. 先检查已有的 Dockerfile 和 compose 文件再修改。
2. 修改 compose 配置后先 `docker compose config` 验证语法。
3. 使用 `--build` 标志确保镜像使用最新代码。
4. 部署前确认 `.env` 文件存在且配置正确。
5. 生产环境始终使用 `restart: unless-stopped`。
