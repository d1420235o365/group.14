"""
app/routes/admin.py — 管理者路由（佔位符）

本檔案供後續管理者功能使用，目前僅定義 Blueprint。
完整 CRUD 功能將在【管理者端功能實作】階段實作。
"""
from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from app.models.book import Book
from app import db

admin_bp = Blueprint('admin', __name__)

ADMIN_PASSWORD = 'admin1234'  # 簡單密碼保護，正式環境應使用更安全的方式


def login_required(f):
    """簡單的 session 登入驗證 decorator"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('請先登入管理後台', 'warning')
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """管理者登入"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('登入成功！', 'success')
            return redirect(url_for('admin.dashboard'))
        flash('密碼錯誤，請重試。', 'danger')
    return render_template('admin/login.html')


@admin_bp.route('/logout')
def logout():
    """管理者登出"""
    session.pop('admin_logged_in', None)
    flash('已登出管理後台', 'info')
    return redirect(url_for('main.index'))


@admin_bp.route('/')
@login_required
def dashboard():
    """管理後台首頁"""
    books = Book.get_all()
    total      = len(books)
    available  = sum(1 for b in books if b.status == '在庫')
    borrowed   = sum(1 for b in books if b.status == '已借出')
    restocking = sum(1 for b in books if b.status == '補貨中')
    return render_template(
        'admin/dashboard.html',
        books=books,
        total=total,
        available=available,
        borrowed=borrowed,
        restocking=restocking
    )


@admin_bp.route('/books/create', methods=['GET', 'POST'])
@login_required
def create_book():
    """新增書籍"""
    if request.method == 'POST':
        title    = request.form.get('title', '').strip()
        author   = request.form.get('author', '').strip()
        isbn     = request.form.get('isbn', '').strip() or None
        category = request.form.get('category', '').strip() or None
        desc     = request.form.get('description', '').strip() or None
        status   = request.form.get('status', '在庫')
        try:
            quantity = int(request.form.get('quantity', 1))
        except ValueError:
            quantity = 1

        if not title or not author:
            flash('書名與作者為必填欄位。', 'danger')
            return render_template('admin/create.html')

        try:
            Book.create(title=title, author=author, isbn=isbn,
                        category=category, description=desc,
                        status=status, quantity=quantity)
            flash(f'《{title}》已成功新增！', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            flash(f'新增失敗：{e}', 'danger')

    return render_template('admin/create.html')


@admin_bp.route('/books/edit/<int:book_id>', methods=['GET', 'POST'])
@login_required
def edit_book(book_id):
    """編輯書籍"""
    book = Book.query.get_or_404(book_id)
    if request.method == 'POST':
        kwargs = {
            'title':       request.form.get('title', '').strip(),
            'author':      request.form.get('author', '').strip(),
            'isbn':        request.form.get('isbn', '').strip() or None,
            'category':    request.form.get('category', '').strip() or None,
            'description': request.form.get('description', '').strip() or None,
            'status':      request.form.get('status', '在庫'),
        }
        try:
            kwargs['quantity'] = int(request.form.get('quantity', 1))
        except ValueError:
            kwargs['quantity'] = 1

        if not kwargs['title'] or not kwargs['author']:
            flash('書名與作者為必填欄位。', 'danger')
            return render_template('admin/edit.html', book=book)

        try:
            book.update(**kwargs)
            flash(f'《{book.title}》已成功更新！', 'success')
            return redirect(url_for('admin.dashboard'))
        except Exception as e:
            flash(f'更新失敗：{e}', 'danger')

    return render_template('admin/edit.html', book=book)


@admin_bp.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book(book_id):
    """刪除書籍"""
    book = Book.query.get_or_404(book_id)
    title = book.title
    try:
        book.delete()
        flash(f'《{title}》已成功刪除。', 'success')
    except Exception as e:
        flash(f'刪除失敗：{e}', 'danger')
    return redirect(url_for('admin.dashboard'))
