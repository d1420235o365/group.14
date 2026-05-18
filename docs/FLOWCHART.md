# 書籍查詢系統 — 流程圖文件 (FLOWCHART.md)

> 版本：1.0 | 日期：2026-05-18

---

## 一、使用者流程圖（User Flow）

### 1.1 一般使用者流程

```mermaid
flowchart LR
    A([使用者開啟網頁]) --> B[首頁]
    B --> C[輸入關鍵字搜尋]
    C --> D{有符合的書籍？}
    D -->|是| E[顯示書籍列表]
    D -->|否| F[顯示查無結果訊息]
    F --> C
    E --> G[點擊書籍]
    G --> H[書籍詳細資訊頁]
    H --> I{庫存狀態}
    I -->|在庫| J[顯示綠色在庫標籤]
    I -->|已借出| K[顯示橘色已借出標籤]
    I -->|補貨中| L[顯示紅色補貨中標籤]
    H --> M([返回列表])
    M --> E
```

### 1.2 管理者流程

```mermaid
flowchart LR
    A([管理者開啟網頁]) --> B[進入管理後台]
    B --> C{選擇操作}
    C -->|新增書籍| D[填寫書籍表單]
    D --> E{資料驗證}
    E -->|通過| F[儲存至資料庫]
    E -->|失敗| G[顯示錯誤訊息]
    G --> D
    F --> H[返回書籍列表]

    C -->|修改書籍| I[選擇書籍]
    I --> J[載入既有資料到表單]
    J --> K[修改並送出]
    K --> E

    C -->|刪除書籍| L[選擇書籍]
    L --> M{確認刪除？}
    M -->|確認| N[從資料庫刪除]
    M -->|取消| H
    N --> H

    C -->|更新庫存狀態| O[選擇書籍]
    O --> P[修改狀態為 在庫 / 已借出 / 補貨中]
    P --> F
```

---

## 二、系統序列圖（Sequence Diagram）

### 2.1 使用者搜尋書籍

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Book Model
    participant DB as SQLite

    User->>Browser: 輸入關鍵字並點擊搜尋
    Browser->>Flask: GET /books?q=關鍵字
    Flask->>Model: Book.search("關鍵字")
    Model->>DB: SELECT * FROM books WHERE title LIKE '%關鍵字%' OR author LIKE '%關鍵字%'
    DB-->>Model: 回傳符合書籍列表
    Model-->>Flask: [Book, Book, ...]
    Flask->>Browser: render_template("books/list.html", books=...)
    Browser-->>User: 顯示書籍列表頁面
```

### 2.2 使用者查看書籍詳情

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Book Model
    participant DB as SQLite

    User->>Browser: 點擊書籍卡片
    Browser->>Flask: GET /books/1
    Flask->>Model: Book.get_by_id(1)
    Model->>DB: SELECT * FROM books WHERE id = 1
    DB-->>Model: 回傳書籍資料
    Model-->>Flask: Book 物件
    Flask->>Browser: render_template("books/detail.html", book=...)
    Browser-->>User: 顯示書籍詳細頁面（含庫存狀態）
```

### 2.3 管理者新增書籍

```mermaid
sequenceDiagram
    actor Admin as 管理者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Book Model
    participant DB as SQLite

    Admin->>Browser: 填寫新增書籍表單並送出
    Browser->>Flask: POST /admin/books/create
    Flask->>Flask: 驗證表單資料
    Flask->>Model: Book.create(title, author, description, status, quantity)
    Model->>DB: INSERT INTO books VALUES (...)
    DB-->>Model: 新增成功，回傳 id
    Model-->>Flask: 新 Book 物件
    Flask->>Browser: redirect("/admin/books")
    Browser-->>Admin: 顯示書籍管理列表（含新書）
```

### 2.4 管理者刪除書籍

```mermaid
sequenceDiagram
    actor Admin as 管理者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Book Model
    participant DB as SQLite

    Admin->>Browser: 點擊刪除按鈕並確認
    Browser->>Flask: POST /admin/books/delete/1
    Flask->>Model: Book.delete(1)
    Model->>DB: DELETE FROM books WHERE id = 1
    DB-->>Model: 刪除成功
    Model-->>Flask: True
    Flask->>Browser: redirect("/admin/books")
    Browser-->>Admin: 顯示更新後的書籍列表
```

---

## 三、功能清單對照表

| 功能編號 | 功能名稱 | HTTP 方法 | URL 路徑 | 對應模板 |
|----------|----------|-----------|----------|----------|
| F-01 | 多條件書籍搜尋 | GET | `/books?q=關鍵字` | `books/list.html` |
| F-02 | 書籍詳細資訊與狀態顯示 | GET | `/books/<id>` | `books/detail.html` |
| F-03a | 新增書籍（表單頁） | GET | `/admin/books/create` | `admin/create.html` |
| F-03b | 新增書籍（送出） | POST | `/admin/books/create` | redirect → 列表 |
| F-03c | 修改書籍（表單頁） | GET | `/admin/books/edit/<id>` | `admin/edit.html` |
| F-03d | 修改書籍（送出） | POST | `/admin/books/edit/<id>` | redirect → 列表 |
| F-03e | 刪除書籍 | POST | `/admin/books/delete/<id>` | redirect → 列表 |
| —      | 管理後台首頁 | GET | `/admin` | `admin/dashboard.html` |
| —      | 網站首頁 | GET | `/` | `index.html` |
