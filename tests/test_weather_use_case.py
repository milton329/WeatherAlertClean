"""
Tests para CheckWeatherUseCase
"""
import pytest
from datetime import datetime
from unittest.mock import Mock, MagicMock
from application.use_cases.check_weather_use_case import CheckWeatherUseCase
from application.dto.weather_request_dto import WeatherRequestDTO
from domain.entities.forecast import Forecast
from domain.entities.notification import Notification


class TestCheckWeatherUseCase:
    """Tests para el caso de uso de verificación de clima"""
    
    @pytest.fixture
    def mock_notification_repository(self):
        """Mock del repositorio de notificaciones"""
        return Mock()
    
    @pytest.fixture
    def mock_weather_service(self):
        """Mock del servicio de clima"""
        return Mock()
    
    @pytest.fixture
    def mock_email_service(self):
        """Mock del servicio de email"""
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_notification_repository, mock_weather_service, mock_email_service):
        """Instancia del caso de uso con mocks inyectados"""
        return CheckWeatherUseCase(
            notification_repository=mock_notification_repository,
            weather_service=mock_weather_service,
            email_service=mock_email_service
        )
    
    def test_execute_with_normal_weather(self, use_case, mock_weather_service):
        """Test: clima normal, no debe enviar alerta"""
        # Arrange
        request = WeatherRequestDTO(
            latitude=5.07,
            longitude=-75.52,
            email="test@example.com"
        )
        
        forecast = Forecast(
            location="Armenia, Colombia",
            latitude=5.07,
            longitude=-75.52,
            temperature_c=25.0,
            condition="Sunny",
            condition_code=1000,
            is_adverse=False,
            forecast_date=datetime.now(),
            humidity=60,
            wind_kph=10.0
        )
        
        mock_weather_service.get_forecast.return_value = forecast
        
        # Act
        result = use_case.execute(request)
        
        # Assert
        assert result['alert_sent'] is False
        assert result['adverse_weather'] is False
        assert 'No se requiere alerta' in result['message']
    
    def test_execute_with_adverse_weather(
        self,
        use_case,
        mock_weather_service,
        mock_email_service,
        mock_notification_repository
    ):
        """Test: clima adverso, debe enviar alerta"""
        # Arrange
        request = WeatherRequestDTO(
            latitude=5.07,
            longitude=-75.52,
            email="test@example.com"
        )
        
        forecast = Forecast(
            location="Armenia, Colombia",
            latitude=5.07,
            longitude=-75.52,
            temperature_c=20.0,
            condition="Heavy Rain",
            condition_code=1195,
            is_adverse=True,
            forecast_date=datetime.now(),
            humidity=90,
            wind_kph=30.0
        )
        
        mock_weather_service.get_forecast.return_value = forecast
        
        # Act
        result = use_case.execute(request)
        
        # Assert
        assert result['alert_sent'] is True
        assert result['adverse_weather'] is True
        mock_email_service.send_email.assert_called_once()
        mock_notification_repository.save.assert_called_once()
    
    def test_execute_with_invalid_email(self, use_case):
        """Test: email inválido debe lanzar ValueError"""
        # Arrange
        request = WeatherRequestDTO(
            latitude=5.07,
            longitude=-75.52,
            email="invalid-email"
        )
        
        # Act & Assert
        with pytest.raises(ValueError):
            use_case.execute(request)
    
    def test_execute_with_invalid_coordinates(self, use_case):
        """Test: coordenadas inválidas deben lanzar ValueError"""
        # Arrange
        request = WeatherRequestDTO(
            latitude=91.0,  # Latitud fuera de rango
            longitude=-75.52,
            email="test@example.com"
        )
        
        # Act & Assert
        with pytest.raises(ValueError):
            use_case.execute(request)
