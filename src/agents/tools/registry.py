import logging
from typing import Callable, Dict

logger = logging.getLogger(__name__)

class ToolRegistry:
    """
    Secure registry of executable actions available to the Digital Workforce.
    Enforces RBAC before tool execution.
    """
    def __init__(self):
        self._tools: Dict[str, Callable] = {}

    def register_tool(self, name: str, func: Callable):
        self._tools[name] = func
        logger.info(f"Registered tool: {name}")

    def execute_tool(self, name: str, kwargs: dict, tenant_id: str, allowed_tools: list) -> any:
        if name not in allowed_tools:
            logger.warning(f"Tenant {tenant_id} attempted unauthorized tool access: {name}")
            raise PermissionError(f"Agent is not authorized to use tool: {name}")
            
        if name not in self._tools:
            raise ValueError(f"Tool {name} does not exist in registry.")
            
        logger.info(f"Executing tool {name} for tenant {tenant_id}")
        return self._tools[name](**kwargs)

registry = ToolRegistry()
