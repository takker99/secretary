#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""モジュールの説明タイトル

    - databaseを管理するclass
    - 変換formatは./README.mdを参照

Todo:
   TODOリストを記載
    * conf.pyの``sphinx.ext.todo`` を有効にしないと使用できない
    * conf.pyの``todo_include_todos = True``にしないと表示されない

"""
import datetime
from typing import List
from enum import Enum, auto
import uuid
# TODO: 作成するクラス一覧
#
# - tasks: taskの追加・変更・複製・削除を行う
# - projects: projectの追加・変更・複製・削除を行う。またproject treeの操作も行う
#   - projectのdatabaseと、idで関連付けられたtreeを管理する
# - records: recordの追加・変更・複製・削除を行う
#
# tagによる検索機能もつける


class Status(Enum):
    """
    Taskに指定できるstatusを定義した列挙型
    """
    ACTIVE = auto()    # 有効なタスク
    ARCHIVED = auto()  # 期限切れもしくは完了


class Task:
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__summary = ''                          # type: str
        self.__description = ''                      # type: str
        self.__length = 0                            # type: int
        self.__deadline = datetime.datetime()        # type: datetime.datetime
        self.__is_completed = 0.0                    # type: float
        self.__status = Status.ACTIVE                # type: Status
        self.__priority = 0                          # type: int
        self.__tag_list = list()                     # type: List[str]
        self.__location = ''                         # type: str
        self.__created_at = datetime.datetime.now()  # type: datetime.datetime
        self.__updated_at = datetime.datetime.now()  # type: datetime.datetime


class Record:
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__summary = ''                          # type: str
        self.__is_completed = 0.0                    # type: float
        self.__begin = datetime.datetime.now()       # type: datetime.datetime
        self.__end = datetime.datetime.now()         # type: datetime.datetime
        self.__tag_list = list()                     # type: List[str]
        self.__location = ''                         # type: str
        self.__commit_message = ''                     # type: str


class Project:
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__name = 'no-name'                      # type: str
        self.__reference = ['../memo/memo.md']         # type: List[str]
        self.__begin = datetime.datetime.now()       # type: datetime.datetime
        self.__end = datetime.datetime.now()         # type: datetime.datetime
        self.__status = Status.ACTIVE                # type: Status
        self.__priority = 0                          # type: int
        self.__tag_list = list()                     # type: List[str]
        self.__task_list = list()                    # type: List[str]
        self.__created_at = datetime.datetime.now()  # type: datetime.datetime
        self.__updated_at = datetime.datetime.now()  # type: datetime.datetime


class Tag:
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__name = 'no-name'                      # type: str


class ProjectManager:
    pass


class TaskManager:
    def __init__(self):
        pass


class RecordManager:
    pass
