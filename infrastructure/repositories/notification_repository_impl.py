"""
Notification Repository Implementation - Capa de Infraestructura
Implementación concreta del repositorio de notificaciones
"""
from typing import List
from domain.repositories.notification_repository import NotificationRepository
from domain.entities.notification import Notification
from infrastructure.database.models.notification_model import NotificationModel


class NotificationRepositoryImpl(NotificationRepository):
    """Implementación del repositorio de notificaciones usando Peewee"""
    
    def save(self, notification: Notification) -> Notification:
        """Guarda una notificación en la base de datos"""
        model = NotificationModel.create(
            email=notification.email,
            latitude=notification.latitude,
            longitude=notification.longitude,
            condition=notification.condition,
            code=notification.code,
            sent_at=notification.sent_at
        )
        
        notification.id = model.id
        return notification
    
    def find_by_email(self, email: str) -> List[Notification]:
        """Encuentra todas las notificaciones para un email"""
        models = NotificationModel.select().where(
            NotificationModel.email == email
        ).order_by(NotificationModel.sent_at.desc())
        
        return [self._to_entity(model) for model in models]
    
    def find_all(self) -> List[Notification]:
        """Obtiene todas las notificaciones"""
        models = NotificationModel.select().order_by(
            NotificationModel.sent_at.desc()
        )
        
        return [self._to_entity(model) for model in models]
    
    def _to_entity(self, model: NotificationModel) -> Notification:
        """Convierte un modelo de base de datos a una entidad"""
        return Notification(
            id=model.id,
            email=model.email,
            latitude=model.latitude,
            longitude=model.longitude,
            condition=model.condition,
            code=model.code,
            sent_at=model.sent_at
        )
