"""
Unit tests for AegisGraph Sentinel Advanced GNN models (GraphSAGE, TGAT, TGN)
"""

import pytest
import torch
import numpy as np
from datetime import datetime, timezone

from src.models.graphsage import GraphSAGEConv, GraphSAGE
from src.models.tgat import TGATConv, TGAT
from src.models.tgn import TGNMemory, GRUMemoryUpdater, TGN
from src.models.risk_model import FraudDetectionModel


class TestGraphSAGE:
    """Test GraphSAGE layers and network model"""
    
    def test_graphsage_conv_forward(self):
        in_channels = 32
        out_channels = 64
        num_node_types = 3
        num_edge_types = 2
        
        # Test mean aggregator
        conv_mean = GraphSAGEConv(
            in_channels=in_channels,
            out_channels=out_channels,
            num_node_types=num_node_types,
            num_edge_types=num_edge_types,
            aggregator_type='mean',
        )
        
        num_nodes = 8
        num_edges = 12
        x = torch.randn(num_nodes, in_channels)
        edge_index = torch.randint(0, num_nodes, (2, num_edges))
        node_type = torch.randint(0, num_node_types, (num_nodes,))
        
        out_mean = conv_mean(x, edge_index, node_type)
        assert out_mean.shape == (num_nodes, out_channels)
        
        # Test pooling aggregator
        conv_pool = GraphSAGEConv(
            in_channels=in_channels,
            out_channels=out_channels,
            num_node_types=num_node_types,
            num_edge_types=num_edge_types,
            aggregator_type='pooling',
        )
        out_pool = conv_pool(x, edge_index, node_type)
        assert out_pool.shape == (num_nodes, out_channels)
        
        # Test LSTM aggregator
        conv_lstm = GraphSAGEConv(
            in_channels=in_channels,
            out_channels=out_channels,
            num_node_types=num_node_types,
            num_edge_types=num_edge_types,
            aggregator_type='lstm',
        )
        out_lstm = conv_lstm(x, edge_index, node_type)
        assert out_lstm.shape == (num_nodes, out_channels)
        
    def test_graphsage_model(self):
        model = GraphSAGE(
            in_channels=16,
            hidden_channels=32,
            out_channels=16,
            num_node_types=2,
            num_edge_types=2,
            num_layers=2,
        )
        
        num_nodes = 10
        x = torch.randn(num_nodes, 16)
        edge_index = torch.randint(0, num_nodes, (2, 15))
        node_type = torch.randint(0, 2, (num_nodes,))
        
        out = model(x, edge_index, node_type)
        assert out.shape == (num_nodes, 16)


class TestTGAT:
    """Test TGAT temporal layers and network model"""
    
    def test_tgat_conv_forward(self):
        in_channels = 32
        out_channels = 16
        num_node_types = 3
        num_edge_types = 2
        heads = 4
        
        conv = TGATConv(
            in_channels=in_channels,
            out_channels=out_channels,
            num_node_types=num_node_types,
            num_edge_types=num_edge_types,
            heads=heads,
            temporal_dim=16,
        )
        
        num_nodes = 8
        num_edges = 12
        x = torch.randn(num_nodes, in_channels)
        edge_index = torch.randint(0, num_nodes, (2, num_edges))
        node_type = torch.randint(0, num_node_types, (num_nodes,))
        edge_timestamp = torch.randn(num_edges)
        
        out = conv(x, edge_index, node_type, edge_timestamp=edge_timestamp)
        assert out.shape == (num_nodes, heads * out_channels)
        
    def test_tgat_model(self):
        model = TGAT(
            in_channels=16,
            hidden_channels=32,
            out_channels=16,
            num_node_types=2,
            num_edge_types=2,
            num_layers=2,
            heads=4,
        )
        
        num_nodes = 10
        x = torch.randn(num_nodes, 16)
        edge_index = torch.randint(0, num_nodes, (2, 15))
        node_type = torch.randint(0, 2, (num_nodes,))
        edge_timestamp = torch.randn(15)
        
        out = model(x, edge_index, node_type, edge_timestamp=edge_timestamp)
        assert out.shape == (num_nodes, 16)


class TestTGN:
    """Test TGN memory, GRU updater, and network model"""
    
    def test_tgn_memory(self):
        num_nodes = 20
        memory_dim = 16
        
        memory = TGNMemory(num_nodes, memory_dim)
        assert memory.memory.shape == (num_nodes, memory_dim)
        
        # Test retrieval
        indices = torch.tensor([1, 3, 5])
        states = memory.get_memory(indices)
        assert states.shape == (3, memory_dim)
        
        # Test update
        new_values = torch.randn(3, memory_dim)
        memory.set_memory(indices, new_values)
        updated_states = memory.get_memory(indices)
        assert torch.allclose(updated_states, new_values)
        
        # Test dynamic resizing
        out_of_bounds_indices = torch.tensor([25])
        states_resized = memory.get_memory(out_of_bounds_indices)
        assert states_resized.shape == (1, memory_dim)
        assert memory.num_nodes > 25
        
        # Test reset
        memory.reset_memory()
        assert torch.all(memory.memory == 0)
        
    def test_gru_updater(self):
        message_dim = 24
        memory_dim = 16
        
        updater = GRUMemoryUpdater(message_dim, memory_dim)
        messages = torch.randn(5, message_dim)
        memory = torch.randn(5, memory_dim)
        
        new_memory = updater(messages, memory)
        assert new_memory.shape == (5, memory_dim)
        
    def test_tgn_model(self):
        model = TGN(
            in_channels=16,
            hidden_channels=32,
            out_channels=16,
            num_node_types=2,
            num_edge_types=2,
            num_nodes=100,
            memory_dim=32,
            temporal_dim=16,
        )
        
        num_nodes = 15
        x = torch.randn(num_nodes, 16)
        edge_index = torch.randint(0, num_nodes, (2, 10))
        node_type = torch.randint(0, 2, (num_nodes,))
        edge_timestamp = torch.randn(10)
        
        # Reset memory state
        model.memory_module.reset_memory()
        
        out = model(x, edge_index, node_type, edge_timestamp=edge_timestamp)
        assert out.shape == (num_nodes, 16)


class TestDynamicRiskModel:
    """Test FraudDetectionModel selected backbones dynamically"""
    
    @pytest.mark.parametrize("model_type", ["HTGAT", "GRAPHSAGE", "TGAT", "TGN"])
    def test_backbone_switching(self, model_type):
        model = FraudDetectionModel(
            node_feature_dim=32,
            hidden_dim=64,
            output_dim=32,
            num_node_types=3,
            num_edge_types=2,
            model_type=model_type,
        )
        
        num_nodes = 10
        x = torch.randn(num_nodes, 32)
        edge_index = torch.randint(0, num_nodes, (2, 15))
        node_type = torch.randint(0, 3, (num_nodes,))
        edge_timestamp = torch.randn(15)
        
        # Run forward pass
        result = model(
            x=x,
            edge_index=edge_index,
            node_type=node_type,
            edge_timestamp=edge_timestamp,
        )
        
        assert 'risk' in result
        assert 0.0 <= result['risk'].item() <= 1.0
