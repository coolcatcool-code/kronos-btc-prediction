FROM ubuntu:latest

# 安装基本依赖
RUN apt update && apt install -y \
    python3 \
    python3-pip \
    git \
    build-essential

# 复制项目文件
COPY . /app
WORKDIR /app

# 安装Python依赖
RUN pip3 install --break-system-packages -r requirements.txt

# 设置启动命令
CMD ["python3", "update_predictions.py"]