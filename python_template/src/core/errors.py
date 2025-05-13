# src/core/errors.py
class DatabaseError(Exception):
    """データベース操作の基本エラー"""
    pass

class TableExistsError(DatabaseError):
    """テーブルが既に存在する場合のエラー"""
    pass

class ViewExistsError(DatabaseError):
    """ビューが既に存在する場合のエラー"""
    pass

class TriggerExistsError(DatabaseError):
    """トリガーが既に存在する場合のエラー"""
    pass

class IndexExistsError(DatabaseError):
    """インデックスが既に存在する場合のエラー"""
    pass

class TransactionError(DatabaseError):
    """トランザクション操作のエラー"""
    pass

class ValidationError(DatabaseError):
    """データバリデーションのエラー"""
    pass

class ConnectionError(DatabaseError):
    """データベース接続のエラー"""
    pass

class QueryError(DatabaseError):
    """クエリ実行のエラー"""
    pass