from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.security import get_password_hash
from app.data.models import TelemetryRecord, SensorRecord, Operator

router = APIRouter()

class OperatorCreate(BaseModel):
    username: str
    password: str

@router.get("/telemetry/recent")
async def get_recent_telemetry(limit: int = 50, db: AsyncSession = Depends(get_db)):
    """Fetches the most recent telemetry frames and associated sensors for the live dashboard."""
    query = (
        select(TelemetryRecord)
        .options(selectinload(TelemetryRecord.sensors))
        .order_by(TelemetryRecord.timestamp.desc())
        .limit(limit)
    )
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    if not records:
        return []
        
    return records

@router.post("/telemetry/ingest", status_code=201)
async def ingest_telemetry(payload: dict, db: AsyncSession = Depends(get_db)):
    """Ingests a new frame of simulated or live sensor data from industrial machines."""
    try:
        new_record = TelemetryRecord(
            plant_health=payload.get("plant_health", 100.0),
            active_anomalies=payload.get("active_anomalies", 0),
            ai_evidence=payload.get("ai_evidence", [])
        )
        db.add(new_record)
        await db.flush() 

        sensors_data = payload.get("sensors", [])
        for s_data in sensors_data:
            new_sensor = SensorRecord(
                telemetry_id=new_record.id,
                sensor_id=s_data.get("sensor_id"),
                subsystem=s_data.get("subsystem"),
                value=s_data.get("value"),
                unit=s_data.get("unit"),
                status=s_data.get("status", "OK")
            )
            db.add(new_sensor)

        await db.commit()
        return {"status": "success", "record_id": new_record.id}
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/operator/register", status_code=201)
async def register_operator(payload: OperatorCreate, db: AsyncSession = Depends(get_db)):
    """Creates a new operator account for the dashboard."""
    new_operator = Operator(
        username=payload.username,
        password_hash=get_password_hash(payload.password)
    )
    db.add(new_operator)
    await db.commit()
    return {"status": "success", "username": new_operator.username}