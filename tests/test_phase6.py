import pytest
import torch
from src.models.risk_model import FraudDetectionModel

@pytest.mark.parametrize("model_type", ["HTGAT", "GRAPHSAGE", "TGAT", "TGN"])
def test_forward_outputs(model_type):
    model = FraudDetectionModel(
        node_feature_dim=64,
        hidden_dim=128,
        output_dim=64,
        num_node_types=5,
        num_edge_types=5,
        num_layers=2,
        heads=4,
        dropout=0.2,
        temporal_dim=16,
        model_type=model_type,
    )
    # Create dummy inputs
    num_nodes = 10
    x = torch.randn(num_nodes, 64)
    edge_index = torch.tensor([[0, 1, 2, 3], [1, 2, 3, 4]], dtype=torch.long)
    edge_attr = torch.randn(edge_index.size(1), 16)
    edge_timestamp = torch.randn(edge_index.size(1))
    out = model(
        x=x,
        edge_index=edge_index,
        edge_attr=edge_attr,
        edge_timestamp=edge_timestamp,
        return_embedding=False,
    )
    assert "risk" in out
    assert "graph_embedding" in out
    assert "anomaly_mask" in out
    # Ensure shapes are correct
    assert out["risk"].shape == torch.Size([])
    assert out["graph_embedding"].dim() >= 2
    assert out["anomaly_mask"].shape == x.shape[:1]
