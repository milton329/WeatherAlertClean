"""
Interfaz NotificationRepository - Capa de Dominio
Define el contrato para el repositorio de notificaciones
"""
from abc import ABC, abstractmethod
from typing import List
from domain.entities.notification import Notification


class NotificationRepository(ABC):
    """Interfaz que define las operaciones del repositorio de notificaciones"""
    
    @abstractmethod
    def save(self, notification: Notification) -> Notification:
        """Guarda una notificación en el repositorio"""
        pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> List[Notification]:
        """Encuentra todas las notificaciones para un email específico"""
        pass
    
    @abstractmethod
    def find_all(self) -> List[Notification]:
        """Obtiene todas las notificaciones"""
        pass
