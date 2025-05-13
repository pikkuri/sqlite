# src/core/db_manager.py
import sqlite3
import json
from typing import Any, Dict, List, Optional, Union
from .errors import (
    DatabaseError, TableExistsError, ViewExistsError,
    TriggerExistsError, IndexExistsError, TransactionError
)

class DatabaseManager:
    """拡張SQLite データベースマネージャー"""

    def __init__(self, db_path: str):
        """
        データベースマネージャーの初期化
        Args:
            db_path (str): データベースファイルのパス
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self) -> None:
        """データベース接続を確立"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            raise DatabaseError(f"データベース接続エラー: {str(e)}")

    def begin_transaction(self) -> None:
        """トランザクションを開始"""
        try:
            self.cursor.execute("BEGIN TRANSACTION")
        except sqlite3.Error as e:
            raise TransactionError(f"トランザクション開始エラー: {str(e)}")

    def commit_transaction(self) -> None:
        """トランザクションをコミット"""
        try:
            self.conn.commit()
        except sqlite3.Error as e:
            raise TransactionError(f"トランザクションコミットエラー: {str(e)}")

    def rollback_transaction(self) -> None:
        """トランザクションをロールバック"""
        try:
            self.conn.rollback()
        except sqlite3.Error as e:
            raise TransactionError(f"トランザクションロールバックエラー: {str(e)}")

    def create_view(self, view_name: str, select_query: str) -> None:
        """
        ビューを作成
        Args:
            view_name (str): ビュー名
            select_query (str): SELECT文
        """
        try:
            self.cursor.execute(f"CREATE VIEW {view_name} AS {select_query}")
            self.conn.commit()
        except sqlite3.Error as e:
            if "already exists" in str(e):
                raise ViewExistsError(f"ビュー '{view_name}' は既に存在します")
            raise DatabaseError(f"ビュー作成エラー: {str(e)}")

    def drop_view(self, view_name: str) -> None:
        """
        ビューを削除
        Args:
            view_name (str): 削除するビュー名
        """
        try:
            self.cursor.execute(f"DROP VIEW IF EXISTS {view_name}")
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"ビュー削除エラー: {str(e)}")

    def create_index(self, table_name: str, column_name: str, index_name: str = None) -> None:
        """
        インデックスを作成
        Args:
            table_name (str): テーブル名
            column_name (str): カラム名
            index_name (str, optional): インデックス名
        """
        if index_name is None:
            index_name = f"idx_{table_name}_{column_name}"
        try:
            self.cursor.execute(f"CREATE INDEX {index_name} ON {table_name}({column_name})")
            self.conn.commit()
        except sqlite3.Error as e:
            if "already exists" in str(e):
                raise IndexExistsError(f"インデックス '{index_name}' は既に存在します")
            raise DatabaseError(f"インデックス作成エラー: {str(e)}")

    def drop_index(self, index_name: str) -> None:
        """
        インデックスを削除
        Args:
            index_name (str): 削除するインデックス名
        """
        try:
            self.cursor.execute(f"DROP INDEX IF EXISTS {index_name}")
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"インデックス削除エラー: {str(e)}")

    def join(
        self,
        table1: str,
        table2: str,
        on: Dict[str, str],
        join_type: str = 'INNER',
        columns: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        テーブルを結合
        Args:
            table1 (str): 1番目のテーブル名
            table2 (str): 2番目のテーブル名
            on (Dict[str, str]): 結合条件
            join_type (str): 結合タイプ (INNER, LEFT, RIGHT, FULL)
            columns (List[str], optional): 取得するカラム
        Returns:
            List[Dict[str, Any]]: 結合結果
        """
        columns_str = "*" if not columns else ", ".join(columns)
        conditions = " AND ".join([f"{k} = {v}" for k, v in on.items()])
        query = f"""
            SELECT {columns_str}
            FROM {table1}
            {join_type} JOIN {table2}
            ON {conditions}
        """
        try:
            self.cursor.execute(query)
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            raise DatabaseError(f"テーブル結合エラー: {str(e)}")

    def create_trigger(
        self,
        trigger_name: str,
        table_name: str,
        when: str,
        event: str,
        action: str
    ) -> None:
        """
        トリガーを作成
        Args:
            trigger_name (str): トリガー名
            table_name (str): 対象テーブル名
            when (str): タイミング (BEFORE, AFTER)
            event (str): イベント (INSERT, UPDATE, DELETE)
            action (str): 実行するSQL
        """
        query = f"""
            CREATE TRIGGER {trigger_name}
            {when} {event} ON {table_name}
            BEGIN
                {action};
            END
        """
        try:
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            if "already exists" in str(e):
                raise TriggerExistsError(f"トリガー '{trigger_name}' は既に存在します")
            raise DatabaseError(f"トリガー作成エラー: {str(e)}")

    def drop_trigger(self, trigger_name: str) -> None:
        """
        トリガーを削除
        Args:
            trigger_name (str): 削除するトリガー名
        """
        try:
            self.cursor.execute(f"DROP TRIGGER IF EXISTS {trigger_name}")
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"トリガー削除エラー: {str(e)}")

    def insert_json(self, table_name: str, json_data: Dict[str, Any]) -> None:
        """
        JSON形式のデータを挿入
        Args:
            table_name (str): テーブル名
            json_data (Dict[str, Any]): 挿入するJSONデータ
        """
        serialized_data = {
            k: json.dumps(v) if isinstance(v, (dict, list)) else v
            for k, v in json_data.items()
        }
        placeholders = ", ".join(["?" for _ in serialized_data])
        columns = ", ".join(serialized_data.keys())
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        
        try:
            self.cursor.execute(query, list(serialized_data.values()))
            self.conn.commit()
        except sqlite3.Error as e:
            raise DatabaseError(f"JSONデータ挿入エラー: {str(e)}")

    def query_json(
        self,
        table_name: str,
        json_column: str,
        json_path: str,
        value: Any
    ) -> List[Dict[str, Any]]:
        """
        JSON内の特定パスの値で検索
        Args:
            table_name (str): テーブル名
            json_column (str): JSONデータを含むカラム名
            json_path (str): JSONパス
            value: 検索値
        Returns:
            List[Dict[str, Any]]: 検索結果
        """
        query = f"""
            SELECT *
            FROM {table_name}
            WHERE json_extract({json_column}, '$.{json_path}') = ?
        """
        try:
            self.cursor.execute(query, (value,))
            return [dict(row) for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            raise DatabaseError(f"JSON検索エラー: {str(e)}")

    def __del__(self):
        """デストラクタ: 接続をクローズ"""
        if self.conn:
            self.conn.close()