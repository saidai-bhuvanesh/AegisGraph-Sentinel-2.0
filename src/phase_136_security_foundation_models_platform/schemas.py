"""
FastAPI request/response schemas for Security Foundation Models Platform
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Any

class FoundationModelSchema(BaseModel):
    model_id: Optional[str] = None
    name: Optional[str] = None
    version: Optional[str] = None
    task_type: Optional[str] = None

class ModelTrainingJobSchema(BaseModel):
    job_id: Optional[str] = None
    model_id: Optional[str] = None
    dataset_path: Optional[str] = None
    status: Optional[str] = None

class EvaluationReportSchema(BaseModel):
    report_id: Optional[str] = None
    model_id: Optional[str] = None
    precision: Optional[float] = None
    recall: Optional[float] = None

class DeploymentConfigSchema(BaseModel):
    config_id: Optional[str] = None
    replicas: Optional[int] = None
    endpoint: Optional[str] = None

class ExecutionRequest(BaseModel):
    tenant_id: str
    parameters: Optional[Dict[str, Any]] = None

class ExecutionResponse(BaseModel):
    status: str
    phase: int
    result: Dict[str, Any]
