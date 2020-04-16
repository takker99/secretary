#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""モジュールの説明タイトル

    - sqlite3を使いやすくしたヘルパークラス
    - 変換formatは./README.mdを参照

Todo:
   TODOリストを記載
    * conf.pyの``sphinx.ext.todo`` を有効にしないと使用できない
    * conf.pyの``todo_include_todos = True``にしないと表示されない

"""
import sqlite3
from typing import Dict, Sequence, Any

# sqlite3で使用できる型


class Database:
    def __init__(self, database):
        self.__connection = sqlite3.connect(database)

    def drop(self, table_name: str) -> sqlite3.Cursor:
        """テーブルを削除する

        tableを削除する。指定されたtableが存在しなければ何もしない

        :param table_name: 削除するtableの名前
        :returns: cursor object

        """
        return self.__connection.execute(f"drop table if exists {table_name}")

    def create(self, table_name: str, column_settings: Sequence[str]) -> sqlite3.Cursor:
        """テーブルを作成する

        tableを作成する。すでにtableが存在していたら何もしない。

        :param table_name: 作成するtableの名前
        :returns: cursor object

        """
        return self.__connection.execute(f"create table if not exists {table_name}({','.join(column_settings)})")

    def insert(self, table_name: str, arguments: Dict[str, Any]) -> sqlite3.Cursor:
        """テーブルにデータを一列追加する

        :param table_name: tableの名前
        :param arguments: 追加するデータ名とその値のペアの辞書
        :returns: cursor object

        """
        # 順番を一致させたkeyとvalueのlistを作る
        keys = [key for key in arguments]
        values = [arguments[key] for key in keys]

        return self.__connection.execute(f"insert into {table_name}({','.join(keys)}) values ({','.join(['?']*len(values))})", values)

    def update(self, table_name: str, set_: Dict[str, Any], where: str):
        """tableのデータを更新する

        :param table_name: 作成するtableの名前
        :param set_: 更新するカラム名と値のdictionary
        :returns: cursor object

        """
        return self.__connection.execute("update {0} set {1} where{2}".format(table_name, ','.join([f"{key} = {value}" for key, value in set_.items()]), where))

    def exists(self, table_name: str, where: str) -> bool:
        """テーブル中に、指定した条件に当てはまる要素が存在するか調べる

        :param table_name 調べるtableの名前
        :returns: 一つでも存在すればTrue

        """

        if self.__connection.execute(f"select * from {table_name} where {where}").fetchone() is not None:
            return True
        else:
            return False

    def __del__(self) -> None:
        self.__connection.close()
