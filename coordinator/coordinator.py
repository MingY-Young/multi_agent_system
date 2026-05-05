import asyncio
from typing import Dict, List, Optional
from datetime import datetime
from core.models import Agent, Task, AgentStatus


class Coordinator:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_queue: asyncio.PriorityQueue = None
        self.completed_tasks: List[Task] = []
        self.event_log: List[Dict] = []
        self._running = False

    async def initialize(self):
        self.task_queue = asyncio.PriorityQueue()
        self._running = True
        self._dispatcher_task = asyncio.create_task(self._dispatch_loop())

    async def shutdown(self):
        self._running = False
        if hasattr(self, '_dispatcher_task'):
            self._dispatcher_task.cancel()

    def register_agent(self, agent: Agent):
        self.agents[agent.agent_id] = agent
        self._log_event("agent_registered", {"agent_id": agent.agent_id, "name": agent.name})

    def get_available_agent(self, task_type: str) -> Optional[Agent]:
        available = [
            agent for agent in self.agents.values()
            if agent.status == AgentStatus.IDLE and agent.can_handle(task_type)
        ]
        if available:
            return available[0]
        return None

    async def submit_task(self, task: Task) -> str:
        self.tasks[task.task_id] = task
        await self.task_queue.put((task.priority, task.task_id))
        self._log_event("task_submitted", {"task_id": task.task_id, "type": task.task_type})
        return task.task_id

    async def _dispatch_loop(self):
        while self._running:
            try:
                if not self.task_queue.empty():
                    _, task_id = await self.task_queue.get()
                    task = self.tasks.get(task_id)
                    if task and task.status == "pending":
                        await self._dispatch_task(task)
                await asyncio.sleep(0.1)
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Dispatcher error: {e}")

    async def _dispatch_task(self, task: Task):
        agent = self.get_available_agent(task.task_type)
        if agent:
            self._log_event("task_dispatched", {
                "task_id": task.task_id,
                "agent_id": agent.agent_id
            })
            result = await agent.execute_task(task)
            self._log_event("task_completed", {
                "task_id": task.task_id,
                "result": result.get("status")
            })
            self.completed_tasks.append(task)
        else:
            await self.task_queue.put((task.priority + 100, task.task_id))
            self._log_event("task_waiting", {"task_id": task.task_id, "reason": "no_available_agent"})

    def _log_event(self, event_type: str, data: Dict):
        self.event_log.append({
            "type": event_type,
            "data": data,
            "timestamp": datetime.now().isoformat()
        })

    def get_system_status(self) -> Dict:
        return {
            "total_agents": len(self.agents),
            "active_agents": sum(1 for a in self.agents.values() if a.status == AgentStatus.WORKING),
            "total_tasks": len(self.tasks),
            "pending_tasks": sum(1 for t in self.tasks.values() if t.status == "pending"),
            "completed_tasks": len(self.completed_tasks),
            "agents": [a.to_dict() for a in self.agents.values()]
        }

    def get_task_status(self, task_id: str) -> Optional[Dict]:
        task = self.tasks.get(task_id)
        return task.to_dict() if task else None

    def get_event_log(self, limit: int = 50) -> List[Dict]:
        return self.event_log[-limit:]


coordinator = Coordinator()
