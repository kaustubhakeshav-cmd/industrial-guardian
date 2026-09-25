import torch
import torch.nn as nn

class TemporalTransformer(nn.Module):
    def __init__(self, num_features=3, d_model=16, nhead=4, num_layers=2, dropout=0.1):
        super(TemporalTransformer, self).__init__()
        
        # Project raw features into higher dimensional space
        self.input_projection = nn.Linear(num_features, d_model)
        
        # Positional encoding to give the model a sense of time
        self.positional_encoding = nn.Parameter(torch.randn(1, 60, d_model))
        
        # Transformer Encoder
        encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, 
            nhead=nhead, 
            dropout=dropout,
            batch_first=True
        )
        self.transformer = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        
        # Project back to original feature space
        self.output_projection = nn.Linear(d_model, num_features)

    def forward(self, x):
        # x shape: [batch_size, sequence_length, num_features]
        seq_len = x.size(1)
        
        # Add positional encoding
        x = self.input_projection(x) + self.positional_encoding[:, :seq_len, :]
        
        # Pass through Transformer
        x = self.transformer(x)
        
        # Reconstruct the sequence
        x = self.output_projection(x)
        return x