from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import jwt

from app.core.config import settings
from app.core.database import get_db
from app.data.models import TelemetryRecord

router = APIRouter()
security = HTTPBearer()

async def verify_investigator_role(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Decrypts the JWT and verifies the user has Investigator privileges."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid or expired authentication token."
        )
        
    role = payload.get("role")
    if role not in ["Investigator", "Admin"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Access Denied: Investigator clearance required to view historical audits."
        )
    return payload

@router.get("/anomalies")
async def get_anomaly_history(
    limit: int = 50, 
    db: AsyncSession = Depends(get_db),
    user_payload: dict = Depends(verify_investigator_role)
):
    """Fetch the most recent anomalous events from the database (Restricted)."""
    query = (
        select(TelemetryRecord)
        .where(TelemetryRecord.active_anomalies > 0)
        .order_by(desc(TelemetryRecord.timestamp))
        .limit(limit)
    )
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    return records