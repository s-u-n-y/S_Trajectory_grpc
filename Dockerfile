# 使用官方 Python 3.10 slim 镜像作为基础镜像
FROM python:3.10-slim

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libprotobuf-dev \
    protobuf-compiler \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 设置工作目录
WORKDIR /app

COPY . /app

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# 安装依赖
RUN uv sync --verbose

# 生成 gRPC Python 文件
RUN uv run -m grpc_tools.protoc -I ./protobufs --python_out=. --grpc_python_out=. ./protobufs/generalAPI.proto

# 暴露端口
EXPOSE 7070

# 启动命令
CMD ["uv", "run", "server.py"]