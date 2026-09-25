from fastapi import APIRouter, Depends, HTTPException, status
from app.data.schemas import LoginRequest, TokenResponse, UserAuth
from app.core.security import create_access_token, get_password_hash, verify_password

# Import the new history router we just created
from app.api.v1.history import router as history_router

router = APIRouter()

# Mock authorized user store for initial development
USERS_DB = {
    "operator": {
        "password_hash": get_password_hash("operator123"),
        "role": "Operator"
    },
    "engineer": {
        "password_hash": get_password_hash("engineer123"),
        "role": "Investigator"
    }
}

@router.post("/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest):
    user_record = USERS_DB.get(credentials.username)
    if not user_record or not verify_password(credentials.password, user_record["password_hash"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(
        data={"sub": credentials.username, "role": user_record["role"]}
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserAuth(username=credentials.username, role=user_record["role"])
    )

@router.get("/health")
async def health_check():
    return {"status": "ONLINE", "system": "Industrial Guardian", "version": "0.1.0"}

# Attach the history endpoints to the main API router
router.include_router(history_router, prefix="/history", tags=["Historical Audit"])