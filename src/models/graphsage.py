"""
GraphSAGE (Graph Sample and Aggregate) Implementation

Implements the GraphSAGE convolution layer and multi-layer GraphSAGE model with:
- Heterogeneous node and edge types
- Multiple neighborhood aggregators: mean, pooling, and LSTM
- Layer Normalization and Dropout
- Graceful pure PyTorch fallback if torch_geometric is not available
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, List, Dict

# Check for torch_geometric availability
try:
    from torch_geometric.nn import MessagePassing
    TORCH_GEOMETRIC_AVAILABLE = True
except ImportError:
    class MessagePassing(nn.Module):
        def __init__(self, **kwargs):
            super().__init__()

        def propagate(self, edge_index, x, edge_type=None, edge_attr=None):
            src, dst = edge_index
            x_src, x_dst = x
            
            # Simple aggregation fallback
            messages = self.message(x_j=x_src[src], edge_type=edge_type)
            
            # Aggregate via index_add_ (equivalent to aggr='add')
            out = torch.zeros_like(x_dst)
            out.index_add_(0, dst, messages)
            return out
            
        def message(self, x_j, edge_type=None):
            return x_j

    TORCH_GEOMETRIC_AVAILABLE = False


class GraphSAGEConv(MessagePassing):
    """
    GraphSAGE Convolution Layer for Heterogeneous Graphs
    
    Aggregates neighbor features and combines them with self features.
    Supports: mean, pooling, and LSTM aggregators.
    """
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        num_node_types: int,
        num_edge_types: int,
        aggregator_type: str = 'mean',
        dropout: float = 0.0,
        negative_slope: float = 0.2,
    ):
        # Determine aggregate operation
        aggr = 'add' if aggregator_type in ['pooling', 'lstm'] else 'mean'
        super().__init__(aggr=aggr, node_dim=0)
        
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_node_types = num_node_types
        self.num_edge_types = num_edge_types
        self.aggregator_type = aggregator_type.lower()
        self.dropout = dropout
        self.negative_slope = negative_slope
        
        if self.aggregator_type not in ['mean', 'pooling', 'lstm']:
            raise ValueError(f"Unknown aggregator type: {self.aggregator_type}")
            
        # Type-specific projections to project different node types into a common space
        self.node_projections = nn.ModuleList([
            nn.Linear(in_channels, out_channels, bias=False)
            for _ in range(num_node_types)
        ])
        
        # Self and neighbor linear transformations
        self.lin_self = nn.Linear(out_channels, out_channels, bias=False)
        self.lin_neigh = nn.Linear(out_channels, out_channels, bias=False)
        
        # Aggregator-specific parameters
        if self.aggregator_type == 'pooling':
            self.lin_pool = nn.Linear(out_channels, out_channels)
        elif self.aggregator_type == 'lstm':
            self.lstm = nn.LSTM(out_channels, out_channels, batch_first=True)
            
        self.bias = nn.Parameter(torch.zeros(out_channels))
        self.reset_parameters()
        
    def reset_parameters(self):
        gain = nn.init.calculate_gain('relu')
        for proj in self.node_projections:
            nn.init.xavier_uniform_(proj.weight, gain=gain)
        nn.init.xavier_uniform_(self.lin_self.weight, gain=gain)
        nn.init.xavier_uniform_(self.lin_neigh.weight, gain=gain)
        
        if self.aggregator_type == 'pooling':
            nn.init.xavier_uniform_(self.lin_pool.weight, gain=gain)
            nn.init.zeros_(self.lin_pool.bias)
        elif self.aggregator_type == 'lstm':
            self.lstm.reset_parameters()
            
        nn.init.zeros_(self.bias)
        
    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.LongTensor,
        node_type: torch.LongTensor,
        edge_type: Optional[torch.LongTensor] = None,
        edge_attr: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Args:
            x: Node features [num_nodes, in_channels]
            edge_index: Graph topology [2, num_edges]
            node_type: Node types [num_nodes]
            edge_type: Edge relation types (optional) [num_edges]
            edge_attr: Edge features (optional, unused in SAGE but kept for API match)
        """
        # 1. Project all nodes to common dim based on node_type
        x_proj = self._apply_node_projections(x, node_type)
        
        # 2. Propagate messages from source to target
        # For SAGE, target nodes aggregate messages from source neighbors
        h_neigh = self.propagate(edge_index, x=(x_proj, x_proj), edge_type=edge_type)
        
        # 3. Post-processing for pooling and LSTM aggregators
        if self.aggregator_type == 'pooling':
            # Mean neighbor degree normalization for the pool sum, or let max pooling handle it
            pass
        elif self.aggregator_type == 'lstm':
            h_neigh = self._lstm_aggregate(h_neigh, edge_index, x_proj)
            
        # 4. Combine self-features with aggregated neighbor-features
        out = self.lin_self(x_proj) + self.lin_neigh(h_neigh)
        out = out + self.bias
        
        return F.dropout(F.relu(out), p=self.dropout, training=self.training)
        
    def message(self, x_j: torch.Tensor, edge_type: Optional[torch.LongTensor] = None) -> torch.Tensor:
        if self.aggregator_type == 'pooling':
            # For pooling, neighbor representations are transformed first
            return F.relu(self.lin_pool(x_j))
        return x_j
        
    def aggregate(self, inputs: torch.Tensor, index: torch.Tensor, ptr: Optional[torch.Tensor] = None, dim_size: Optional[int] = None) -> torch.Tensor:
        if self.aggregator_type == 'mean':
            # Custom scatter mean
            return super().aggregate(inputs, index, ptr=ptr, dim_size=dim_size)
        elif self.aggregator_type == 'pooling':
            # Max pooling: we use scatter_reduce for max if available, otherwise fallback
            num_nodes = dim_size or int(index.max().item() + 1) if index.numel() > 0 else 0
            if num_nodes == 0:
                return inputs
            out = torch.full((num_nodes, inputs.size(-1)), float('-inf'), dtype=inputs.dtype, device=inputs.device)
            idx = index.unsqueeze(-1).expand_as(inputs)
            out.scatter_reduce_(0, idx, inputs, reduce='amax', include_self=False)
            # Replace -inf with zero for nodes with no neighbors
            out = torch.where(out == float('-inf'), torch.zeros_like(out), out)
            return out
        else:
            # For LSTM we do custom processing in forward pass after propagate (or here)
            # Return inputs as-is (they will be grouped in _lstm_aggregate)
            return inputs
            
    def _apply_node_projections(self, x: torch.Tensor, node_type: torch.LongTensor) -> torch.Tensor:
        num_nodes = x.size(0)
        out = torch.zeros(num_nodes, self.out_channels, device=x.device, dtype=x.dtype)
        if node_type is None:
            node_type = torch.zeros(num_nodes, dtype=torch.long, device=x.device)
        for ntype in range(self.num_node_types):
            mask = node_type == ntype
            if not mask.any():
                continue
            out[mask] = self.node_projections[ntype](x[mask])
        return out
        
    def _lstm_aggregate(self, h_raw_messages: torch.Tensor, edge_index: torch.LongTensor, x_proj: torch.Tensor) -> torch.Tensor:
        """
        Custom LSTM aggregation for node neighbors
        """
        src, dst = edge_index
        num_nodes = x_proj.size(0)
        device = x_proj.device
        
        # Group source features by destination node
        # For simplicity and vectorization, we sort edge indices by destination node
        sorted_dst, perm = torch.sort(dst)
        sorted_src = src[perm]
        
        # Count number of neighbors per destination node
        unique_dst, counts = torch.unique_consecutive(sorted_dst, return_counts=True)
        
        # Max sequence length (number of neighbors)
        if counts.numel() > 0:
            max_len = int(counts.max().item())
        else:
            max_len = 0
            
        h_neigh = torch.zeros(num_nodes, self.out_channels, device=device)
        
        if max_len == 0:
            return h_neigh
            
        # Build padded sequences for LSTM: [num_unique_dst, max_len, out_channels]
        batch_size = unique_dst.size(0)
        lstm_input = torch.zeros(batch_size, max_len, self.out_channels, device=device)
        
        # Fill sequences
        start_idx = 0
        for i, count in enumerate(counts.tolist()):
            end_idx = start_idx + count
            src_indices = sorted_src[start_idx:end_idx]
            lstm_input[i, :count] = x_proj[src_indices]
            start_idx = end_idx
            
        # Run through LSTM
        # We sort or pack if sequence lengths are highly variable, or just run with padding
        # Let's run LSTM and take final hidden state of each sequence
        lstm_out, (hn, cn) = self.lstm(lstm_input)
        
        # Extract the hidden state at the actual length of each sequence
        # hn is [1, batch_size, out_channels]
        h_neigh[unique_dst] = hn.squeeze(0)
        
        return h_neigh


