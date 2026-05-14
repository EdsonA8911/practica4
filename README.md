# Dashboard App (Flask-AppBuilder)

Panel de administración para **categorías**, **productos** y **ventas**, con reportes y subida de imágenes. Backend en **Python / Flask / Flask-AppBuilder** y base de datos **MySQL**.

## Requisitos

- Python 3.11+ (probado con 3.13)
- Docker (opcional, para MySQL)

## Puesta en marcha local

1. **Clonar el repositorio**

2. **Variables de entorno** (recomendado)

   ```bash
   cp .env.example .env
   ```

   Edita `.env` y define al menos `SECRET_KEY` y, si aplica, `SQLALCHEMY_DATABASE_URI`.

3. **MySQL con Docker** (desde la raíz de este repo)

   ```bash
   docker compose up -d
   ```

4. **Entorno virtual e instalación**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **Arrancar la aplicación**

   ```bash
   cd dashboard-app
   python run.py
   ```

   Por defecto escucha en **http://127.0.0.1:8080**.

6. **Usuario administrador** (solo la primera vez)

   ```bash
   cd dashboard-app
   source ../.venv/bin/activate
   export FLASK_APP=run:app
   flask fab create-admin --username admin --firstname Admin --lastname User --email admin@example.com --password tu_clave_segura
   ```

## Estructura principal

| Ruta | Descripción |
|------|-------------|
| `requirements.txt` | Dependencias Python |
| `docker-compose.yml` | MySQL 8 para desarrollo |
| `dashboard-app/` | Código Flask (`run.py`, `config.py`, `app/`) |

## Subir a GitHub

1. Crea un repositorio vacío en GitHub (sin README si ya tienes uno aquí).
2. En la raíz de este proyecto:

   ```bash
   git init
   git add .
   git commit -m "Initial commit: dashboard Flask-AppBuilder"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
   git push -u origin main
   ```

No subas el archivo **`.env`** ni la carpeta **`.venv`**: ya están ignorados en `.gitignore`.

## Licencia

Define la licencia que corresponda a tu organización.
