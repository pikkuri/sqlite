# src/utils/validators.py
from typing import Dict, Any, List, Optional
import re

class Validators:
    """データ検証用ユーティリティクラス"""

    @staticmethod
    def validate_table_name(table_name: str) -> bool:
        """
        テーブル名の有効性を検証
        Args:
            table_name: 検証するテーブル名
        Returns:
            bool: 有効な場合True
        """
        # テーブル名は文字で始まり、文字、数字、アンダースコアのみ許可
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, table_name))

    @staticmethod
    def validate_column_name(column_name: str) -> bool:
        """
        カラム名の有効性を検証
        Args:
            column_name: 検証するカラム名
        Returns:
            bool: 有効な場合True
        """
        # カラム名は文字で始まり、文字、数字、アンダースコアのみ許可
        pattern = r'^[a-zA-Z][a-zA-Z0-9_]*$'
        return bool(re.match(pattern, column_name))

    @staticmethod
    def validate_sqlite_type(data_type: str) -> bool:
        """
        SQLiteデータ型の有効性を検証
        Args:
            data_type: 検証するデータ型
        Returns:
            bool: 有効な場合True
        """
        valid_types = {
            'INTEGER', 'TEXT', 'REAL', 'BLOB', 'NULL',
            'VARCHAR', 'CHAR', 'DECIMAL', 'BOOLEAN', 'DATE', 'DATETIME'
        }
        return data_type.upper() in valid_types

    @staticmethod
    def validate_column_definition(columns: Dict[str, str]) -> bool:
        """
        カラム定義の有効性を検証
        Args:
            columns: カラム名とデータ型の辞書
        Returns:
            bool: すべて有効な場合True
        """
        if not columns:
            return False
            
        for column_name, data_type in columns.items():
            if not Validators.validate_column_name(column_name):
                return False
            if not Validators.validate_sqlite_type(data_type.split()[0]):
                return False
        return True

    @staticmethod
    def validate_data_type(value: Any, expected_type: str) -> bool:
        """
        値のデータ型を検証
        Args:
            value: 検証する値
            expected_type: 期待されるSQLiteデータ型
        Returns:
            bool: 型が一致する場合True
        """
        type_map = {
            'INTEGER': int,
            'TEXT': str,
            'REAL': float,
            'BOOLEAN': bool
        }
        
        expected_type = expected_type.upper().split()[0]
        if expected_type not in type_map:
            return True  # 不明な型は検証をスキップ
            
        return isinstance(value, type_map[expected_type])