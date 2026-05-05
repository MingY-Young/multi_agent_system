from enum import Enum
from typing import Dict, List, Any, Optional
from datetime import datetime
import asyncio


class AgentStatus(Enum):
    IDLE = "idle"
    WORKING = "working"
    WAITING = "waiting"
    ERROR = "error"


class Task:
    def __init__(self, task_id: str, task_type: str, payload: Dict[str, Any], priority: int = 1):
        self.task_id = task_id
        self.task_type = task_type
        self.payload = payload
        self.priority = priority
        self.status = "pending"
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.result = None
        self.error = None
        self.assignee = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_type": self.task_type,
            "payload": self.payload,
            "priority": self.priority,
            "status": self.status,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "result": self.result,
            "error": self.error,
            "assignee": self.assignee
        }


class Agent:
    def __init__(self, agent_id: str, name: str, role: str, capabilities: List[str]):
        self.agent_id = agent_id
        self.name = name
        self.role = role
        self.capabilities = capabilities
        self.status = AgentStatus.IDLE
        self.current_task = None
        self.task_history = []
        self.performance_metrics = {
            "tasks_completed": 0,
            "tasks_failed": 0,
            "avg_execution_time": 0
        }

    def can_handle(self, task_type: str) -> bool:
        return task_type in self.capabilities

    async def execute_task(self, task: Task) -> Dict[str, Any]:
        task.status = "running"
        task.started_at = datetime.now()
        task.assignee = self.agent_id
        self.status = AgentStatus.WORKING
        self.current_task = task

        try:
            await asyncio.sleep(0.5)

            if task.task_type == "data_collection":
                result = await self._collect_data(task.payload)
            elif task.task_type == "data_analysis":
                result = await self._analyze_data(task.payload)
            elif task.task_type == "report_generation":
                result = await self._generate_report(task.payload)
            elif task.task_type == "notification":
                result = await self._send_notification(task.payload)
            elif task.task_type == "task_planning":
                result = await self._plan_tasks(task.payload)
            else:
                result = {"status": "completed", "output": f"Task {task.task_id} processed by {self.name}"}

            task.status = "completed"
            task.completed_at = datetime.now()
            task.result = result
            self.performance_metrics["tasks_completed"] += 1
            self.task_history.append(task)

        except Exception as e:
            task.status = "failed"
            task.error = str(e)
            task.completed_at = datetime.now()
            self.performance_metrics["tasks_failed"] += 1

        finally:
            self.status = AgentStatus.IDLE
            self.current_task = None

        return task.to_dict()

    async def _collect_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        data_source = payload.get("data_source", "unknown")
        return {
            "status": "completed",
            "data_collected": {
                "records": 150,
                "source": data_source,
                "timestamp": datetime.now().isoformat()
            }
        }

    async def _analyze_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = payload.get("data", {})
        return {
            "status": "completed",
            "analysis": {
                "total_records": 150,
                "patterns_found": 5,
                "insights": ["用户活跃度上升", "转化率提升", "留存率稳定"]
            }
        }

    async def _generate_report(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        report_type = payload.get("report_type", "daily")
        return {
            "status": "completed",
            "report": {
                "type": report_type,
                "title": f"{report_type.capitalize()}运营报告",
                "summary": "整体运营状况良好",
                "generated_at": datetime.now().isoformat()
            }
        }

    async def _send_notification(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        channel = payload.get("channel", "email")
        recipient = payload.get("recipient", "unknown")
        return {
            "status": "completed",
            "notification": {
                "channel": channel,
                "recipient": recipient,
                "sent": True,
                "sent_at": datetime.now().isoformat()
            }
        }

    async def _plan_tasks(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "status": "completed",
            "plan": {
                "tasks": [
                    {"id": "t1", "type": "data_collection", "priority": 1},
                    {"id": "t2", "type": "data_analysis", "priority": 2, "depends_on": ["t1"]},
                    {"id": "t3", "type": "report_generation", "priority": 3, "depends_on": ["t2"]}
                ]
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "role": self.role,
            "capabilities": self.capabilities,
            "status": self.status.value,
            "current_task": self.current_task.task_id if self.current_task else None,
            "performance_metrics": self.performance_metrics
        }
