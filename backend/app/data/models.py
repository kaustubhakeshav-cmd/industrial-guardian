from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.core.database import Base

class TelemetryRecord(Base):
    __tablename__ = "telemetry_records"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), index=True)
    plant_health = Column(Float, nullable=False)
    active_anomalies = Column(Integer, default=0)
    
    # Store the AI evidence directly as a JSON array for easy retrieval
    ai_evidence = Column(JSON, default=list)

    # Relationship to individual sensor readings
    sensors = relationship("SensorRecord", back_populates="telemetry_frame", cascade="all, delete-orphan")

class SensorRecord(Base):
    __tablename__ = "sensor_records"

    id = Column(Integer, primary_key=True, index=True)
    telemetry_id = Column(Integer, ForeignKey("telemetry_records.id"), index=True)
    
    sensor_id = Column(String, index=True)
    subsystem = Column(String)
    value = Column(Float)
    unit = Column(String)
    status = Column(String)

    telemetry_frame = relationship("TelemetryRecord", back_populates="sensors")