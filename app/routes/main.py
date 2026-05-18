"""
app/routes/main.py — 一般使用者路由

路由清單：
  GET  /              → 首頁（搜尋入口）
  GET  /books         → 書籍搜尋結果列表（F-01）
  GET  /books/<id>    → 書籍詳細資訊（F-02）
"""
from flask import Blueprint, render_template, request
from app.models.book import Book

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """首頁 — 顯示搜尋列與精選書籍"""
    # 首頁也顯示最新 6 本書作為預覽
    latest_books = Book.query.order_by(Book.created_at.desc()).limit(6).all()
    return render_template('index.html', latest_books=latest_books)


@main_bp.route('/books')
def book_list():
    """書籍搜尋結果頁 — 支援關鍵字、分類、狀態多條件搜尋（F-01）

    Query Parameters:
        q        — 關鍵字（模糊比對書名 / 作者）
        category — 分類篩選
        status   — 庫存狀態篩選
    """
    q        = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    status   = request.args.get('status', '').strip()

    query = Book.query

    # ── 關鍵字模糊搜尋（書名 OR 作者）────────────────
    if q:
        from app import db
        pattern = f'%{q}%'
        query = query.filter(
            db.or_(
                Book.title.ilike(pattern),
                Book.author.ilike(pattern),
                Book.isbn.ilike(pattern)
            )
        )

    # ── 分類篩選 ──────────────────────────────────────
    if category:
        query = query.filter(Book.category == category)

    # ── 狀態篩選 ──────────────────────────────────────
    if status:
        query = query.filter(Book.status == status)

    books = query.order_by(Book.created_at.desc()).all()

    # 取得所有分類（供下拉選單使用）
    from app import db as _db
    categories = [
        row[0] for row in
        _db.session.query(Book.category).distinct().filter(Book.category.isnot(None)).all()
    ]

    return render_template(
        'books/list.html',
        books=books,
        q=q,
        category=category,
        status=status,
        categories=categories,
        total=len(books)
    )


@main_bp.route('/books/<int:book_id>')
def book_detail(book_id):
    """書籍詳細資訊頁（F-02）"""
    book = Book.query.get_or_404(book_id)
    return render_template('books/detail.html', book=book)
