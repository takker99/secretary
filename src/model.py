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

# TODO: 作成するクラス一覧
#
# - tasks: taskの追加・変更・複製・削除を行う
# - projects: projectの追加・変更・複製・削除を行う。またproject treeの操作も行う
#   - projectのdatabaseと、idで関連付けられたtreeを管理する
# - records: recordの追加・変更・複製・削除を行う
#
# tagによる検索機能もつける


class Task:
    pass


class Record:
    pass


class Project:
    pass


class Tag:
    pass


class ProjectManager:
    pass


class TaskManager:
    def __init__(self):
        pass


class RecordManager:
    pass