class GraphSAGE(nn.Module):
    """
    Multi-layer GraphSAGE architecture
    """
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        num_node_types: int,
        num_edge_types: int,
        num_layers: int = 2,
        aggregator_type: str = 'mean',
        dropout: float = 0.3,
    ):
        super().__init__()
        
        self.num_layers = num_layers
        self.dropout = dropout
        
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        
        # First layer
        self.convs.append(
            GraphSAGEConv(
                in_channels=in_channels,
                out_channels=hidden_channels,
                num_node_types=num_node_types,
                num_edge_types=num_edge_types,
                aggregator_type=aggregator_type,
                dropout=dropout,
            )
        )
        self.norms.append(nn.LayerNorm(hidden_channels))
        
        # Hidden layers
        for _ in range(num_layers - 2):
            self.convs.append(
                GraphSAGEConv(
                    in_channels=hidden_channels,
                    out_channels=hidden_channels,
                    num_node_types=num_node_types,
                    num_edge_types=num_edge_types,
                    aggregator_type=aggregator_type,
                    dropout=dropout,
                )
            )
            self.norms.append(nn.LayerNorm(hidden_channels))
            
        # Final prediction embedding layer
        if num_layers > 1:
            self.convs.append(
                GraphSAGEConv(
                    in_channels=hidden_channels,
                    out_channels=out_channels,
                    num_node_types=num_node_types,
                    num_edge_types=num_edge_types,
                    aggregator_type=aggregator_type,
                    dropout=0.0,
                )
            )
            
    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.LongTensor,
        node_type: torch.LongTensor,
        edge_type: Optional[torch.LongTensor] = None,
        edge_attr: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Forward pass of Multi-layer GraphSAGE
        """
        for i in range(self.num_layers):
            x = self.convs[i](x, edge_index, node_type, edge_type, edge_attr)
            
            if i < self.num_layers - 1:
                x = self.norms[i](x)
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
                
        return x
