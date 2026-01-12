"""
Database Connection - Capa de Infraestructura
Manejo de la conexión a la base de datos SQLite
"""
from peewee import SqliteDatabase


class DatabaseConnection:
    """Singleton para manejar la conexión a la base de datos"""
    
    _instance = None
    _db = None
    
    def __new__(cls, db_name: str = 'weather_alerts.db'):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._db = SqliteDatabase(db_name)
        return cls._instance
    
    @property
    def db(self) -> SqliteDatabase:
        """Retorna la instancia de la base de datos"""
        return self._db
    
    def initialize_tables(self, models: list):
        """Inicializa las tablas en la base de datos"""
        with self._db:
            self._db.create_tables(models, safe=True)
    
    def close(self):
        """Cierra la conexión a la base de datos"""
        if self._db and not self._db.is_closed():
            self._db.close()


# Instancia global de la conexión
db_connection = DatabaseConnection()
