import torch
import torch.nn as nn

class RiskPredictionNet(nn.Module):
    """Deep neural network estimating system or financial risk score in range [0, 1]."""
    
    def __init__(self, input_dim: int = 5):
        super(RiskPredictionNet, self).__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
            nn.Linear(8, 1),
            nn.Sigmoid()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)

def load_pretrained_model(input_dim: int = 5) -> RiskPredictionNet:
    """Instantiates and returns evaluation-ready neural network."""
    model = RiskPredictionNet(input_dim=input_dim)
    model.eval()  # Set to inference mode
    return model