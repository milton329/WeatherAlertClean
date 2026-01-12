"""
Entidad Notification - Capa de Dominio
Representa una notificación sin dependencias externas
"""
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Notification:
    """Entidad que representa una notificación de alerta climática"""
    
    email: str
    latitude: float
    longitude: float
    condition: str
    code: int
    sent_at: datetime
    id: int = None
    
    def to_dict(self) -> dict:
        """Convierte la notificación a un diccionario"""
        return {
            'id': self.id,
            'email': self.email,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'condition': self.condition,
            'code': self.code,
            'sent_at': self.sent_at.strftime('%Y-%m-%d %H:%M:%S')
        }
