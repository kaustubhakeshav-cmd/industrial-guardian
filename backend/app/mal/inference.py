import torch
import numpy as np
from app.mal.model import TemporalTransformer
from app.core.config import settings

class AnomalyDetector:
    def __init__(self):
        # Initialize our PyTorch model
        self.model = TemporalTransformer(num_features=3)
        self.model.eval() # Set to evaluation mode
        
        # In a production environment, we would load pre-trained weights here:
        # self.model.load_state_dict(torch.load('weights.pth'))
        
        self.sequence_length = 30
        self.buffer = []
        
    def add_reading(self, pressure, flow, temp):
        # Normalize the incoming data (rough static scaling for the mock data)
        norm_p = pressure / 100.0
        norm_f = flow / 50.0
        norm_t = temp / 200.0
        
        self.buffer.append([norm_p, norm_f, norm_t])
        
        if len(self.buffer) > self.sequence_length:
            self.buffer.pop(0)

    def evaluate(self) -> dict:
        # We need a full sequence to run the temporal model
        if len(self.buffer) < self.sequence_length:
            return {"is_anomaly": False, "score": 0.0, "evidence": []}

        # Convert buffer to PyTorch tensor: [batch_size=1, seq_len=30, features=3]
        input_tensor = torch.tensor([self.buffer], dtype=torch.float32)
        
        with torch.no_grad():
            reconstruction = self.model(input_tensor)
            
            # Calculate Mean Squared Error (MSE) between input and reconstruction
            mse_loss = torch.mean((input_tensor - reconstruction) ** 2, dim=-1)
            
            # The score for the most recent timestep
            current_score = mse_loss[0, -1].item()

        # Determine if it exceeds our dynamic threshold
        is_anomaly = current_score > settings.DEFAULT_ANOMALY_THRESHOLD
        
        evidence = []
        if is_anomaly:
            evidence.append(f"Transformer reconstruction error ({current_score:.3f}) exceeded baseline.")
            
        return {
            "is_anomaly": is_anomaly,
            "score": current_score,
            "evidence": evidence
        }

# Global singleton instance
ai_engine = AnomalyDetector()