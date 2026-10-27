from fastapi import APIRouter
from app.core.config import settings

router = APIRouter(prefix="/health", tags=["Health & System"])

@router.get("/")
def get_health():
    """System health check and provider readiness report."""
    return {
        "status": "healthy",
        "service": settings.PROJECT_NAME,
        "version": "1.0.0",
        "llm_provider": settings.LLM_PROVIDER,
        "demo_mode": settings.DEMO_MODE,
        "default_currency": settings.DEFAULT_CURRENCY,
        "multi_agent_framework": "LangGraph 1.2+",
        "providers": {
            "weather": "Open-Meteo Real-Time Meteorological API",
            "geocoding": "OpenStreetMap Nominatim + Curated POIs",
            "transport": "TRIPORA Distance & Transit Estimator",
            "hotel": "TRIPORA Verified Accommodation Catalog"
        }
    }
