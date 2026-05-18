from datetime import datetime
from app import db  # SQLAlchemy instance from app/__init__.py


class Book(db.Model):
    """書籍資料模型"""
    __tablename__ = 'book'

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title       = db.Column(db.Text, nullable=False)
    author      = db.Column(db.Text, nullable=False)
    isbn        = db.Column(db.Text, nullable=True)
    category    = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    status      = db.Column(db.Text, nullable=False, default='在庫')
    quantity    = db.Column(db.Integer, nullable=False, default=1)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at  = db.Column(db.DateTime, nullable=False, default=datetime.now,
                            onupdate=datetime.now)

    # ──────────────────────────────────────────
    # CRUD 方法
    # ──────────────────────────────────────────

    @classmethod
    def get_all(cls):
        """取得所有書籍"""
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, book_id):
        """依 ID 取得單筆書籍"""
        return cls.query.get_or_404(book_id)

    @classmethod
    def search(cls, keyword):
        """模糊搜尋書名或作者（對應 F-01）"""
        pattern = f'%{keyword}%'
        return cls.query.filter(
            db.or_(
                cls.title.ilike(pattern),
                cls.author.ilike(pattern)
            )
        ).all()

    @classmethod
    def create(cls, title, author, isbn=None, category=None,
               description=None, status='在庫', quantity=1):
        """新增書籍（對應 F-03）"""
        book = cls(
            title=title,
            author=author,
            isbn=isbn,
            category=category,
            description=description,
            status=status,
            quantity=quantity
        )
        db.session.add(book)
        db.session.commit()
        return book

    def update(self, **kwargs):
        """修改書籍資料（對應 F-03）"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
        db.session.commit()
        return self

    def delete(self):
        """刪除書籍（對應 F-03）"""
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Book id={self.id} title={self.title} status={self.status}>'
