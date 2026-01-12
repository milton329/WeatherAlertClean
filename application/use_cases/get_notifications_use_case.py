"""
Get Notifications Use Case - Capa de Aplicación
Caso de uso para obtener notificaciones por email
"""
from typing import List
from domain.repositories.notification_repository import NotificationRepository
from application.dto.notification_dto import NotificationDTO, NotificationListDTO


class GetNotificationsUseCase:
    """Caso de uso para obtener notificaciones de un usuario"""
    
    def __init__(self, notification_repository: NotificationRepository):
        self.notification_repository = notification_repository
    
    def execute(self, email: str) -> NotificationListDTO:
        """
        Ejecuta el caso de uso de obtención de notificaciones
        
        Args:
            email: Email del usuario
            
        Returns:
            NotificationListDTO: Lista de notificaciones
        """
        if not email or '@' not in email:
            raise ValueError("Email inválido")
        
        # Obtener notificaciones del repositorio
        notifications = self.notification_repository.find_by_email(email)
        
        # Convertir a DTOs
        notification_dtos = [
            NotificationDTO(
                sent_at=n.sent_at.strftime('%Y-%m-%d %H:%M:%S'),
                latitude=n.latitude,
                longitude=n.longitude,
                condition=n.condition,
                code=n.code
            )
            for n in notifications
        ]
        
        return NotificationListDTO(notifications=notification_dtos)
