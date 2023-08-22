# 运行python
FROM python:3.11-alpine

WORKDIR /app
COPY . .

# 设置软件源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
# 设置时区
RUN apk --no-cache add tzdata  && \
    ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone \
# 安装pip源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && \
    python -m pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 环境
ENV REDIS_HOST = "localhost"
ENV REDIS_PASSWORD = "123456"

# 暴露端口
EXPOSE 23457

# 入口
ENTRYPOINT ["python", "main.py"]