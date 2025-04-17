from fastapi import APIRouter

router = APIRouter()

@router.get("")
def health_check():
    """
    Health check endpoint to verify API is running.
    """
    return {"status": "ok", "message": "API is operational"}
