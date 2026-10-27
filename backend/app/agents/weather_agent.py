from typing import List, Dict, Any, Optional
from app.providers.weather_provider import weather_provider
from app.schemas.agent_schemas import WeatherForecast

class WeatherIntelligenceAgent:
    """Agent 5: Analyzes meteorological forecasts and identifies weather-related travel risks."""

    async def analyze_weather(
        self,
        lat: float,
        lng: float,
        start_date_str: str,
        duration_days: int
    ) -> tuple[List[WeatherForecast], bool, List[str]]:
        forecasts = await weather_provider.get_forecast(
            lat=lat,
            lng=lng,
            start_date_str=start_date_str,
            duration_days=duration_days
        )

        has_rainy_days = False
        weather_advisories = []

        for wf in forecasts:
            if wf.is_rainy:
                has_rainy_days = True
                weather_advisories.append(
                    f"Day {wf.day_number} ({wf.date}): {wf.condition} ({wf.precipitation_chance}% rain chance). "
                    f"Outdoor activities should be substituted with indoor venues like museums or cultural centers."
                )

        return forecasts, has_rainy_days, weather_advisories

weather_agent = WeatherIntelligenceAgent()
