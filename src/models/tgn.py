"""
TGN (Temporal Graph Network) Implementation

Implements:
- Persistent Node Memory module (TGNMemory)
- GRU-based memory updater (GRUMemoryUpdater)
- Message generator and aggregator
- Memory-based GNN architecture
- Support for pure PyTorch execution
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional, List, Dict, Tuple

from .temporal_encoding import TemporalEncoding
from .graphsage import GraphSAGEConv


class TGNMemory(nn.Module):
    """
    Persistent node memory for TGN.
    
    Keeps state vector and last updated timestamp for each node.
    """
    def __init__(self, num_nodes: int, memory_dim: int):
        super().__init__()
        self.num_nodes = num_nodes
        self.memory_dim = memory_dim
        
        # Persistent state memory buffer (not parameter since we update it via GRU)
        self.register_buffer(
            'memory',
            torch.zeros(num_nodes, memory_dim, dtype=torch.float32)
        )
        
        # Last updated timestamps
        self.register_buffer(
            'last_update',
            torch.zeros(num_nodes, dtype=torch.float32)
        )
        
    def reset_memory(self):
        """Reset all memory states to zeros"""
        self.memory.fill_(0)
        self.last_update.fill_(0)
        
    def get_memory(self, node_indices: torch.Tensor) -> torch.Tensor:
        """Retrieve memory states for nodes, resizing buffer if node index is out of bounds"""
        # Dynamic memory resizing for batch inference with unseen nodes
        max_idx = int(node_indices.max().item()) if node_indices.numel() > 0 else -1
        if max_idx >= self.num_nodes:
            self._resize(max_idx + 100) # add margin
            
        return self.memory[node_indices]
        
    def set_memory(self, node_indices: torch.Tensor, values: torch.Tensor):
        """Set memory states for nodes"""
        max_idx = int(node_indices.max().item()) if node_indices.numel() > 0 else -1
        if max_idx >= self.num_nodes:
            self._resize(max_idx + 100)
            
        self.memory[node_indices] = values
        
    def update_timestamp(self, node_indices: torch.Tensor, timestamps: torch.Tensor):
        """Update last updated timestamps for nodes"""
        max_idx = int(node_indices.max().item()) if node_indices.numel() > 0 else -1
        if max_idx >= self.num_nodes:
            self._resize(max_idx + 100)
            
        self.last_update[node_indices] = timestamps
        
    def _resize(self, new_num_nodes: int):
        """Dynamically expand memory buffers"""
        device = self.memory.device
        
        # Expand memory buffer
        new_memory = torch.zeros(new_num_nodes, self.memory_dim, dtype=torch.float32, device=device)
        new_memory[:self.num_nodes] = self.memory
        self.memory = new_memory
        
        # Expand timestamp buffer
        new_last_update = torch.zeros(new_num_nodes, dtype=torch.float32, device=device)
        new_last_update[:self.num_nodes] = self.last_update
        self.last_update = new_last_update
        
        self.num_nodes = new_num_nodes


class GRUMemoryUpdater(nn.Module):
    """
    GRU cell for updating node memory using messages.
    """
    def __init__(self, message_dim: int, memory_dim: int):
        super().__init__()
        self.gru = nn.GRUCell(input_size=message_dim, hidden_size=memory_dim)
        
    def forward(self, messages: torch.Tensor, memory: torch.Tensor) -> torch.Tensor:
        """
        Args:
            messages: Aggregated node messages [num_updated_nodes, message_dim]
            memory: Node memories before update [num_updated_nodes, memory_dim]
        """
        return self.gru(messages, memory)


class TGN(nn.Module):
    """
    Temporal Graph Network (TGN)
    
    Contains memory tracking, GRU updater, and a GraphSAGE Conv projection layer.
    """
    def __init__(
        self,
        in_channels: int,
        hidden_channels: int,
        out_channels: int,
        num_node_types: int,
        num_edge_types: int,
        num_nodes: int = 20000,
        memory_dim: int = 64,
        temporal_dim: int = 16,
        dropout: float = 0.3,
    ):
        super().__init__()
        
        self.in_channels = in_channels
        self.hidden_channels = hidden_channels
        self.out_channels = out_channels
        self.memory_dim = memory_dim
        self.temporal_dim = temporal_dim
        self.dropout = dropout
        
        # Node memory components
        self.memory_module = TGNMemory(num_nodes, memory_dim)
        
        # Message creation: message = [src_memory || dst_memory || delta_t || edge_attr]
        # In our case, edge_attr dimension = temporal_dim (time embedding)
        # Message dimension = memory_dim * 2 + temporal_dim
        self.message_dim = memory_dim * 2 + temporal_dim
        self.memory_updater = GRUMemoryUpdater(self.message_dim, memory_dim)
        
        # Temporal encoder
        self.temporal_encoder = TemporalEncoding(encoding_dim=temporal_dim)
        
        # GNN layer (GraphSAGEConv) to aggregate memories of neighbors
        # Input to GNN is Projected Memory (memory_dim) or (in_channels + memory_dim)
        # We project raw node feature (in_channels) + memory (memory_dim) to hidden_channels
        self.input_projection = nn.Linear(in_channels + memory_dim, hidden_channels)
        
        self.gnn = GraphSAGEConv(
            in_channels=hidden_channels,
            out_channels=out_channels,
            num_node_types=num_node_types,
            num_edge_types=num_edge_types,
            aggregator_type='mean',
            dropout=dropout,
        )
        
        self.reset_parameters()
        
    def reset_parameters(self):
        self.memory_module.reset_memory()
        nn.init.xavier_uniform_(self.input_projection.weight)
        nn.init.zeros_(self.input_projection.bias)
        self.gnn.reset_parameters()
        
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
        Args:
            x: Node features [num_nodes, in_channels]
            edge_index: Graph topology [2, num_edges]
            node_type: Node types [num_nodes]
            edge_type: Edge relation types [num_edges]
            edge_attr: Edge features (optional)
            edge_timestamp: Edge timestamps [num_edges]
        """
        num_nodes = x.size(0)
        device = x.device
        
        # Rescale model indices if needed
        indices = torch.arange(num_nodes, device=device)
        memories = self.memory_module.get_memory(indices)
        
        # If timestamp is provided, execute Memory Update Step based on edge events
        if edge_timestamp is not None and edge_index.size(1) > 0:
            src, dst = edge_index
            
            # Construct messages for each interaction edge
            t_enc = self.temporal_encoder(edge_timestamp)  # [num_edges, temporal_dim]
            
            # Message for source: [s_src || s_dst || delta_t || edge_t_enc]
            msg_src = torch.cat([memories[src], memories[dst], t_enc], dim=-1)
            # Message for destination: [s_dst || s_src || delta_t || edge_t_enc]
            msg_dst = torch.cat([memories[dst], memories[src], t_enc], dim=-1)
            
            # Aggregate messages per node (using index_add to sum messages)
            aggregated_msgs = torch.zeros(num_nodes, self.message_dim, device=device)
            aggregated_counts = torch.zeros(num_nodes, 1, device=device)
            
            aggregated_msgs.index_add_(0, src, msg_src)
            aggregated_counts.index_add_(0, src, torch.ones_like(src, dtype=torch.float32).unsqueeze(-1))
            
            aggregated_msgs.index_add_(0, dst, msg_dst)
            aggregated_counts.index_add_(0, dst, torch.ones_like(dst, dtype=torch.float32).unsqueeze(-1))
            
            # Mean aggregation
            mask = (aggregated_counts > 0).squeeze(-1)
            aggregated_msgs[mask] = aggregated_msgs[mask] / aggregated_counts[mask]
            
            # Update memories for active nodes
            active_nodes = torch.nonzero(mask).squeeze(-1)
            if active_nodes.numel() > 0:
                updated_mem = self.memory_updater(
                    aggregated_msgs[active_nodes],
                    memories[active_nodes]
                )
                self.memory_module.set_memory(active_nodes, updated_mem)
                self.memory_module.update_timestamp(active_nodes, edge_timestamp[0].expand_as(active_nodes))
                
                # Fetch updated memories
                memories = self.memory_module.get_memory(indices)
                
        # Combine node features and updated memory
        combined = torch.cat([x, memories], dim=-1)
        h_node = F.relu(self.input_projection(combined))
        
        # Spatial aggregate via GraphSAGEConv
        out = self.gnn(
            x=h_node,
            edge_index=edge_index,
            node_type=node_type,
            edge_type=edge_type,
            edge_attr=edge_attr,
        )
        
        return out
