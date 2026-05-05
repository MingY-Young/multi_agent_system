
## 功能特性

- 🚀 **多Agent架构**：支持多种角色的Agent协同工作
- 🔄 **任务分发**：智能任务分配和执行
- 📊 **实时监控**：系统状态和任务进度追踪
- 📱 **Web界面**：可视化管理控制台
- 📡 **REST API**：完整的API接口支持

## 内置Agent角色

| Agent ID | 名称 | 角色 | 能力 |
|----------|------|------|------|
| agent_001 | 数据采集员 | DataCollector | 数据采集 |
| agent_002 | 数据分析师 | DataAnalyzer | 数据分析、数据采集 |
| agent_003 | 报告生成员 | ReportGenerator | 报告生成 |
| agent_004 | 通知专员 | Notifier | 通知推送 |
| agent_005 | 任务规划师 | TaskPlanner | 任务规划、数据分析 |

## 技术栈

- **框架**: FastAPI 0.104.1
- **服务器**: Uvicorn 0.24.0
- **数据验证**: Pydantic 2.5.0
- **异步支持**: Asyncio

## 安装与运行

### 环境要求

- Python 3.8+
- pip 20.0+

### 安装依赖

```bash
cd multi_agent_system
pip install -r requirements.txt
```

### 启动服务

```bash
python run.py
```

启动后访问：
- **API地址**: http://localhost:8000
- **Web界面**: http://localhost:8000/web
- **API文档**: http://localhost:8000/docs

## API接口

### 基础接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/` | 健康检查 |
| GET | `/api/status` | 获取系统状态 |
| GET | `/api/events` | 获取事件日志 |

### Agent管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/agents` | 列出所有Agent |
| GET | `/api/agents/{agent_id}` | 获取单个Agent详情 |
| POST | `/api/agents` | 创建新Agent |

### 任务管理

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/tasks` | 列出所有任务 |
| GET | `/api/tasks/{task_id}` | 获取任务状态 |
| POST | `/api/tasks` | 提交新任务 |

### API使用示例

**创建任务**
```bash
curl -X POST http://localhost:8000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "task_type": "data_collection",
    "payload": {"source": "database", "query": "SELECT * FROM users"},
    "priority": 1
  }'
```

**获取任务列表**
```bash
curl http://localhost:8000/api/tasks
```

**获取系统状态**
```bash
curl http://localhost:8000/api/status
```

## 开发说明

### 添加新Agent

通过API动态注册新Agent：

```bash
curl -X POST http://localhost:8000/api/agents \
  -H "Content-Type: application/json" \
  -d '{
    "name": "新Agent",
    "role": "NewRole",
    "capabilities": ["capability1", "capability2"]
  }'
```

### 扩展功能

1. 在 `coordinator/coordinator.py` 中添加新的Agent类型
2. 在 `api/main.py` 中添加新的API端点
3. 在 `core/models.py` 中定义新的数据模型

## 许可证

MIT License
