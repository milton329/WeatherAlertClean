"""
Weather API Service - Capa de Infraestructura
Servicio para interactuar con la API externa de clima
"""
import requests
from datetime import datetime
from domain.entities.forecast import Forecast


class WeatherAPIException(Exception):
    """Excepción personalizada para errores de la API del clima"""
    pass


class WeatherAPIService:
    """Servicio para consultar la API de WeatherAPI.com"""
    
    # Códigos de condiciones adversas según WeatherAPI
    ADVERSE_CODES = [
        1063, 1066, 1069, 1072, 1087, 1114, 1117,  # Lluvia, nieve, hielo
        1135, 1147,  # Niebla
        1150, 1153, 1168, 1171, 1180, 1183, 1186, 1189, 1192, 1195,  # Llovizna y lluvia
        1198, 1201, 1204, 1207, 1210, 1213, 1216, 1219, 1222, 1225,  # Lluvia helada y nieve
        1237, 1240, 1243, 1246, 1249, 1252, 1255, 1258, 1261, 1264,  # Granizo y nieve
        1273, 1276, 1279, 1282  # Tormentas
    ]
    
    def __init__(self, api_key: str, api_url: str, days: int = 2):
        self.api_key = api_key
        self.api_url = api_url
        self.days = days
    
    def get_forecast(self, latitude: float, longitude: float) -> Forecast:
        """
        Obtiene el pronóstico del clima para una ubicación
        
        Args:
            latitude: Latitud de la ubicación
            longitude: Longitud de la ubicación
            
        Returns:
            Forecast: Entidad con el pronóstico del clima
            
        Raises:
            WeatherAPIException: Si hay un error al consultar la API
        """
        try:
            params = {
                'key': self.api_key,
                'q': f'{latitude},{longitude}',
                'days': self.days,
                'aqi': 'no',
                'alerts': 'no'
            }
            
            response = requests.get(self.api_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            return self._parse_forecast(data, latitude, longitude)
            
        except requests.exceptions.RequestException as e:
            raise WeatherAPIException(f"Error al consultar la API del clima: {str(e)}")
        except (KeyError, ValueError) as e:
            raise WeatherAPIException(f"Error al procesar la respuesta de la API: {str(e)}")
    
    def _parse_forecast(self, data: dict, latitude: float, longitude: float) -> Forecast:
        """Parsea la respuesta de la API a una entidad Forecast"""
        current = data['current']
        location = data['location']
        
        condition_code = current['condition']['code']
        is_adverse = condition_code in self.ADVERSE_CODES
        
        return Forecast(
            location=f"{location['name']}, {location['country']}",
            latitude=latitude,
            longitude=longitude,
            temperature_c=current['temp_c'],
            condition=current['condition']['text'],
            condition_code=condition_code,
            is_adverse=is_adverse,
            forecast_date=datetime.now(),
            humidity=current['humidity'],
            wind_kph=current['wind_kph']
        )
