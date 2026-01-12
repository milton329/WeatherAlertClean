"""
Check Weather Use Case - Capa de Aplicación
Caso de uso para verificar el clima y enviar alertas
"""
from datetime import datetime
from domain.repositories.notification_repository import NotificationRepository
from domain.entities.notification import Notification
from domain.entities.forecast import Forecast
from application.dto.weather_request_dto import WeatherRequestDTO


class CheckWeatherUseCase:
    """Caso de uso para verificar el clima y procesar alertas"""
    
    def __init__(
        self,
        notification_repository: NotificationRepository,
        weather_service,
        email_service
    ):
        self.notification_repository = notification_repository
        self.weather_service = weather_service
        self.email_service = email_service
    
    def execute(self, request: WeatherRequestDTO) -> dict:
        """
        Ejecuta el caso de uso de verificación de clima
        
        Args:
            request: DTO con los datos de la solicitud
            
        Returns:
            dict: Resultado de la verificación
        """
        # Validar request
        is_valid, error_msg = request.validate()
        if not is_valid:
            raise ValueError(error_msg)
        
        # Obtener pronóstico del clima
        forecast = self.weather_service.get_forecast(
            request.latitude,
            request.longitude
        )
        
        # Procesar resultado
        result = {
            'forecast': forecast.get_description(),
            'location': forecast.location,
            'adverse_weather': forecast.is_adverse
        }
        
        # Si hay clima adverso, enviar alerta y guardar notificación
        if forecast.requires_alert():
            self._send_alert(forecast, request.email)
            self._save_notification(forecast, request.email)
            result['alert_sent'] = True
            result['message'] = 'Alerta enviada debido a condiciones climáticas adversas'
        else:
            result['alert_sent'] = False
            result['message'] = 'No se requiere alerta'
        
        return result
    
    def _send_alert(self, forecast: Forecast, email: str):
        """Envía una alerta por correo electrónico"""
        subject = f"⚠️ Alerta Climática - {forecast.condition}"
        body = f"""
        Se ha detectado una condición climática adversa en tu ubicación:
        
        📍 Ubicación: {forecast.location}
        🌡️ Temperatura: {forecast.temperature_c}°C
        ☁️ Condición: {forecast.condition}
        💧 Humedad: {forecast.humidity}%
        💨 Viento: {forecast.wind_kph} km/h
        
        Por favor, toma las precauciones necesarias.
        
        Fecha: {forecast.forecast_date.strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        self.email_service.send_email(email, subject, body)
    
    def _save_notification(self, forecast: Forecast, email: str):
        """Guarda la notificación en el repositorio"""
        notification = Notification(
            email=email,
            latitude=forecast.latitude,
            longitude=forecast.longitude,
            condition=forecast.condition,
            code=forecast.condition_code,
            sent_at=datetime.now()
        )
        
        self.notification_repository.save(notification)
