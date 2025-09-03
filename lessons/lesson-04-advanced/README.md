# Lesson 4: 高级技巧与最佳实践

## 🎯 学习目标

- 掌握 Extended Thinking 模式的使用
- 理解 Plan 模式 + TDD 工作流
- 学习 Context 管理的高级技巧
- 掌握项目级别的最佳实践

## 📖 理论基础

### Extended Thinking 模式

Extended Thinking 是 Claude Code 的高级功能，允许 AI 进行更深度的思考和分析。

#### 思考级别
```bash
think          # 基础思考
think hard     # 深度思考  
think harder   # 更深度思考
ultrathink     # 极限思考模式
```

#### 使用场景
- **复杂问题分析** - 需要多角度思考的问题
- **架构设计** - 系统级的设计决策
- **性能优化** - 需要深度分析的性能问题
- **故障排查** - 复杂的系统问题诊断

### Plan 模式 + TDD 工作流

Plan 模式允许 Claude 先分析项目结构，然后制定实施计划，特别适合复杂项目。

#### TDD (Test-Driven Development) 原则
- 先写测试，基于输入输出对
- 不要创建 mock 实现
- 测试驱动开发，确保功能正确性

## 🚀 实战演练

### Extended Thinking 实践

#### 案例 1: 复杂架构设计

```bash
# 使用 Extended Thinking 分析微服务架构
think harder
请分析这个微服务架构的性能瓶颈和设计问题：
- API Gateway -> User Service -> Database
- Order Service -> Redis Cache  
- Payment Service -> External API
- Notification Service -> Message Queue
```

#### 案例 2: 性能问题深度分析

```bash
ultrathink
深度分析这个系统的性能问题：
1. 用户服务响应时间偶尔超过 2s
2. 订单服务在高并发时出现超时
3. 支付服务有重复支付的 bug
4. 通知服务消息积压
```

### Plan 模式 + TDD 实践

#### 案例 1: 微服务重构计划

```bash
/plan analyze-codesbase "分析这个微服务架构的性能瓶颈"
```

**Plan 模式输出包含**：
- 项目结构分析
- 性能瓶颈识别
- 重构优先级
- 实施步骤

#### 案例 2: TDD 工作流

```bash
# 先写测试
请为用户服务编写测试，基于以下输入输出对：
输入: {username: "test", password: "123456"}
输出: {success: true, token: "jwt-token", user: {id: 1, username: "test"}}

# 然后实现功能
基于测试实现用户登录功能，不要创建 mock
```

## 🎯 高级 Context 管理

### 1. Context 清理策略

```bash
# 频繁使用 /clear 保持上下文清洁
/clear

# 使用 @文件名 精确引用
@user-service.js 中的登录函数

# 使用分段处理复杂任务
task1: 分析数据结构
task2: 识别性能问题  
task3: 制定优化方案
```

### 2. 项目级别的 Context 管理

创建 `.claude/` 项目配置：
```
.claude/
├── agents/           # 项目专用 agents
├── commands/         # 项目专用命令
└── hooks/           # 项目级 hooks
```

### 3. 敏感信息管理

```bash
# 使用环境变量
process.env.DB_PASSWORD
process.env.API_KEY

# 避免硬编码敏感信息
❌ const dbPassword = "admin123"
✅ const dbPassword = process.env.DB_PASSWORD
```

## 📊 高级工作流模板

### 1. 完整的项目开发工作流

```bash
# 阶段 1: 需求分析
think hard
分析这个需求的业务逻辑和技术实现要点

# 阶段 2: 架构设计
/plan design-architecture "设计系统架构和组件关系"

# 阶段 3: TDD 开发
# 3.1 编写测试
为核心功能编写测试，定义输入输出对

# 3.2 实现功能
基于测试实现功能，确保测试通过

# 阶段 4: 代码审查
linus-code-reviewer 审查实现的代码

# 阶段 5: 安全检查
security-expert 检查安全问题

# 阶段 6: 性能优化
performance-expert 分析性能瓶颈
```

