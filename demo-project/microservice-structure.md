# 微服务架构示例

## 服务架构
```
API Gateway -> User Service -> Database
            -> Order Service -> Redis Cache
            -> Payment Service -> External API
            -> Notification Service -> Message Queue
```

## 已知性能问题
1. User Service 响应时间偶尔超过 2s
2. Order Service 在高并发时出现超时
3. Payment Service 有重复支付的 bug
4. Notification Service 消息积压

## 技术栈
- Node.js + Express
- PostgreSQL + Redis
- RabbitMQ
- Docker + Kubernetes