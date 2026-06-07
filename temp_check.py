from src.api.services.fraud_service import FraudService
from src.api.services.scoring_service import ScoringService

svc = FraudService(ScoringService())
try:
    svc.detect_fraud([1, 2, 3])
    print('no error')
except Exception as e:
    print('error', type(e).__name__)
