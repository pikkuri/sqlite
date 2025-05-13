# src/models/base_model.py
from typing import Dict, Any, Optional, List
from ..core.db_manager import DatabaseManager

class BaseModel:
    """
    モデルの基本クラス
    すべてのモデルクラスの基底となる共通機能を提供
    """
    
    def __init__(self, db_manager: DatabaseManager):
        """
        BaseModelの初期化
        Args:
            db_manager: DatabaseManagerインスタンス
        """
        self.db_manager = db_manager
        self.table_name = ""  # サブクラスで上書き
        self.fields = {}      # サブクラスで上書き

    def create_table(self) -> bool:
        """
        モデルのテーブルを作成
        Returns:
            bool: テーブル作成成功時True
        """
        return self.db_manager.create_table(self.table_name, self.fields)

    def save(self, data: Dict[str, Any]) -> bool:
        """
        モデルのデータを保存
        Args:
            data: 保存するデータの辞書
        Returns:
            bool: 保存成功時True
        """
        return self.db_manager.insert(self.table_name, data)

    def find(self, conditions: Dict[str, Any], sort_by: Optional[str] = None, 
             order: str = 'ASC') -> List[Dict[str, Any]]:
        """
        条件に基づいてデータを検索
        Args:
            conditions: 検索条件
            sort_by: ソートするカラム
            order: ソート順序
        Returns:
            List[Dict]: 検索結果のリスト
        """
        return self.db_manager.find(self.table_name, conditions, sort_by, order)

    def update(self, key_column: str, key_value: Any, 
              update_data: Dict[str, Any]) -> bool:
        """
        データを更新
        Args:
            key_column: キーカラム
            key_value: キー値
            update_data: 更新データ
        Returns:
            bool: 更新成功時True
        """
        return self.db_manager.update(self.table_name, key_column, key_value, update_data)