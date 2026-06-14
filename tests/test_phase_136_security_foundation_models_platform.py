"""
Comprehensive testing module for Security Foundation Models Platform
"""

import pytest
from src.phase_136_security_foundation_models_platform.models import FoundationModel, ModelTrainingJob, EvaluationReport, DeploymentConfig
from src.phase_136_security_foundation_models_platform.store import get_store
from src.phase_136_security_foundation_models_platform.service import get_service
from src.phase_136_security_foundation_models_platform.analytics import SecurityFoundationModelsPlatformAnalytics

def test_models_to_dict():
    obj = FoundationModel()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = FoundationModel.from_dict(d)
    assert obj2.model_id == obj.model_id

    obj = ModelTrainingJob()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = ModelTrainingJob.from_dict(d)
    assert obj2.job_id == obj.job_id

    obj = EvaluationReport()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = EvaluationReport.from_dict(d)
    assert obj2.report_id == obj.report_id

    obj = DeploymentConfig()
    d = obj.to_dict()
    assert isinstance(d, dict)
    obj2 = DeploymentConfig.from_dict(d)
    assert obj2.config_id == obj.config_id

def test_store_operations():
    store = get_store()
    obj = FoundationModel()
    store.add_foundationmodel(obj)
    assert store.get_foundationmodel(obj.model_id) is not None
    assert len(store.list_foundationmodels()) >= 1

    obj = ModelTrainingJob()
    store.add_modeltrainingjob(obj)
    assert store.get_modeltrainingjob(obj.job_id) is not None
    assert len(store.list_modeltrainingjobs()) >= 1

    obj = EvaluationReport()
    store.add_evaluationreport(obj)
    assert store.get_evaluationreport(obj.report_id) is not None
    assert len(store.list_evaluationreports()) >= 1

    obj = DeploymentConfig()
    store.add_deploymentconfig(obj)
    assert store.get_deploymentconfig(obj.config_id) is not None
    assert len(store.list_deploymentconfigs()) >= 1

def test_service_methods():
    srv = get_service()
    assert srv.register_model(name="test", task_type="test") is not None
    assert srv.train_model(model_id="test", dataset_path="test") is not None
    assert srv.evaluate_model(model_id="test") is not None
    assert srv.deploy_model(model_id="test") is not None
    assert srv.execute("tenant-123")["status"] == "success"

def test_analytics():
    calc = SecurityFoundationModelsPlatformAnalytics()
    assert calc.calculate_kpis()["efficiency_rating"] == 98.4
    assert calc.generate_dashboard_metrics()["system_health"] == 100.0