### 2. 生产问题排查工作流

```bash
# 阶段 1: 问题收集
收集错误日志、监控指标、用户反馈

# 阶段 2: 深度分析
ultrathink
分析这些问题的根本原因和关联性

# 阶段 3: 多角度验证
data-analyzer 分析数据模式
system-expert 分析系统架构
security-expert 排查安全相关问题

# 阶段 4: 解决方案
基于多代理分析结果制定解决方案

# 阶段 5: 实施和验证
分步骤实施解决方案，验证效果
```

### 3. 代码重构工作流

```bash
# 阶段 1: 现状分析
think harder
分析当前代码的问题和重构必要性

# 阶段 2: 重构规划
refactoring-specialist 制定重构计划

# 阶段 3: TDD 保护
为现有功能编写测试，确保重构不破坏功能

# 阶段 4: 分步重构
按照优先级分步骤进行重构

# 阶段 5: 验证和优化
验证重构效果，进行性能优化
```

## 💡 最佳实践总结

### 1. 项目组织原则

```
项目根目录/
├── .claude/              # Claude 配置
│   ├── agents/          # 专用代理
│   ├── commands/        # 自定义命令
│   └── hooks/          # 项目 hooks
├── src/                 # 源代码
├── tests/              # 测试代码
├── docs/               # 项目文档
└── README.md          # 项目说明
```

### 2. 代码质量标准

- **Linus 品味**: 消除特殊情况，数据结构优先
- **安全第一**: 所有外部输入都验证
- **性能意识**: 避免不必要的复杂度
- **测试覆盖**: 核心功能必须有测试

### 3. 工作流优化

- **使用 Extended Thinking**: 复杂问题深度分析
- **Plan 模式先行**: 大改动先做计划
- **TDD 开发**: 测试驱动功能实现
- **多代理协作**: 复杂任务分工处理

### 4. 团队协作

- **共享配置**: .claude/ 目录提交到 git
- **统一标准**: 团队使用相同的 agents 和 commands
- **代码审查**: 使用标准化的审查流程
- **知识沉淀**: 文档化经验和最佳实践

## 🎯 实战案例

### 案例 1: 电商平台性能优化

```bash
# 1. 问题分析
ultrathink
分析电商平台的性能问题：
- 首页加载慢
- 商品搜索响应时间长
- 订单处理偶尔超时

# 2. 多代理分析
performance-expert 分析系统瓶颈
data-analyzer 分析用户行为模式
infrastructure-expert 分析基础设施问题

# 3. 制定优化方案
基于分析结果制定分阶段优化计划

# 4. 实施和验证
分步骤实施优化措施，验证效果
```

### 案例 2: 微服务架构重构

```bash
# 1. 现状分析
think harder
分析当前单体应用的问题和微服务化的必要性

# 2. 架构设计
/plan design-microservices "设计微服务架构和拆分方案"

# 3. TDD 实施
为每个微服务编写测试，然后实现功能

# 4. 迁移策略
制定数据迁移和服务切换策略

# 5. 验证和优化
验证微服务架构的性能和可靠性
```

## 📝 练习作业

1. **Extended Thinking 练习**: 使用 `think harder` 分析一个复杂的业务问题

2. **Plan 模式练习**: 使用 `/plan` 命令制定一个项目重构计划

3. **TDD 练习**: 为一个现有功能编写测试，然后重构实现

4. **综合练习**: 创建一个包含 Extended Thinking、Plan 模式、TDD 的完整工作流

## 🎓 总结

- Extended Thinking 让 AI 进行更深度的思考和分析
- Plan 模式 + TDD 确保项目开发的系统性和可靠性
- Context 管理是高级用户的核心技能
- 好的最佳实践 = 系统性方法 + 专业工具 + 团队协作

---

**课程完成**: 恭喜！你已经掌握了 Claude Code 的高级技巧，开始在实际项目中应用这些技能吧！