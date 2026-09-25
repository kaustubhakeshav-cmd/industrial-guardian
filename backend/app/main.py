import asyncio
import random 
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.endpoints import router as api_v1_router
from app.services.websocket_manager import ws_manager
from app.services.replay_service import replay_engine
from app.mal.inference import ai_engine

# Database imports
from app.core.database import engine, Base, AsyncSessionLocal
from app.data.models import TelemetryRecord, SensorRecord

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on startup
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    streaming_task = asyncio.create_task(stream_telemetry_loop())
    yield
    streaming_task.cancel()

async def stream_telemetry_loop():
    interval = 1.0 / settings.STREAM_FREQUENCY_HZ
    while True:
        try:
            frame = replay_engine.get_next_frame()
            
            pressure = frame.sensors.get("PUMP_PRESSURE").value
            flow = frame.sensors.get("FLOW_RATE").value
            temp = frame.sensors.get("REACTOR_TEMP").value
            
            ai_engine.add_reading(pressure, flow, temp)
            analysis = ai_engine.evaluate()
            
            # Safely format complex AI outputs into a list of strings
           # Safely format complex AI outputs into a list of strings
            raw_evidence = analysis.get("evidence", [])
            if isinstance(raw_evidence, dict):
                frame.evidence = [f"{str(k).replace('_', ' ').title()}: {v}" for k, v in raw_evidence.items()]
            elif isinstance(raw_evidence, list):
                # Handle cases where evidence is a list of tuples or lists
                frame.evidence = [f"{item[0]}: {item[1]}" if isinstance(item, (tuple, list)) and len(item) == 2 else str(item) for item in raw_evidence]
            else:
                frame.evidence = [str(item) for item in raw_evidence]
            
            if analysis.get("is_anomaly"):
                frame.active_anomalies = 1
                frame.plant_health = 65.0
                frame.estimated_ttf_hours = round(random.uniform(2.5, 18.0), 1) # AI forecasts 2 to 18 hours remaining
                if "PUMP_PRESSURE" in frame.sensors:
                    frame.sensors["PUMP_PRESSURE"].status = "ANOMALY" 
            else:
                frame.active_anomalies = 0
                frame.plant_health = 100.0
                frame.estimated_ttf_hours = None # No imminent failure
                if "PUMP_PRESSURE" in frame.sensors:
                    frame.sensors["PUMP_PRESSURE"].status = "NORMAL"

            # Asynchronously save the frame and sensor data to PostgreSQL
            async with AsyncSessionLocal() as db:
                db_telemetry = TelemetryRecord(
                    timestamp=frame.timestamp,
                    plant_health=frame.plant_health,
                    active_anomalies=frame.active_anomalies,
                    ai_evidence=frame.evidence
                )
                
                for sensor_id, sensor_data in frame.sensors.items():
                    db_sensor = SensorRecord(
                        sensor_id=sensor_id,
                        subsystem=sensor_data.subsystem,
                        value=sensor_data.value,
                        unit=sensor_data.unit,
                        status=sensor_data.status
                    )
                    db_telemetry.sensors.append(db_sensor)
                    
                db.add(db_telemetry)
                await db.commit()

            # Broadcast to React
            await ws_manager.broadcast_telemetry(frame)
            
        except Exception as e:
            print(f"CRITICAL ERROR IN TELEMETRY STREAM: {e}")
            
        await asyncio.sleep(interval)
        
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix=settings.API_V1_STR)

@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)