# tests/test_db_manager.py
import pytest
import os
from src.core.db_manager import DatabaseManager

class TestDatabaseManager:
    """DatabaseManagerのテストクラス"""
    
    @pytest.fixture
    def db_manager(self):
        """テスト用のDatabaseManagerインスタンスを準備"""
        test_db = "test_database.db"
        # テスト前に古いDBファイルを削除
        if os.path.exists(test_db):
            os.remove(test_db)
        db_manager = DatabaseManager(test_db)
        yield db_manager
        # テスト後にDBファイルを削除
        if os.path.exists(test_db):
            os.remove(test_db)

    def test_create_table(self, db_manager):
        """テーブル作成機能のテスト"""
        # テストデータ
        table_name = "test_table"
        columns = {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "age": "INTEGER"
        }
        
        # テーブル作成を実行
        result = db_manager.create_table(table_name, columns)
        assert result is True

    def test_insert_and_find(self, db_manager):
        """データ挿入と検索機能のテスト"""
        # テストテーブルを作成
        table_name = "test_table"
        columns = {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "age": "INTEGER"
        }
        db_manager.create_table(table_name, columns)
        
        # テストデータを挿入
        test_data = {
            "name": "Test User",
            "age": 30
        }
        result = db_manager.insert(table_name, test_data)
        assert result is True
        
        # データを検索
        found = db_manager.find(table_name, {"age": 30})
        assert len(found) == 1
        assert found[0]["name"] == "Test User"
        assert found[0]["age"] == 30

    def test_update(self, db_manager):
        """データ更新機能のテスト"""
        # テストテーブルを作成
        table_name = "test_table"
        columns = {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "age": "INTEGER"
        }
        db_manager.create_table(table_name, columns)
        
        # テストデータを挿入
        test_data = {
            "name": "Test User",
            "age": 30
        }
        db_manager.insert(table_name, test_data)
        
        # データを更新
        update_result = db_manager.update(
            table_name,
            "name",
            "Test User",
            {"age": 31}
        )
        assert update_result is True
        
        # 更新を確認
        found = db_manager.find(table_name, {"name": "Test User"})
        assert len(found) == 1
        assert found[0]["age"] == 31

    def test_find_with_sort(self, db_manager):
        """ソート機能付きデータ検索のテスト"""
        # テストテーブルを作成
        table_name = "test_table"
        columns = {
            "id": "INTEGER PRIMARY KEY",
            "name": "TEXT",
            "age": "INTEGER"
        }
        db_manager.create_table(table_name, columns)
        
        # テストデータを挿入
        test_data = [
            {"name": "User A", "age": 25},
            {"name": "User B", "age": 30},
            {"name": "User C", "age": 20}
        ]
        for data in test_data:
            db_manager.insert(table_name, data)
        
        # 年齢でソートして検索
        found = db_manager.find(table_name, {}, sort_by="age", order="ASC")
        assert len(found) == 3
        assert found[0]["age"] == 20
        assert found[2]["age"] == 30