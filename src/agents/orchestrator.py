import asyncio
import logging
import uuid
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class AgentTask(BaseModel):
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    agent_type: str
    trigger_event: Dict[str, Any]
    status: str = "PENDING"
    assigned_tenant_id: str
    execution_trace: list = []

class AgentOrchestrationService:
    """
    Manages the lifecycle of AI agents (Digital Workforce).
    Supervisor pattern that dequeues tasks and assigns them to worker personas.
    """
    def __init__(self):
        self.active_tasks: Dict[str, AgentTask] = {}
        self.lock = asyncio.Lock()

    async def assign_task(self, tenant_id: str, agent_type: str, event_payload: dict) -> str:
        async with self.lock:
            task = AgentTask(
                agent_type=agent_type,
                trigger_event=event_payload,
                assigned_tenant_id=tenant_id
            )
            self.active_tasks[task.task_id] = task
            logger.info(f"Task {task.task_id} assigned to {agent_type} for tenant {tenant_id}")
            
            # Start background processing
            asyncio.create_task(self._process_task(task))
            return task.task_id

    async def _process_task(self, task: AgentTask):
        task.status = "IN_PROGRESS"
        logger.info(f"Processing task {task.task_id} with Agent: {task.agent_type}")
        try:
            # Simulated ReAct Loop execution
            await asyncio.sleep(2)
            task.execution_trace.append({"thought": "Analyzing payload", "action": "None", "observation": "Payload parsed"})
            
            # Logic routes to specific persona here (L1_ANALYST, INVESTIGATOR)
            
            task.status = "COMPLETED"
            logger.info(f"Task {task.task_id} completed successfully.")
        except Exception as e:
            logger.error(f"Task {task.task_id} failed: {e}")
            task.status = "FAILED"

    async def get_task_status(self, task_id: str) -> Optional[AgentTask]:
        return self.active_tasks.get(task_id)

orchestrator = AgentOrchestrationService()
