# 使用 Python 3.11 官方镜像作为基础镜像
FROM python:3.11-slim-buster
# 安装 Java
RUN apt-get update && \
    apt-get install -y openjdk-11-jre && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器的工作目录
COPY . /app

# 安装 Flask 和 zxing
RUN pip install Flask zxing
RUN pip install qrcode[pil]
RUN pip install matplotlib
# 公开容器内的端口 5000
EXPOSE 5002

# 创建 uploads 目录
RUN mkdir -p /app/uploads
RUN chmod -R 777 uploads

# 设置环境变量以确保 Flask 在生产模式下运行
# ENV FLASK_ENV=production

# 运行 Flask 应用
CMD [ "python", "app.py"]

