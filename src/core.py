#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""モジュールの説明タイトル

    - secretary操作の窓口を担うクラス
    - 変換formatは./README.mdを参照

Todo:

"""
import datetime
from typing import List, Dict
from enum import Enum, auto
import uuid
from model import Tag, Task, Status, Project, Record

# 現状
#
# - とりあえず最低限揃っていてほしいcommandは列挙した。
# - 次は、これらをコマンドを実装するために必要な、各Managerのmethodを列挙する。こんな感じで設計を詰めていく。
# - idの型をあとからでも変えられるようにtypingで定義しておく
#   - もしかしたらidをulidに変えるかもしれない。そうなっても変更箇所が少ない設計にする

class Core:
    def __init__(self):
        pass

    def create_task(self, summary: str):
        """タスクを新規作成する

        :function: TODO
        :returns: TODO

        """
        # 内部実装はTask管理objectに委譲する
        pass

    def change_task(self, task_id: int,
                    summary: str = None,
                    description: str = None,
                    deadline: datetime.datetime = None,
                    status: Status = None,
                    location: str = None):
        """タスクの各種属性を変更する

        値がNoneだった変数は変更しない。


        :function: TODO
        :returns: TODO

        """
        # 内部実装はTask管理objectに委譲する
        pass

    def clone_task(self, task_id: int) -> int:
        """タスクを複製する

        :function: TODO
        :returns: 複製したtaskのid

        """
        # 内部実装はTask管理objectに委譲する
        pass

    def delete_task(self, task_id: int) -> None:
        """タスクを削除する

        :function: TODO
        :returns: TODO

        """
        # 内部実装はTask管理objectに委譲する
        pass

    def convert_task_to_project(self, task_id: int) -> int:
        """タスクをprojectに変換する

        :function: TODO
        :returns: 生成したprojectのid

        """
        # 内部実装
        # 1. project作成
        # 2. project treeに登録
        # 3. task削除
        # 4. (treeからの削除は3.で行う)
        pass

    def create_record(self,task_ids:List[int], begin:datetime.datetime,end:datetime.datetime,is_completed:bool,location:str,commit_message:str)->int:
        """recordを作成する

        タスク実行後に、すべての情報を一括して入力するときに使う

        :function: TODO
        :returns: 作成したrecordのid

        """
        pass

    def start_record(self,task_ids:List[int],location:str)->int:
        """recordを開始する

        :function: TODO
        :returns: 記録を開始したrecordのid

        """
        pass

    def end_record(self,record_id:int,location:str,commit_message:str):
        """recordを終了する

        :function: TODO
        :returns:

        """
        pass



    def create_project(self,
                       name: str) -> int:
        """projectを作成する

        :function: TODO
        :returns: 生成したprojectのid

        """
        # 内部実装はProject管理objectに委譲する
        pass

    def change_project(self, project_id: int,
                       name: str = None,
                       status: Status = None,
                       priority: int = None
                       ):
        """Projectの各種属性を変更する

        値がNoneだった変数は変更しない。


        :function: TODO
        :returns: TODO

        """
        # 内部実装はTask管理objectに委譲する
        pass

    def move_project(self, project_id: int,
                     new_begin: datetime.datetime
                     ):
        """Projectを時間軸上で移動する

        :function: TODO
        :returns: TODO

        """
        # 内部実装はTask管理objectに委譲する
        pass

    def change_project_span(self, project_id: int,
                            begin: datetime.datetime,
                            end: datetime.datetime
                            ):
        """Projectの開始・終了時刻を変える

        長さが、配下のtaskの合計見積もり時間を超えていたらエラーを出す

        :function: TODO
        :returns: TODO

        """
        # 内部実装はTask管理objectに委譲する
        pass

# tree 関連
    def add_project(self, project_id, tree_path: List[int]):
        """指定したproject treeにprojectを紐付ける
        """
        pass

    def remove_project(self, tree_path: List[int]):
        """指定したproject treeの末端を外す
        """
        pass

    def move_tree(self, tree_path:List[int],target_path:List[int]):
        """project treeを移動する

        :param tree_path: 移動したいproject treeへのpath
        :returns: TODO

        """
        pass

    def show_tree(self, tree_path: List[int],show_id:bool=true) -> str:
        """指定したprojectからのproject treeを表示する

        """
        pass


# tag系method

    def change_tag(self, tags: List[Tag],
                   task_id: int = None,
                   record_id=None,
                   project_id=None):
        """各種objectのtagを一括変更する

        2つ以上のidに値を入れたらエラー

        :function: TODO
        :returns: TODO

        """
        # 内部実装はTag管理objectに委譲する
        pass

    def add_tag(self, tags: List[Tag],
                task_id: int = None,
                record_id=None,
                project_id=None):
        """各種objectにtagを追加する

        2つ以上のidに値を入れたらエラー

        :function: TODO
        :returns: TODO

        """
        # 内部実装はTag管理objectに委譲する
        pass

    def remove_tag(self, tags: List[Tag],
                   task_id: int = None,
                   record_id=None,
                   project_id=None):
        """各種objectからtagを外す

        2つ以上のidに値を入れたらエラー

        :function: TODO
        :returns: TODO

        """
        # 内部実装はTag管理objectに委譲する
        pass

    def create_tag(self, name: str) -> int:
        """tagを新規作成する

        :function: TODO
        :returns: 生成したtagのid

        """
        # 内部実装はTag管理objectに委譲する
        pass

    def rename_tag(self, tag_id, name: str) -> None:
        """tagの名前を変更する

        :function: TODO
        :returns: 生成したtagのid

        """
        # 内部実装はTag管理objectに委譲する
        pass

    def replace_tag(self, source_tag_id, dist_tag_id) -> None:
        """tagをすべて別のtagで置き換える。置き換えられたtagは削除する

        :function: TODO
        :returns: 生成したtagのid

        """
        # 内部実装はTag管理objectに委譲する
        pass

    def delete_tag(self, tag_id) -> None:
        """tagを削除する

        :function: TODO
        :returns: 生成したtagのid

        """
        # 内部実装はTag管理objectに委譲する
        pass

    # 検索系
    def find_task(self,
            tag_ids: List[int]=None,
            time_span: List[datetime.datetime] = None,
            belong_to: List[int] = None,
            achievement: float = None,
            status:Status=Status.ACTIVE)->List[int]:
        """条件に一致するtaskのリストを取得する

        :param belong_to: 所属先のprojectのid list
        :returns: TODO

        """
        pass

    def find_record(self,
            tag_ids: List[int]=None,
            time_span: List[datetime.datetime] = None,
            belong_to: List[int] = None,
            achievement: float = None,
            status:Status=Status.ACTIVE)->List[int]:
        """条件に一致するrecordのリストを取得する

        :param belong_to: 所属先のtaskのid list
        :returns: TODO

        """
        pass

    def find_project(self,
            tag_ids: List[int]=None,
            time_span: List[datetime.datetime] = None,
            belong_to: List[int] = None,
            achievement: float = None,
            status:Status=Status.ACTIVE)->List[int]:
        """条件に一致するprojectのリストを取得する

        :param belong_to: 所属先のprojectのid list
        :returns: TODO

        """
        pass

    # 集計
    def create_achievement_chart(self, task_ids: List[List[int]]):
        """taskの二次元リストから、日にちごとのタスクの達成度表をexcelで出力する
        """
        pass


    # 内部函数：イヴェント発火時に自動で実行するもの
    def expire_project(self, project_id):
        """projectを期限切れにし、inbox projectにcloneしたprojectを放り込む
        """
        pass
