# 编译GO
FROM golang:1.21-alpine as builder

WORKDIR /app
COPY . .

RUN go env -w GO111MODULE=on \
    && go env -w GOPROXY=https://goproxy.cn,direct \
    && go env -w CGO_ENABLED=0 \
    && go env \
    && go mod tidy \
    && go build -o main .

FROM alpine:latest

WORKDIR /app

# 设置软件源
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g' /etc/apk/repositories
# 设置时区
RUN apk --no-cache add tzdata && \
    cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && \
    echo "Asia/Shanghai" > /etc/timezone

COPY --from=builder /app/main ./
RUN ls -al
ENV PROXY_ADDR = "127.0.0.1:23457"

EXPOSE 23456

ENTRYPOINT ./main