from urllib.parse import quote

from flask import current_app
from flask_appbuilder import BaseView, ModelView, expose
from flask_appbuilder.filemanager import thumbgen_filename
from flask_appbuilder.models.sqla.interface import SQLAInterface
from markupsafe import Markup

from .extensions import appbuilder, db
from .models import Categoria, Producto, Venta


def _fmt_imagen(val):
    """Muestra miniatura en listado/detalle; enlace abre imagen completa."""
    if not val:
        return ""
    filename = (val if isinstance(val, str) else str(val)).strip()
    if not filename:
        return ""
    base = (current_app.config.get("IMG_UPLOAD_URL") or "/static/uploads/").rstrip("/") + "/"
    full = f"{base}{quote(filename, safe='')}"
    thumb = f"{base}{quote(thumbgen_filename(filename), safe='')}"
    return Markup(
        '<a href="{full}" target="_blank" rel="noopener noreferrer">'
        '<img src="{thumb}" alt="" class="img-thumbnail" '
        'style="max-height:80px;max-width:160px;object-fit:contain;" loading="lazy"/>'
        "</a>"
    ).format(full=full, thumb=thumb)


def _fmt_fecha(val):
    """Muestra fechas en calendario local (naive UTC guardada en BD)."""
    if val is None:
        return ""
    if hasattr(val, "strftime"):
        return val.strftime("%d/%m/%Y %H:%M")
    return str(val)


class CategoriaModelView(ModelView):
    datamodel = SQLAInterface(Categoria)
    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripcion",
        "url_imagen": "Imagen",
        "estado": "Estado",
        "creado_en": "Creado en",
        "actualizado_en": "Actualizado en",
    }
    list_columns = ["nombre", "descripcion", "url_imagen", "estado", "creado_en", "actualizado_en"]
    add_columns = ["nombre", "descripcion", "url_imagen", "estado"]
    edit_columns = ["nombre", "descripcion", "url_imagen", "estado"]
    show_columns = ["nombre", "descripcion", "url_imagen", "estado", "creado_en", "actualizado_en"]
    formatters_columns = {
        "url_imagen": _fmt_imagen,
        "creado_en": _fmt_fecha,
        "actualizado_en": _fmt_fecha,
    }


class ProductoModelView(ModelView):
    datamodel = SQLAInterface(Producto)
    label_columns = {
        "nombre": "Nombre",
        "descripcion": "Descripcion",
        "precio": "Precio",
        "categoria": "Categoría",
        "url_imagen": "Imagen",
        "estado": "Estado",
        "creado_en": "Creado en",
        "actualizado_en": "Actualizado en",
    }
    list_columns = ["nombre", "precio", "categoria", "url_imagen", "estado", "creado_en", "actualizado_en"]
    add_columns = ["nombre", "descripcion", "precio", "categoria", "url_imagen", "estado"]
    edit_columns = ["nombre", "descripcion", "precio", "categoria", "url_imagen", "estado"]
    show_columns = ["nombre", "descripcion", "precio", "url_imagen", "estado", "creado_en", "actualizado_en"]
    formatters_columns = {
        "url_imagen": _fmt_imagen,
        "creado_en": _fmt_fecha,
        "actualizado_en": _fmt_fecha,
    }


class VentaModelView(ModelView):
    datamodel = SQLAInterface(Venta)
    list_columns = ["producto", "cantidad", "precio_unitario", "total", "fecha"]
    add_columns = ["producto", "cantidad", "precio_unitario", "total"]
    edit_columns = ["producto", "cantidad", "precio_unitario", "total"]
    formatters_columns = {"fecha": _fmt_fecha}


# REPORTES
class ReporteView(BaseView):
    route_base = "/reportes"

    @expose("/")
    def index(self):
        total_ventas = db.session.query(Venta).count()
        total_ingresos = db.session.query(db.func.sum(Venta.total)).scalar() or 0
        venta_por_producto = (
            db.session.query(Venta.producto, db.func.sum(Venta.cantidad))
            .group_by(Venta.producto)
            .all()
        )
        return self.render_template(
            "reportes.html",
            t_ventas=total_ventas,
            t_ingresos=total_ingresos,
            venta_por_producto=venta_por_producto,
        )


appbuilder.add_view(
    CategoriaModelView,
    "Categorias",
    icon="fa-info",
    category="Configuraciones",
    category_icon="fa-info",
)

appbuilder.add_view(
    ProductoModelView,
    "Productos",
    icon="fa-info",
    category="Configuraciones",
    category_icon="fa-info",
)

appbuilder.add_view(
    VentaModelView,
    "Ventas",
    icon="fa-cart-arrow-down",
    category="Ventas",
    category_icon="fa-shopping-cart",
)

appbuilder.add_view_no_menu(ReporteView())

appbuilder.add_link(
    "Reporte1",
    href="/reportes/",
    icon="fa-file-text",
    category="Reportes",
)
