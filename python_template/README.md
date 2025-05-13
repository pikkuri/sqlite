# SQLite SDK

## 概要
Windows 11環境でPython 3.10.11とSQLite3を使用した、データベース操作のための高機能なSDKです。

## 主な機能
- 基本的なCRUD操作
- データのソート機能
- 単一キーによる検索
- 複数キーによる検索
- キーによるレコード更新

## 用語解説
### SQLiteの基本用語
- **データベース (Database)**: データを永続的に保存するためのファイルシステム
- **テーブル (Table)**: データを行と列で管理する表形式の構造
- **レコード (Record)**: テーブル内の1行分のデータ
- **カラム (Column)**: テーブル内の各項目（フィールド）
- **プライマリーキー (Primary Key)**: レコードを一意に識別するための値
- **インデックス (Index)**: データの検索を高速化するための仕組み

### SDKの技術用語
- **CRUD操作**: Create（作成）、Read（読み取り）、Update（更新）、Delete（削除）の基本的なデータ操作
- **クエリビルダー**: SQLクエリを簡単に構築するためのツール
- **バリデーション**: データの整合性を確認する機能

## インストール方法
```bash
pip install -r requirements.txt
```

## 詳細な使用方法
### 1. データベースの作成と接続
```python
from src.core.db_manager import DatabaseManager

# データベースの作成
db = DatabaseManager('my_database.db')
```

### 2. テーブル操作
```python
# テーブルの作成
db.create_table('products', {
    'id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT',
    'price': 'REAL',
    'stock': 'INTEGER'
})

# テーブルの削除
db.drop_table('products')
```

### 3. データの操作
```python
# 単一レコードの追加
db.insert('products', {
    'name': '商品A',
    'price': 1000,
    'stock': 50
})

# 複数レコードの検索
result = db.find('products', {
    'price': {'$gt': 500},
    'stock': {'$gt': 0}
})

# データの更新
db.update('products', 
    {'stock': 45}, 
    {'name': '商品A'}
)

# データの削除
db.delete('products', {'stock': 0})
```

### 4. 高度な検索とソート
```python
# 複数条件での検索
result = db.find('products', {
    'price': {'$lt': 2000},
    'stock': {'$gt': 10}
})

# ソート機能の使用
result = db.find('products', {}, sort={'price': 'DESC'})
```

## 基本的な使用例
```python
from src.core.db_manager import DatabaseManager

# データベースマネージャーの初期化
db = DatabaseManager('example.db')

# テーブルの作成
db.create_table('users', {
    'id': 'INTEGER PRIMARY KEY',
    'name': 'TEXT',
    'age': 'INTEGER'
})

# データの挿入
db.insert('users', {'name': 'John', 'age': 30})

# データの検索
result = db.find('users', {'age': 30})
```

## エラー対処方法
### よくあるエラーと解決方法
1. **データベース接続エラー**
   - 原因: データベースファイルへのアクセス権限がない
   - 解決: ファイルのパーミッションを確認

2. **テーブル作成エラー**
   - 原因: 同名のテーブルが既に存在する
   - 解決: テーブル名を変更するか、既存のテーブルを削除

3. **データ型エラー**
   - 原因: カラムの型と異なるデータを挿入しようとした
   - 解決: データ型を確認し、適切な型に変換

## 実践例
### ユーザー管理システムの例
```python
# ユーザーテーブルの作成
db.create_table('users', {
    'id': 'INTEGER PRIMARY KEY',
    'username': 'TEXT',
    'email': 'TEXT',
    'created_at': 'TIMESTAMP'
})

# ユーザーの登録
db.insert('users', {
    'username': 'test_user',
    'email': 'test@example.com',
    'created_at': '2023-05-13 10:00:00'
})

# メールアドレスでユーザーを検索
user = db.find('users', {'email': 'test@example.com'})
```

## テスト実行
```bash
python -m pytest tests/
```

## 注意事項
1. データベースファイルは適切な権限で管理してください
2. 大量のデータを扱う場合は、インデックスの活用を検討してください
3. 重要なデータは定期的にバックアップを取ることをお勧めします
