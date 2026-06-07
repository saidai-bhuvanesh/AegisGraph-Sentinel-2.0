import torch
import torch.nn as nn

class TemporalAnomalyDetector(nn.Module):
    """Simple temporal anomaly detection layer.

    Given a sequence of node embeddings over time, this module computes a
    running mean and variance and flags embeddings that deviate beyond a
    configurable threshold (default 3 standard deviations).
    """
    def __init__(self, threshold: float = 3.0):
        super().__init__()
        self.threshold = threshold
        # Running statistics (initialized on first forward)
        self.register_buffer("running_mean", torch.tensor(0.0))
        self.register_buffer("running_var", torch.tensor(0.0))
        self.register_buffer("count", torch.tensor(0))

    def forward(self, embeddings: torch.Tensor) -> torch.BoolTensor:
        """Return a mask indicating anomalous nodes.

        Parameters
        ----------
        embeddings: torch.Tensor
            Shape ``[num_nodes, hidden_dim]``
        """
        if self.count == 0:
            # Initialise statistics with the first batch
            self.running_mean = embeddings.mean(dim=0)
            self.running_var = embeddings.var(dim=0, unbiased=False)
            self.count = torch.tensor(1)
            return torch.zeros(embeddings.size(0), dtype=torch.bool, device=embeddings.device)

        # Update running stats (Welford's online algorithm)
        new_count = self.count + 1
        delta = embeddings.mean(dim=0) - self.running_mean
        self.running_mean = self.running_mean + delta / new_count
        delta2 = embeddings.mean(dim=0) - self.running_mean
        self.running_var = ((self.count - 1) * self.running_var + delta * delta2) / self.count
        self.count = new_count

        # Compute z‑score per node
        std = torch.sqrt(self.running_var + 1e-6)
        z = (embeddings - self.running_mean) / std
        # Anomaly if any dimension exceeds threshold
        mask = (z.abs() > self.threshold).any(dim=1)
        return mask
