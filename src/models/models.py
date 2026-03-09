from decimal import Decimal
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

# Modelos de SQLAlchemy para las tablas 'companies' y 'charges', con sus respectivas relaciones y tipos de datos. Generados a partir del diagrama de bd.

class Company(Base):
    """Modelo para la tabla 'companies'"""
    __tablename__ = "companies"

    # El company_id del dataset funciona como llave primaria
    id: Mapped[str] = mapped_column(String(40), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(130), nullable=False)

    # Relación: Una compañía puede tener múltiples cargos (transacciones)
    charges: Mapped[List["Charge"]] = relationship(
        "Charge", back_populates="company", cascade="all, delete-orphan"
    )

class Charge(Base):
    """Modelo para la tabla 'charges'"""
    __tablename__ = "charges"
    # id de cargo del dataset funciona como llave primaria y es un string
    id: Mapped[str] = mapped_column(String(40), primary_key=True)

    # Llave foránea que conecta con la tabla companies
    company_id: Mapped[str] = mapped_column(
        String(40), ForeignKey("companies.id"), nullable=False
    )
    
    # El monto se almacena como Decimal para evitar problemas de precisión con los números de punto flotante, y se define con una precisión de 16 dígitos y 2 decimales como se especifica en la prueba.
    amount: Mapped[Decimal] = mapped_column(Numeric(16, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    # updated_at corresponde al campo 'paid_at' del dataset original
    # Es Optional (nullable) porque hay registros sin fecha de pago que no han sido pagados o estan pendientes, por lo que pueden tener un valor nulo en este campo.
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Relación inversa: Cada cargo pertenece a una única compañía
    company: Mapped["Company"] = relationship("Company", back_populates="charges")
