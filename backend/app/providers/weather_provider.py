from datetime import datetime, date, timedelta
from typing import List, Dict, Any, Optional
import httpx
from app.schemas.agent_schemas import WeatherForecast

WMO_CODE_MAP = {
    0: ("Clear sky", False),
    1: ("Mainly clear", False),
    2: ("Partly cloudy", False),
    3: ("Overcast", False),
    45: ("Fog", False),
    48: ("Depositing rime fog", False),
    51: ("Light drizzle", True),
    53: ("Moderate drizzle", True),
    55: ("Dense drizzle", True),
    61: ("Slight rain", True),
    63: ("Moderate rain", True),
    65: ("Heavy rain", True),
    71: ("Slight snow", True),
    73: ("Moderate snow", True),
    75: ("Heavy snow", True),
    80: ("Slight rain showers", True),
    81: ("Moderate rain showers", True),
    82: ("Violent rain showers", True),
    95: ("Thunderstorm", True),
    96: ("Thunderstorm with hail", True)
}

class WeatherProvider:
    """Weather provider querying Open-Meteo or climatological fallback."""

    async def get_forecast(self, lat: float, lng: float, start_date_str: str, duration_days: int) -> List[WeatherForecast]:
        """Fetch multi-day weather forecast for destination."""
        forecasts: List[WeatherForecast] = []
        is_live = False
        source_label = "Open-Meteo Weather API"

        try:
            async with httpx.AsyncClient(timeout=4.0) as client:
                url = "https://api.open-meteo.com/v1/forecast"
                params = {
                    "latitude": lat,
                    "longitude": lng,
                    "daily": "weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max",
                    "timezone": "auto"
                }
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json().get("daily", {})
                    time_list = data.get("time", [])
                    weathercodes = data.get("weathercode", [])
                    max_temps = data.get("temperature_2m_max", [])
                    min_temps = data.get("temperature_2m_min", [])
                    precip_probs = data.get("precipitation_probability_max", [])

                    if time_list:
                        is_live = True
                        for i in range(min(duration_days, len(time_list))):
                            day_num = i + 1
                            day_date = time_list[i] if i < len(time_list) else start_date_str
                            wcode = weathercodes[i] if i < len(weathercodes) else 1
                            cond_text, is_wet = WMO_CODE_MAP.get(wcode, ("Partly Cloudy", False))
                            t_max = float(max_temps[i]) if i < len(max_temps) else 28.0
                            t_min = float(min_temps[i]) if i < len(min_temps) else 20.0
                            p_prob = int(precip_probs[i]) if i < len(precip_probs) and precip_probs[i] is not None else (40 if is_wet else 10)
                            is_rainy = is_wet or p_prob >= 50

                            risk = "High risk of precipitation affecting open-air walks." if is_rainy else "Optimal conditions for outdoor activities and excursions."
                            alts = ["Local museum or art gallery visit", "Indoor heritage cooking masterclass", "Traditional indoor cultural performance"] if is_rainy else []

                            forecasts.append(WeatherForecast(
                                date=day_date,
                                day_number=day_num,
                                condition=cond_text,
                                temp_high_c=round(t_max, 1),
                                temp_low_c=round(t_min, 1),
                                precipitation_chance=p_prob,
                                is_rainy=is_rainy,
                                is_outdoor_suitable=not is_rainy,
                                risk_assessment=risk,
                                suggested_alternatives=alts,
                                affected_activities=[],
                                data_source=source_label,
                                freshness="Live Open-Meteo Satellite & Numerical Model Forecast"
                            ))
        except Exception:
            is_live = False

        if not is_live or len(forecasts) < duration_days:
            # Climatological fallback / demo simulation with realistic variance
            source_label = "TRIPORA Climatological Model (Demo Mode)"
            try:
                base_dt = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            except Exception:
                base_dt = date.today() + timedelta(days=7)

            forecasts = []
            conditions_cycle = [
                ("Sunny & Pleasant", 29.0, 21.0, 10, False),
                ("Partly Cloudy", 28.0, 20.5, 20, False),
                ("Scattered Rain Showers", 25.0, 19.0, 65, True),  # Day 3 rain test case for replanning!
                ("Clear & Mild", 27.5, 19.5, 15, False),
                ("Mainly Sunny", 30.0, 22.0, 10, False),
                ("Overcast Breeze", 26.0, 18.0, 30, False),
                ("Golden Sunshine", 31.0, 23.0, 5, False)
            ]

            for i in range(duration_days):
                day_num = i + 1
                curr_dt = base_dt + timedelta(days=i)
                cond, t_high, t_low, p_prob, is_rain = conditions_cycle[i % len(conditions_cycle)]
                
                risk = "Rain showers predicted; outdoor touring may experience interruptions." if is_rain else "Favorable weather for sightseeing, coastal walks, and walking tours."
                alts = ["National museum tour", "Covered shopping arcade", "Indoor palace museum & cultural show"] if is_rain else []

                forecasts.append(WeatherForecast(
                    date=curr_dt.strftime("%Y-%m-%d"),
                    day_number=day_num,
                    condition=cond,
                    temp_high_c=t_high,
                    temp_low_c=t_low,
                    precipitation_chance=p_prob,
                    is_rainy=is_rain,
                    is_outdoor_suitable=not is_rain,
                    risk_assessment=risk,
                    suggested_alternatives=alts,
                    affected_activities=[],
                    data_source=source_label,
                    freshness="Climatological Benchmark Estimates (Dates beyond live forecast or offline)"
                ))

        return forecasts

weather_provider = WeatherProvider()
