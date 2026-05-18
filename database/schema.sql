-- database/schema.sql
-- 書籍查詢系統 資料庫建表語法

CREATE TABLE IF NOT EXISTS book (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    title       TEXT     NOT NULL,
    author      TEXT     NOT NULL,
    isbn        TEXT,
    category    TEXT,
    description TEXT,
    status      TEXT     NOT NULL DEFAULT '在庫'
                         CHECK(status IN ('在庫', '已借出', '補貨中')),
    quantity    INTEGER  NOT NULL DEFAULT 1,
    created_at  DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);
