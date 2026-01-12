"""
Weather Request DTO - Capa de Aplicación
Data Transfer Object para solicitudes de clima
"""
from dataclasses import dataclass


@dataclass
class WeatherRequestDTO:
    """DTO para solicitudes de verificación de clima"""
    
    latitude: float
    longitude: float
    email: str
    
    def validate(self) -> tuple[bool, str]:
        """Valida los datos del DTO"""
        if not self.email or '@' not in self.email:
            return False, "Email inválido"
        
        if not isinstance(self.latitude, (int, float)) or not isinstance(self.longitude, (int, float)):
            return False, "Latitud y longitud deben ser números"
        
        if not (-90 <= self.latitude <= 90):
            return False, "Latitud debe estar entre -90 y 90"
        
        if not (-180 <= self.longitude <= 180):
            return False, "Longitud debe estar entre -180 y 180"
        
        return True, ""
