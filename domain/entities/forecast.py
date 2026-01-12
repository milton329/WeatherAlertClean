"""
Entidad Forecast - Capa de Dominio
Representa el pronóstico del clima sin dependencias externas
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Forecast:
    """Entidad que representa un pronóstico del clima"""
    
    location: str
    latitude: float
    longitude: float
    temperature_c: float
    condition: str
    condition_code: int
    is_adverse: bool
    forecast_date: datetime
    humidity: Optional[int] = None
    wind_kph: Optional[float] = None
    
    def requires_alert(self) -> bool:
        """Determina si el pronóstico requiere una alerta"""
        return self.is_adverse
    
    def get_description(self) -> str:
        """Retorna una descripción legible del pronóstico"""
        return (f"{self.condition} con {self.temperature_c}°C en {self.location}. "
                f"Humedad: {self.humidity}%, Viento: {self.wind_kph} km/h")
