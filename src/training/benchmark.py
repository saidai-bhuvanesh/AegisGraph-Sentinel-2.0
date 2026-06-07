"""
Benchmark Comparisons for AegisGraph Sentinel 2.0 GNN Backbones

Compares HTGAT, GraphSAGE, TGAT, and TGN on:
- Validation F1-Score
- Validation ROC-AUC
- Training speed (seconds/epoch)
- Inference latency (milliseconds/transaction)
"""

import time
import torch
import numpy as np
from datetime import datetime, timezone
from torch.utils.data import DataLoader

from src.data.graph_constructor import TemporalGraphConstructor, create_sample_transactions
from src.models.risk_model import FraudDetectionModel
from src.training.production_trainer import ProductionTrainer, SimpleGraphDataset, collate_graphs


def run_benchmark():
    print("=" * 80)
    print("AEGISGRAPH SENTINEL 2.0 - GNN BACKBONE BENCHMARK SUITE")
    print("=" * 80)
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Device: {device}")
    
    # 1. Dataset Generation
    print("\nGenerating benchmark dataset...")
    graphs = []
    labels = []
    
    # Create a baseline constructor to track overall unique nodes
    base_constructor = TemporalGraphConstructor(time_window_hours=24)
    base_constructor.add_transactions(create_sample_transactions())
    num_nodes = len(base_constructor.node_to_idx)
    
    for i in range(15):
        constructor = TemporalGraphConstructor(time_window_hours=24)
        txns = create_sample_transactions()
        is_fraud = i % 5 >= 3
        constructor.add_transactions(txns)
        graph = constructor.construct_pyg_graph()
        graphs.append(graph)
        labels.append(1 if is_fraud else 0)
        
    dataset = SimpleGraphDataset(graphs, labels)
    train_size = 10
    val_size = 5
    
    train_dataset = torch.utils.data.Subset(dataset, range(train_size))
    val_dataset = torch.utils.data.Subset(dataset, range(train_size, train_size + val_size))
    
    train_loader = DataLoader(train_dataset, batch_size=2, shuffle=True, collate_fn=collate_graphs)
    val_loader = DataLoader(val_dataset, batch_size=2, shuffle=False, collate_fn=collate_graphs)
    
    model_types = ['HTGAT', 'GRAPHSAGE', 'TGAT', 'TGN']
    results = {}
    
    for model_type in model_types:
        print(f"\nEvaluating backbone: {model_type}...")
        print("-" * 50)
        
        # Instantiate risk model
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
        
        # TGN specifically needs memory reset
        if model_type == 'TGN':
            model.backbone.reset_parameters()
            
        model.to(device)
        
        # Train configuration
        config = {
            'learning_rate': 0.002,
            'weight_decay': 0.0001,
            'batch_size': 2,
            'num_epochs': 3,  # Keep it short for fast benchmarking
            'early_stopping_patience': 3,
            'optimizer': 'adam',
            'scheduler': 'cosine',
            'loss': {
                'type': 'focal',
                'alpha': 0.25,
                'gamma': 2.0,
            },
        }
        
        trainer = ProductionTrainer(
            model=model,
            config=config,
            device=device,
            output_dir=f'models/benchmark_{model_type}',
        )
        
        # Measure training speed
        start_train = time.time()
        train_summary = trainer.train(train_loader, val_loader)
        train_duration = time.time() - start_train
        avg_epoch_time = train_duration / config['num_epochs']
        
        # Measure inference latency
        model.eval()
        latencies = []
        with torch.no_grad():
            for batch in val_loader:
                batch = batch.to(device)
                
                # Dynamic model checks
                start_inf = time.time()
                _ = model(batch)
                latency = (time.time() - start_inf) * 1000.0 / batch.num_graphs  # Per graph latency in ms
                latencies.append(latency)
                
        avg_inf_latency = np.mean(latencies)
        
        best_f1 = train_summary.get('best_val_f1', 0.0)
        best_metrics = train_summary.get('val_metrics', [])
        best_auc = best_metrics[-1].get('roc_auc', 0.0) if best_metrics else 0.0
        
        results[model_type] = {
            'best_f1': best_f1,
            'best_auc': best_auc,
            'train_time_epoch_s': avg_epoch_time,
            'inference_latency_ms': avg_inf_latency,
        }
        
    # Print comparison table
    print("\n" + "=" * 85)
    print(f"{'GNN BACKBONE COMPARISON SUMMARY':^85}")
    print("=" * 85)
    print(f"{'Backbone Type':<20} | {'Best F1-Score':<15} | {'Best ROC-AUC':<15} | {'Train Time/Epoch':<18} | {'Inference Latency':<18}")
    print("-" * 85)
    for model_type, metrics in results.items():
        print(f"{model_type:<20} | {metrics['best_f1']:<15.4f} | {metrics['best_auc']:<15.4f} | {metrics['train_time_epoch_s']:<15.3f}s | {metrics['inference_latency_ms']:<15.2f}ms")
    print("=" * 85)


if __name__ == "__main__":
    run_benchmark()
