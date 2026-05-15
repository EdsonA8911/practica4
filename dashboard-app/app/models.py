import datetime

from flask_appbuilder import Model
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, ForeignKey, Text, event
from sqlalchemy.orm import relationship


def utc_now() -> datetime.datetime:
    """UTC naive para columnas MySQL DATETIME (evita errores con datetimes con tz)."""
    return datetime.datetime.now(datetime.UTC).replace(tzinfo=None)


class Categoria(Model):
    __tablename__="categoria"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    url_imagen = Column(
        ImageColumn(thumbnail_size=(64, 64, True), size=(800, 800, True)),
        nullable=True,
    )
    estado = Column(Boolean, nullable=True)
    creado_en = Column(DateTime, default=utc_now, nullable=False)
    actualizado_en = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    
    productos = relationship(
        "Producto",
        back_populates="categoria",
    )
    
    def __repr__(self):
        return  self.nombre
    
class Producto(Model):
    __tablename__="producto"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(Numeric(10, 2), nullable=True)
    categoria_id = Column(Integer, ForeignKey("categoria.id"), nullable=False)
    url_imagen = Column(
        ImageColumn(thumbnail_size=(64, 64, True), size=(800, 800, True)),
        nullable=True,
    )
    estado = Column(Boolean, nullable=True)
    creado_en = Column(DateTime, default=utc_now, nullable=False)
    actualizado_en = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)
    categoria = relationship(
        "Categoria",
        back_populates="productos",
    )
    
    def __repr__(self):
        return  self.nombre

class Venta (Model):
    __tablename__="venta"
    id = Column(Integer, primary_key=True)
    producto = Column(String(150), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Numeric(10, 2), nullable=True)
    total = Column(Numeric(10, 2), nullable=True)
    fecha = Column(DateTime, default=utc_now, nullable=False)


@event.listens_for(Categoria, "before_insert")
def _categoria_before_insert(_mapper, _connection, target):
    now = utc_now()
    if target.creado_en is None:
        target.creado_en = now
    if target.actualizado_en is None:
        target.actualizado_en = now


@event.listens_for(Categoria, "before_update")
def _categoria_before_update(_mapper, _connection, target):
    target.actualizado_en = utc_now()


@event.listens_for(Producto, "before_insert")
def _producto_before_insert(_mapper, _connection, target):
    now = utc_now()
    if target.creado_en is None:
        target.creado_en = now
    if target.actualizado_en is None:
        target.actualizado_en = now


@event.listens_for(Producto, "before_update")
def _producto_before_update(_mapper, _connection, target):
    target.actualizado_en = utc_now()