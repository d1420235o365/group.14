"""
app.py — 應用程式入口點
執行方式：
    flask run          （開發模式）
    python app.py      （直接執行）
"""
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
