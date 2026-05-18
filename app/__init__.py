import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# ── 全域 SQLAlchemy 實例（models 會 import 此物件）──
db = SQLAlchemy()


def create_app():
    """Flask Application Factory — 建立並設定 Flask app"""
    app = Flask(__name__, instance_relative_config=True)

    # ── 基本設定 ──────────────────────────────────────
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # ── 確保 instance 資料夾存在 ─────────────────────
    os.makedirs(app.instance_path, exist_ok=True)

    # ── 初始化擴充套件 ────────────────────────────────
    db.init_app(app)

    # ── 建立資料表（首次執行時） ──────────────────────
    with app.app_context():
        from app.models.book import Book  # noqa: F401
        db.create_all()

    # ── 註冊 Blueprint ────────────────────────────────
    from app.routes.main import main_bp
    from app.routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
