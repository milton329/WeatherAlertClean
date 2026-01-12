"""
Notification DTO - Capa de Aplicación
Data Transfer Object para respuestas de notificaciones
"""
from dataclasses import dataclass
from typing import List


@dataclass
class NotificationDTO:
    """DTO para representar una notificación en las respuestas"""
    
    sent_at: str
    latitude: float
    longitude: float
    condition: str
    code: int


@dataclass
class NotificationListDTO:
    """DTO para lista de notificaciones"""
    
    notifications: List[NotificationDTO]
    
    def to_dict(self) -> dict:
        """Convierte el DTO a un diccionario"""
        return {
            'notifications': [
                {
                    'sent_at': n.sent_at,
                    'latitude': n.latitude,
                    'longitude': n.longitude,
                    'condition': n.condition,
                    'code': n.code
                }
                for n in self.notifications
            ]
        }
