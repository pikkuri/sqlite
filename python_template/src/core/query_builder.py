# src/core/query_builder.py
from typing import Dict, List, Any, Optional

class QueryBuilder:
    """SQLクエリを動的に構築するユーティリティクラス"""

    @staticmethod
    def build_select_query(table_name: str, 
                          conditions: Optional[Dict[str, Any]] = None,
                          sort_by: Optional[str] = None,
                          order: str = 'ASC') -> Tuple[str, List[Any]]:
        """
        SELECT文を構築
        Args:
            table_name: テーブル名
            conditions: WHERE句の条件
            sort_by: ORDER BY句のカラム
            order: ソート順
        Returns:
            Tuple[str, List]: クエリ文字列とパラメータのタプル
        """
        query = f"SELECT * FROM {table_name}"
        params = []

        if conditions:
            where_conditions = []
            for key, value in conditions.items():
                where_conditions.append(f"{key} = ?")
                params.append(value)
            query += " WHERE " + " AND ".join(where_conditions)

        if sort_by:
            query += f" ORDER BY {sort_by} {order}"

        return query, params

    @staticmethod
    def build_insert_query(table_name: str, data: Dict[str, Any]) -> Tuple[str, List[Any]]:
        """
        INSERT文を構築
        Args:
            table_name: テーブル名
            data: 挿入するデータ
        Returns:
            Tuple[str, List]: クエリ文字列とパラメータのタプル
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        return query, list(data.values())

    @staticmethod
    def build_update_query(table_name: str, 
                          update_data: Dict[str, Any],
                          conditions: Dict[str, Any]) -> Tuple[str, List[Any]]:
        """
        UPDATE文を構築
        Args:
            table_name: テーブル名
            update_data: 更新するデータ
            conditions: WHERE句の条件
        Returns:
            Tuple[str, List]: クエリ文字列とパラメータのタプル
        """
        set_clause = ", ".join([f"{k} = ?" for k in update_data.keys()])
        where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        
        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
        params = list(update_data.values()) + list(conditions.values())
        
        return query, params

    @staticmethod
    def build_delete_query(table_name: str, 
                          conditions: Dict[str, Any]) -> Tuple[str, List[Any]]:
        """
        DELETE文を構築
        Args:
            table_name: テーブル名
            conditions: WHERE句の条件
        Returns:
            Tuple[str, List]: クエリ文字列とパラメータのタプル
        """
        where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        query = f"DELETE FROM {table_name} WHERE {where_clause}"
        return query, list(conditions.values())