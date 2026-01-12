"""
Tests para GetNotificationsUseCase
"""
import pytest
from datetime import datetime
from unittest.mock import Mock
from application.use_cases.get_notifications_use_case import GetNotificationsUseCase
from domain.entities.notification import Notification


class TestGetNotificationsUseCase:
    """Tests para el caso de uso de obtención de notificaciones"""
    
    @pytest.fixture
    def mock_notification_repository(self):
        """Mock del repositorio de notificaciones"""
        return Mock()
    
    @pytest.fixture
    def use_case(self, mock_notification_repository):
        """Instancia del caso de uso con mock inyectado"""
        return GetNotificationsUseCase(
            notification_repository=mock_notification_repository
        )
    
    def test_execute_with_existing_notifications(self, use_case, mock_notification_repository):
        """Test: debe retornar notificaciones existentes"""
        # Arrange
        email = "test@example.com"
        notifications = [
            Notification(
                id=1,
                email=email,
                latitude=5.07,
                longitude=-75.52,
                condition="Heavy Rain",
                code=1195,
                sent_at=datetime(2025, 4, 7, 10, 0, 0)
            ),
            Notification(
                id=2,
                email=email,
                latitude=5.07,
                longitude=-75.52,
                condition="Thunderstorm",
                code=1273,
                sent_at=datetime(2025, 4, 6, 15, 30, 0)
            )
        ]
        
        mock_notification_repository.find_by_email.return_value = notifications
        
        # Act
        result = use_case.execute(email)
        
        # Assert
        assert len(result.notifications) == 2
        assert result.notifications[0].condition == "Heavy Rain"
        assert result.notifications[1].condition == "Thunderstorm"
        mock_notification_repository.find_by_email.assert_called_once_with(email)
    
    def test_execute_with_no_notifications(self, use_case, mock_notification_repository):
        """Test: debe retornar lista vacía si no hay notificaciones"""
        # Arrange
        email = "test@example.com"
        mock_notification_repository.find_by_email.return_value = []
        
        # Act
        result = use_case.execute(email)
        
        # Assert
        assert len(result.notifications) == 0
        mock_notification_repository.find_by_email.assert_called_once_with(email)
    
    def test_execute_with_invalid_email(self, use_case):
        """Test: email inválido debe lanzar ValueError"""
        # Arrange
        email = "invalid-email"
        
        # Act & Assert
        with pytest.raises(ValueError):
            use_case.execute(email)
    
    def test_execute_with_empty_email(self, use_case):
        """Test: email vacío debe lanzar ValueError"""
        # Act & Assert
        with pytest.raises(ValueError):
            use_case.execute("")
    
    def test_to_dict_conversion(self, use_case, mock_notification_repository):
        """Test: conversión correcta a diccionario"""
        # Arrange
        email = "test@example.com"
        notifications = [
            Notification(
                id=1,
                email=email,
                latitude=5.07,
                longitude=-75.52,
                condition="Heavy Rain",
                code=1195,
                sent_at=datetime(2025, 4, 7, 10, 0, 0)
            )
        ]
        
        mock_notification_repository.find_by_email.return_value = notifications
        
        # Act
        result = use_case.execute(email)
        result_dict = result.to_dict()
        
        # Assert
        assert 'notifications' in result_dict
        assert len(result_dict['notifications']) == 1
        assert result_dict['notifications'][0]['sent_at'] == '2025-04-07 10:00:00'
        assert result_dict['notifications'][0]['condition'] == 'Heavy Rain'
        assert result_dict['notifications'][0]['code'] == 1195
