import os
from pathlib import Path

from flask import Flask

from .extensions import appbuilder, db


def create_app() -> Flask:
    # Raíz del repo (donde están docker-compose.yml y .env)
    _repo_root = Path(__file__).resolve().parents[2]
    try:
        from dotenv import load_dotenv

        load_dotenv(_repo_root / ".env", override=False)
    except ImportError:
        pass

    app = Flask(__name__)
    app.config.from_object("config")

    for _key in ("UPLOAD_FOLDER", "IMG_UPLOAD_FOLDER"):
        _path = app.config.get(_key)
        if _path:
            os.makedirs(_path, exist_ok=True)

    db.init_app(app)
    with app.app_context():
        from .models import Categoria, Producto
        db.create_all()
        appbuilder.init_app(app, db.session)
        from . import views
        
    return app
