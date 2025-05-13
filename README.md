# SQLite SDK

## 概要
Windows 11環境でPython 3.10.11とSQLite3を使用した、データベース操作のための高機能なSDKです。

## 主な機能
- 基本的なCRUD操作
- データのソート機能
- 単一キーによる検索
- 複数キーによる検索
- キーによるレコード更新

## 高度な機能
### トランザクション管理
複数の操作をまとめて実行し、データの整合性を保証します。
```python
# トランザクションの使用例
db.begin_transaction()
try:
    db.insert('users', {'name': 'Alice'})
    db.insert('profiles', {'user_id': 1})
    db.commit_transaction()
except Exception as e:
    db.rollback_transaction()
    print(f'エラー: {e}')
```

### ビューの使用
複雑なクエリを再利用可能な仮想テーブルとして定義できます。
```python
# ユーザー情報とプロフィールを結合したビューの作成
db.create_view('user_profiles', '''
    SELECT users.*, profiles.* 
    FROM users 
    JOIN profiles ON users.id = profiles.user_id
''')
```

### インデックスの活用
検索パフォーマンスを向上させるためのインデックスを管理します。
```python
# 検索頻度の高いカラムにインデックスを作成
db.create_index('users', 'email')

# インデックスの削除
db.drop_index('idx_users_email')
```

### JOIN操作
複数のテーブルを結合してデータを取得します。
```python
# ユーザーとその注文情報を結合して取得
result = db.join(
    'users',
    'orders',
    {'users.id': 'orders.user_id'},
    join_type='LEFT'
)
```

### トリガーの設定
特定のイベント発生時に自動的に実行される処理を定義します。
```python
# 更新日時を自動更新するトリガー
db.create_trigger(
    'update_timestamp',
    'users',
    'AFTER',
    'UPDATE',
    'UPDATE users SET updated_at = CURRENT_TIMESTAMP'
)
```

### JSONデータの操作
JSON形式のデータを効率的に保存・検索します。
```python
# JSON形式のデータを保存
db.insert_json('settings', {
    'theme': 'dark',
    'notifications': {'email': True, 'push': False}
})

# JSON内の特定の値で検索
results = db.query_json(
    'settings',
    'notifications',
    'email',
    True
)
```

### エラーハンドリング
発生しうる様々なエラーに対して適切に対処します。
```python
try:
    db.create_table('existing_table', {...})
except TableExistsError as e:
    print(f'エラー: {e}')
except DatabaseError as e:
    print(f'データベースエラー: {e}')
```

## インストール方法
```bash
pip install -r requirements.txt
```

## 使用例
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

## テスト実行
```bash
python -m pytest tests/
```

## 注意事項
1. データベースファイルは適切な権限で管理してください
2. 大量のデータを扱う場合は、インデックスの活用を検討してください
3. 重要なデータは定期的にバックアップを取ることをお勧めします
4. トランザクションを使用する際は、必ずエラーハンドリングを実装してください
5. 複雑なJSONデータを扱う場合は、クエリのパフォーマンスに注意してください