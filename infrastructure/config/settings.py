"""
Settings - Capa de Infraestructura
Configuración centralizada de la aplicación
"""
import os
from dataclasses import dataclass


@dataclass
class Settings:
    """Configuración de la aplicación"""
    
    # Seguridad
    API_KEY: str
    
    # Weather API
    WEATHER_API_KEY: str
    WEATHER_API_URL: str
    WEATHER_DAYS: int
    
    # Email
    MAIL_SERVER: str
    MAIL_PORT: int
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_USE_TLS: bool
    
    # Database
    DATABASE_NAME: str
    
    @classmethod
    def from_env(cls) -> 'Settings':
        """Carga la configuración desde las variables de entorno"""
        return cls(
            API_KEY=os.getenv('API_KEY', ''),
            WEATHER_API_KEY=os.getenv('WEATHER_API_KEY', ''),
            WEATHER_API_URL=os.getenv('WEATHER_API_URL', 'https://api.weatherapi.com/v1/forecast.json'),
            WEATHER_DAYS=int(os.getenv('WEATHER_DAYS', 2)),
            MAIL_SERVER=os.getenv('MAIL_SERVER', ''),
            MAIL_PORT=int(os.getenv('MAIL_PORT', 587)),
            MAIL_USERNAME=os.getenv('MAIL_USERNAME', ''),
            MAIL_PASSWORD=os.getenv('MAIL_PASSWORD', ''),
            MAIL_USE_TLS=os.getenv('MAIL_USE_TLS', 'True').lower() == 'true',
            DATABASE_NAME=os.getenv('DATABASE_NAME', 'weather_alerts.db')
        )
