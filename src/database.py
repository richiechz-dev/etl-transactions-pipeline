from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///data/database.db" # Se utilizo sqlite porque es sencillo de probar y no requiere una instalacion adicional. Pero de igual forma se tiene en cuenta que se puede cambiar a otro motor de base de datos gracias a Sqlalchemy. Unicamente se sabe de igual forma que sqlite tiene limitaciones.

engine = create_engine(DATABASE_URL, echo=False)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass

def init_db():
    """Crea todas las tablas definidas en los modelos."""
    Base.metadata.drop_all(bind=engine) # Borra todas las tablas para evitar conflictos con datos anteriores, especialmente util para correr el proceso varias veces desde el proceso main en modo prueba unicamente, en un entorno de producción se debería eliminar esta línea para evitar la pérdida de datos.
    Base.metadata.create_all(bind=engine)
