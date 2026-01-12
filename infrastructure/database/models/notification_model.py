"""
Notification Model - Capa de Infraestructura
Modelo de base de datos para notificaciones usando Peewee ORM
"""
from peewee import Model, CharField, FloatField, IntegerField, DateTimeField
from infrastructure.database.connection import db_connection


class NotificationModel(Model):
    """Modelo de base de datos para notificaciones"""
    
    email = CharField()
    latitude = FloatField()
    longitude = FloatField()
    condition = CharField()
    code = IntegerField()
    sent_at = DateTimeField()
    
    class Meta:
        database = db_connection.db
        table_name = 'notifications'
