import asyncio
import uuid
import os
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from coordinator.coordinator import coordinator, Agent, Task


app = FastAPI(title="Multi-Agent Collaboration System", version="1.0.0")

web_path = os.path.join(os.path.dirname(__file__), "..", "web")
if os.path.exists(web_path):
    app.mount("/static", StaticFiles(directory=web_path), name="static")

@app.get("/web")
async def root():
    return FileResponse(os.path.join(web_path, "index.html"))

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TaskCreate(BaseModel):
    task_type: str
    payload: Dict
    priority: int = 1


class TaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


class AgentCreate(BaseModel):
    name: str
    role: str
    capabilities: List[str]


@app.on_event("startup")
async def startup():
    await coordinator.initialize()

    agents = [
        Agent("agent_001", "数据采集员", "DataCollector", ["data_collection"]),
        Agent("agent_002", "数据分析师", "DataAnalyzer", ["data_analysis", "data_collection"]),
        Agent("agent_003", "报告生成员", "ReportGenerator", ["report_generation"]),
        Agent("agent_004", "通知专员", "Notifier", ["notification"]),
        Agent("agent_005", "任务规划师", "TaskPlanner", ["task_planning", "data_analysis"]),
    ]

    for agent in agents:
        coordinator.register_agent(agent)


@app.get("/")
async def root():
    return {"message": "Multi-Agent Collaboration System API", "version": "1.0.0"}


@app.get("/api/status")
async def get_status():
    return coordinator.get_system_status()


@app.get("/api/agents")
async def list_agents():
    return {
        "agents": [agent.to_dict() for agent in coordinator.agents.values()]
    }


@app.get("/api/agents/{agent_id}")
async def get_agent(agent_id: str):
    agent = coordinator.agents.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent.to_dict()


@app.post("/api/agents")
async def create_agent(agent_data: AgentCreate):
    agent_id = f"agent_{uuid.uuid4().hex[:8]}"
    agent = Agent(
        agent_id=agent_id,
        name=agent_data.name,
        role=agent_data.role,
        capabilities=agent_data.capabilities
    )
    coordinator.register_agent(agent)
    return {"agent_id": agent_id, "message": "Agent created successfully"}


@app.get("/api/tasks")
async def list_tasks(status: Optional[str] = None):
    tasks = list(coordinator.tasks.values())
    if status:
        tasks = [t for t in tasks if t.status == status]
    return {"tasks": [t.to_dict() for t in tasks]}


@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    task_info = coordinator.get_task_status(task_id)
    if not task_info:
        raise HTTPException(status_code=404, detail="Task not found")
    return task_info


@app.post("/api/tasks")
async def create_task(task_data: TaskCreate):
    task_id = f"task_{uuid.uuid4().hex[:8]}"
    task = Task(
        task_id=task_id,
        task_type=task_data.task_type,
        payload=task_data.payload,
        priority=task_data.priority
    )
    await coordinator.submit_task(task)
    return {"task_id": task_id, "message": "Task submitted successfully"}


@app.get("/api/events")
async def get_events(limit: int = 50):
    return {"events": coordinator.get_event_log(limit)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
