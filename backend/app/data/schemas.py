from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Literal
from datetime import datetime

class SensorReading(BaseModel):
    sensor_id: str
    subsystem: str = Field(..., description="e.g., Boiler, Turbine, Pump B, Heat Exchanger")
    value: float
    unit: str
    status: Literal["NORMAL", "WARNING", "ANOMALY"] = "NORMAL"

class SensorContribution(BaseModel):
    sensor_id: str
    subsystem: str
    contribution: float = Field(..., ge=0.0, le=1.0)
    current_value: float
    baseline_value: float
    unit: str

class AnomalyEvidence(BaseModel):
    anomaly_score: float = Field(..., ge=0.0, le=1.0)
    threshold: float
    status: Literal["NOMINAL", "WARNING", "CRITICAL"]
    model_version: str = "ttf-ss-v1.0.0"
    model_type: str = "Self-Supervised Temporal Transformer"
    timestamp: datetime
    affected_sensors: List[SensorContribution]
    alarm_triggered: bool = False
    alarm_acknowledged: bool = False

class TelemetryFrame(BaseModel):
    timestamp: datetime
    plant_health: float = Field(..., ge=0.0, le=100.0)
    active_anomalies: int
    open_incidents: int
    sensors: Dict[str, SensorReading]
    evidence: Optional[List[str]] = None
    estimated_ttf_hours: Optional[float] = None
    
class UserAuth(BaseModel):
    username: str
    role: Literal["Operator", "Investigator", "Admin"]

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: UserAuth