"""
TGAT (Temporal Graph Attention Network) Implementation

Implements the TGAT layers with:
- Temporal attention mechanism combining node features and sinusoidal edge time-encodings
- Multi-head self-attention
- Support for heterogeneous graphs
- Graceful pure PyTorch fallback if torch_geometric is not available
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, List, Dict, Tuple
import math

from .temporal_encoding import TemporalEncoding

# Check for torch_geometric availability
try:
    from torch_geometric.nn import MessagePassing
    from torch_geometric.utils import softmax
    TORCH_GEOMETRIC_AVAILABLE = True
except ImportError:
    class MessagePassing(nn.Module):
        def __init__(self, **kwargs):
            super().__init__()

        def propagate(self, edge_index, x, **kwargs):
            src, dst = edge_index
            x_src, x_dst = x
            
            msg_args = {}
            for k, v in kwargs.items():
                msg_args[k] = v
                
            if 'x_i' not in msg_args:
                msg_args['x_i'] = x_dst[dst]
            if 'x_j' not in msg_args:
                msg_args['x_j'] = x_src[src]
            if 'index' not in msg_args:
                msg_args['index'] = dst
            if 'size_i' not in msg_args:
                msg_args['size_i'] = x_dst.size(0)
                
            messages = self.message(**msg_args)
            out = torch.zeros_like(x_dst)
            out.index_add_(0, dst, messages)
            return out
            
        def message(self, **kwargs):
            # Default fallback simply returns the source node representation
            return kwargs.get('x_j')

    def softmax(src, index, num_nodes=None):
        if num_nodes is None:
            num_nodes = int(index.max().item()) + 1 if index.numel() > 0 else 1

        src_max = torch.full(
            (num_nodes, src.size(-1)), float('-inf'),
            dtype=src.dtype, device=src.device,
        )
        idx = index.unsqueeze(-1).expand_as(src)
        src_max.scatter_reduce_(0, idx, src, reduce='amax', include_self=True)
        src_max = src_max.clamp(min=0)
        out = (src - src_max[index]).exp()

        out_sum = torch.zeros_like(src_max)
        out_sum.scatter_add_(0, idx, out)
        return out / (out_sum[index] + 1e-16)

    TORCH_GEOMETRIC_AVAILABLE = False


class TGATConv(MessagePassing):
    """
    Temporal Graph Attention Network (TGAT) Convolution Layer
    
    Computes temporal attention:
    - Node representation query: h_i
    - Neighbor keys/values: h_j + TemporalEncoding(t_i - t_j)
    """
    def __init__(
        self,
        in_channels: int,
        out_channels: int,
        num_node_types: int,
        num_edge_types: int,
        heads: int = 4,
        dropout: float = 0.3,
        temporal_dim: int = 16,
    ):
        super().__init__(aggr='add', node_dim=0)
        
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.num_node_types = num_node_types
        self.num_edge_types = num_edge_types
        self.heads = heads
        self.dropout = dropout
        self.temporal_dim = temporal_dim
        
        # Projection to common embedding space for different node types
        self.node_projections = nn.ModuleList([
            nn.Linear(in_channels, heads * out_channels, bias=False)
            for _ in range(num_node_types)
        ])
        
        # Temporal encoder for relative time differences
        self.temporal_encoder = TemporalEncoding(encoding_dim=temporal_dim)
        
        # Attention projection matrices
        # Projection for keys and values includes temporal feature dimension
        self.lin_query = nn.Linear(heads * out_channels, heads * out_channels, bias=False)
        self.lin_key = nn.Linear(heads * out_channels + temporal_dim, heads * out_channels, bias=False)
        self.lin_value = nn.Linear(heads * out_channels + temporal_dim, heads * out_channels, bias=False)
        
        # Attention coefficient scaling factor
        self.scale = 1.0 / math.sqrt(out_channels)
        
        # Output project & Bias
        self.lin_out = nn.Linear(heads * out_channels, heads * out_channels)
        
        self.reset_parameters()
        
    def reset_parameters(self):
        gain = nn.init.calculate_gain('relu')
        for proj in self.node_projections:
            nn.init.xavier_uniform_(proj.weight, gain=gain)
            
        nn.init.xavier_uniform_(self.lin_query.weight, gain=gain)
        nn.init.xavier_uniform_(self.lin_key.weight, gain=gain)
        nn.init.xavier_uniform_(self.lin_value.weight, gain=gain)
        nn.init.xavier_uniform_(self.lin_out.weight, gain=gain)
        nn.init.zeros_(self.lin_out.bias)
        
    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.LongTensor,
        node_type: torch.LongTensor,
        edge_type: Optional[torch.LongTensor] = None,
        edge_attr: Optional[torch.Tensor] = None,
        edge_timestamp: Optional[torch.Tensor] = None,
        return_attention_weights: bool = False,
    ) -> torch.Tensor | Tuple[torch.Tensor, Tuple[torch.Tensor, torch.Tensor]]:
        """
        Args:
            x: Node features [num_nodes, in_channels]
            edge_index: Edge index [2, num_edges]
            node_type: Node type index [num_nodes]
            edge_type: Edge type index [num_edges]
            edge_attr: Edge attribute (optional) [num_edges, edge_dim]
            edge_timestamp: Edge timestamp [num_edges]
        """
        # 1. Type-specific node projections
        x_proj = self._apply_node_projections(x, node_type)
        
        # If timestamp is not provided, mock time difference as 0
        if edge_timestamp is None:
            edge_timestamp = torch.zeros(edge_index.size(1), device=x.device)
            
        # 2. Compute Q, K, V
        # Q is computed per destination node
        q = self.lin_query(x_proj)
        
        # 3. Message propagation
        # Pass x_proj (source & destination) and edge_timestamp
        out = self.propagate(
            edge_index,
            x=(x_proj, x_proj),
            edge_timestamp=edge_timestamp,
            q=q,
        )
        
        # 4. Final output projection
        out = self.lin_out(out)
        
        attention_weights = getattr(self, '_last_attention_weights', None)
        if return_attention_weights:
            return out, (edge_index, attention_weights)
            
        return out
        
    def message(
        self,
        x_i: torch.Tensor,  # Target node [num_edges, heads * out_channels]
        x_j: torch.Tensor,  # Source node [num_edges, heads * out_channels]
        edge_timestamp: torch.Tensor,
        q: torch.Tensor,  # Target queries [num_nodes, heads * out_channels]
        index: torch.LongTensor,  # Target indices per edge
        size_i: Optional[int],
    ) -> torch.Tensor:
        H, C = self.heads, self.out_channels
        num_edges = x_j.size(0)
        
        # Relative time encoding (we model time delta between source and target, or absolute timestamp)
        # Here we encode the edge timestamp directly
        t_enc = self.temporal_encoder(edge_timestamp)  # [num_edges, temporal_dim]
        
        # Concatenate source features with time encoding
        k_input = torch.cat([x_j, t_enc], dim=-1)  # [num_edges, heads * out_channels + temporal_dim]
        v_input = torch.cat([x_j, t_enc], dim=-1)
        
        # Project keys and values
        k = self.lin_key(k_input).view(num_edges, H, C)  # [num_edges, H, C]
        v = self.lin_value(v_input).view(num_edges, H, C)  # [num_edges, H, C]
        
        # Extract queries for destination nodes of edges
        # q_i shape: [num_edges, H, C]
        q_i = q[index].view(num_edges, H, C)
        
        # Compute attention coefficients
        # dot product of q_i and k: [num_edges, H]
        alpha = (q_i * k).sum(dim=-1) * self.scale
        
        # Softmax normalize over all incoming edges of target node
        alpha = softmax(alpha, index, num_nodes=size_i)
        
        # Save attention weights for explainability
        self._last_attention_weights = alpha.detach()
        
        # Apply dropout to attention
        alpha = F.dropout(alpha, p=self.dropout, training=self.training)
        
        # Weighted value aggregation: [num_edges, H, C]
        msg = v * alpha.unsqueeze(-1)
        
        return msg.view(num_edges, H * C)
        
    def _apply_node_projections(self, x: torch.Tensor, node_type: torch.LongTensor) -> torch.Tensor:
        num_nodes = x.size(0)
        out = torch.zeros(num_nodes, self.heads * self.out_channels, device=x.device, dtype=x.dtype)
        for ntype in range(self.num_node_types):
            mask = node_type == ntype
            if not mask.any():
                continue
            out[mask] = self.node_projections[ntype](x[mask])
        return out


class TGAT(nn.Module):
    """
    Multi-layer Temporal Graph Attention Network
    """
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        num_node_types: int,
        num_edge_types: int,
        num_layers: int = 2,
        heads: int = 4,
        dropout: float = 0.3,
        temporal_dim: int = 16,
    ):
        super().__init__()
        
        self.num_layers = num_layers
        self.dropout = dropout
        
        self.convs = nn.ModuleList()
        self.norms = nn.ModuleList()
        
        # First layer
        self.convs.append(
            TGATConv(
                in_channels=in_channels,
                out_channels=hidden_channels,
                num_node_types=num_node_types,
                num_edge_types=num_edge_types,
                heads=heads,
                dropout=dropout,
                temporal_dim=temporal_dim,
            )
        )
        self.norms.append(nn.LayerNorm(heads * hidden_channels))
        
        # Hidden layers
        for _ in range(num_layers - 2):
            self.convs.append(
                TGATConv(
                    in_channels=heads * hidden_channels,
                    out_channels=hidden_channels,
                    num_node_types=num_node_types,
                    num_edge_types=num_edge_types,
                    heads=heads,
                    dropout=dropout,
                    temporal_dim=temporal_dim,
                )
            )
            self.norms.append(nn.LayerNorm(heads * hidden_channels))
            
        # Last layer: aggregate output heads by averaging
        if num_layers > 1:
            self.convs.append(
                TGATConv(
                    in_channels=heads * hidden_channels,
                    out_channels=out_channels,
                    num_node_types=num_node_types,
                    num_edge_types=num_edge_types,
                    heads=1,  # Final layer projects to single head output
                    dropout=dropout,
                    temporal_dim=temporal_dim,
                )
            )
            
    def forward(
        self,
        x: torch.Tensor,
        edge_index: torch.LongTensor,
        node_type: torch.LongTensor,
        edge_type: Optional[torch.LongTensor] = None,
        edge_attr: Optional[torch.Tensor] = None,
        edge_timestamp: Optional[torch.Tensor] = None,
    ) -> torch.Tensor:
        """
        Forward pass of TGAT
        """
        for i in range(self.num_layers):
            x = self.convs[i](
                x=x,
                edge_index=edge_index,
                node_type=node_type,
                edge_type=edge_type,
                edge_attr=edge_attr,
                edge_timestamp=edge_timestamp,
            )
            
            if i < self.num_layers - 1:
                x = self.norms[i](x)
                x = F.relu(x)
                x = F.dropout(x, p=self.dropout, training=self.training)
                
        return x
