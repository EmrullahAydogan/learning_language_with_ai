"""
Health check endpoints for monitoring service status
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.core.deps import get_db
from app.core.config import settings
import redis
from datetime import datetime

router = APIRouter()


@router.get("/health")
def health_check():
    """
    Basic health check endpoint
    Returns 200 if service is running
    """
    return {
        "status": "healthy",
        "service": "language-learning-api",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/ready")
def readiness_check(db: Session = Depends(get_db)):
    """
    Readiness check - verifies all dependencies are available
    Returns 200 if service is ready to accept traffic
    """
    checks = {
        "database": "unknown",
        "redis": "unknown",
        "openai": "unknown"
    }

    all_healthy = True

    # Check database
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
        all_healthy = False

    # Check Redis
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        checks["redis"] = "healthy"
    except Exception as e:
        checks["redis"] = f"unhealthy: {str(e)}"
        all_healthy = False

    # Check OpenAI (just verify key exists, don't make API call)
    if settings.OPENAI_API_KEY and settings.OPENAI_API_KEY != "sk-your-openai-api-key-here":
        checks["openai"] = "configured"
    else:
        checks["openai"] = "not configured"

    if not all_healthy:
        raise HTTPException(status_code=503, detail={
            "status": "not ready",
            "checks": checks,
            "timestamp": datetime.utcnow().isoformat()
        })

    return {
        "status": "ready",
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/live")
def liveness_check():
    """
    Liveness check - verifies service process is alive
    Returns 200 if service process is running
    """
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat()
    }


@router.get("/health/startup")
def startup_check(db: Session = Depends(get_db)):
    """
    Startup check - verifies service has completed initialization
    Returns 200 if service is fully initialized
    """
    try:
        # Check if database has tables
        result = db.execute(text(
            "SELECT COUNT(*) FROM information_schema.tables "
            "WHERE table_schema = 'public' AND table_name = 'users'"
        ))
        user_table_exists = result.scalar() > 0

        if not user_table_exists:
            raise HTTPException(status_code=503, detail={
                "status": "not started",
                "message": "Database tables not initialized. Run migrations first.",
                "timestamp": datetime.utcnow().isoformat()
            })

        return {
            "status": "started",
            "database_initialized": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=503, detail={
            "status": "not started",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        })
