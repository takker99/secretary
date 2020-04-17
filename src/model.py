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
from typing import List, Dict
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


class IDPublisher:
    """
    idを発行するクラス

    発行されるidは各インスタンスごとに一意でなければならない
    """

    __slots__ = ['__next_id']

    def __init__(self, next_id: int = 0):
        """constructor

        :param next_id: 最初に発行するid。前回使用していたIDPublisherのデータを引き継ぐために使用する。
        """
        self.__next_id = next_id

    def publish(self) -> int:
        """idを発行する

        :return: 発行したid
        """
        temp = self.__next_id
        self.__next_id += 1
        return temp


class Status(Enum):
    """
    Taskに指定できるstatusを定義した列挙型
    """
    ACTIVE = auto()    # 有効なタスク
    ARCHIVED = auto()  # 期限切れもしくは完了


class Task:
    def __init__(self, summary: str,
                 length: int,
                 created_at: datetime.datetime,
                 updated_at: datetime.datetime,
                 description: str = None,
                 deadline: datetime.datetime = None,
                 is_completed: float = 0.0,
                 status: Status = Status.ACTIVE,
                 priority: int = None,
                 tags: List[Tag] = None,
                 location: str = None):
        """constructor

        :param id_: taskに紐付けるid. 初期化時以外では設定不可能
        """
        self.__summary = summary                          # type: str
        self.__description = description                      # type: str
        self.__length = length                            # type: int
        self.__deadline = deadline        # type: datetime.datetime
        self.__is_completed = is_completed                    # type: float
        self.__status = status                # type: Status
        self.__priority = priority                          # type: int
        self.__tag_list = tags                     # type: List[str]
        self.__location = location                         # type: str
        self.__created_at = created_at  # type: datetime.datetime
        self.__updated_at = updated_at  # type: datetime.datetime

    # property変更の都度、updated_atを更新する
    def __setattr__(self, name, value):
        if name != "__updated_at":
            self.__updated_at = datetime.datetime.now()
        super().__setattr__(name, value)

class Record:
    def __init__(self, id_):
        """constructor

        :param id_: taskに紐付けるid. 初期化時以外では設定不可能
        """
        self.__id = id_
        self.__summary = ''                          # type: str
        self.__is_completed = 0.0                    # type: float
        self.__begin = datetime.datetime.now()       # type: datetime.datetime
        self.__end = datetime.datetime.now()         # type: datetime.datetime
        self.__tag_list = list()                     # type: List[str]
        self.__location = ''                         # type: str
        self.__commit_message = ''                     # type: str


class Project:
    def __init__(self, id_):
        """constructor

        :param id_: taskに紐付けるid. 初期化時以外では設定不可能
        """
        self.__id = id_
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
        self.__tasks = dict()  # type: List[Task]
        self.__id_publisher = IDPublisher()

    def create(self, summary: str,
               length: int,
               description: str = None,
               deadline: datetime.datetime = None,
               status: Status = Status.ACTIVE,
               priority: int = None,
               tags: List[Tag] = None,
               location: str = None) -> None:
        """taskを新規作成する

        :function: TODO
        :returns: TODO

        """
        created_at = datetime.datetime.now()
        self.__tasks[self.__id_publisher.publish()] = Task(
            summary=summary,
            description=description,
            length=length,
            deadline=deadline,
            status=status,
            priority=priority,
            tags=tags,
            location=location,
            created_at=created_at,
            updated_at=created_at)

    def __append(self, id_, task: Task) -> None:
        """taskを追加する

        データファイルからtask listの情報を復元するときに使う。非公開。
        """
        self.__tasks[id_] = task

    def __getitem__(self, id_) -> Task:
        """Task managerが管理しているTaskを取得する

        :param id_:取得したいTaskのid
        :return: 指定したidに対応したTask
        :raise KeyError: if id_ doesn't exist
        """
        return self.__tasks[id_]

    # __setitem__はない。外部から好き勝手にタスクをいじれないようにする


class RecordManager:
    pass
