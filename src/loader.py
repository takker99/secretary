#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""モジュールの説明タイトル

    - toml<-->sqlite3の相互変換script
    - 変換formatは./README.mdを参照

Todo:
   TODOリストを記載
    * conf.pyの``sphinx.ext.todo`` を有効にしないと使用できない
    * conf.pyの``todo_include_todos = True``にしないと表示されない

"""
import pandas as pd
import toml
import sqlite3
import argparse
import pathlib
import uuid
import sys
from library.database import Database
from contextlib import closing
import datetime


def insert(cursor, table_name, tuple_values):
    return cursor.executemany(f"insert into {table_name} values ({','.join(['?']*len(tuple_values[0]))})", tuple_values)


def reset_table(cursor, table_name, column_settings):
    print(f"creating table \"{table_name}\"...", end="")
    cursor.execute(f"drop table if exists {table_name}")
    cursor.execute(
        f"create table {table_name}({column_settings})")
    print("done.")

def replace_unix_time(dict_: dict, key: str) -> None:
    if key in dict_:
        if isinstance(dict_[key], datetime.datetime):
            raise TypeError("the type of this value must be datetime.datetime")
        iso_time = dict_[key]
        del dict_[key]
        dict_[key]=(int)iso_time.replace(tzinfo=timezone.utc).timestamp()


def load_tasks_from_toml(database: Database, toml_files: list[str]) -> None:
    """toml filesから、tasks tableの情報を読み込む
    """
    # toml filesを一括して読み込む
    temp = toml.load(toml_files)

    # tasksが一つもなかったら中断する
    if "tasks" in temp:
        return

    # tableが存在しなかったら作成する
    database.create("tasks", ["task_id integer primary key autoincrement",
                              "summary text not null",
                              "description text default null",
                              "length integer default null",
                              "deadline integer default null",
                              "is_completed integer check(is_completed in (0,1)) default 0",
                              "status text check(status in ('active','archived')) default 'archived'",
                              "priority integer default null",
                              "location text default null",
                              "created_at integer not null",
                              "updated_at integer not null"])
    database.create("tasks_tagging", [
                    "task_id integer not null", "tag_id integer not null"])

    # タグの情報を追加する
    for task in temp["tasks"]:
        for tag_id in task["tag_ids"]:
            database.insert("tags",{"task_id":task["task_id"],"tag_id":tag_id})

    # タスクを登録する
    for task in temp["tasks"]:
        # deadline,created_at,updated_at に関しては、ISO 8601 からUNIX time(UTC)に変換する
        replace_unix_time(task,"deadline")
        replace_unix_time(task,"created_at")
        replace_unix_time(task,"updated_at")

        if database.exists("task", f"task_id={task['task_id']}"):
            # すでに登録されている場合は上書きする
            database.update(
                "task", {key: value for key, value in task.items() if key != "task_id"}, f"task_id={task['task_id']}")
        else:
            database.insert("task",task)

    pass


def load_toml(cursor: sqlite3.Cursor):
    """toml filesからデータベースを構築する


    """
    pass


def temporary_func(args: argparse.Namespace) -> None:
    toml_path = pathlib.Path(args.toml_path).resolve()  # 絶対パスに変換する
    db_path = pathlib.Path(args.db_path).resolve()  # 絶対パスに変換する
    print(f"the target file: {toml_path}")
    print(f"the database file: {db_path}")
    target = toml.load(toml_path)
    # idが設定されていない要素があったら、新しく割り当てる
    is_changed = False
    for i in target["problems"]:
        if not "id" in i:
            i["id"] = str(uuid.uuid4())
            is_changed = is_changed | True

    # -make_word_id optionがある時
    # - problemsの各要素が"cf.w.xx"を値に持つreferenceを持っていたら、その要素を別のtableに定義し直す
    # - 他の処理は行わない
    if args.make_word_id:
        for i in target["problems"]:
            if "reference" in i:
                number = int(i["reference"].split(".")[2])
                del i["reference"]
                target["word-id"].append(
                    {"id": i["id"], "reference-id": "c70bd010-db8e-4d37-8f5c-f7832a618e15", "number": number})
                print(f"id={i['id']}\nnumber={number}")
        # encoder=toml.TomlPreserveCommentEncoder()を指定してもコメントは消えてしまう
        toml.dump(target, open(toml_path, "w"))
        sys.exit(0)

    if is_changed:
        toml.dump(target, open(toml_path, "w"))

    with closing(sqlite3.connect(db_path)) as problem_data:
        cursor = problem_data.cursor()

        # 同名のテーブルがあったら、削除して作り直す
        # データはすべてtomlで管理し、RDBはただの自動生成ファイルとみなす。なのでRDBは消して問題ない
        reset_table(cursor, "problems",
                    "id text primary key unique not null,question text,answer text")
        reset_table(cursor, "word_id",
                    "id text not null,reference_id not null,number integer, primary key(mportより前に記載するid,reference_id)")

        print("writing data...", end="")

        # tomlファイルから書き込むデータを作成する
        # referenceはnullでも良い
        problems = [(str(uuid.uuid4()), i["answer"][0], i["question"])
                    for i in target["problems"]]
        word_id = [(i["id"], i["reference-id"], i["number"])
                   for i in target["word-id"]]

        # database に書き込む
        insert(cursor, "problems", problems)
        insert(cursor, "word_id", word_id)
        print("done")

        # 変更を保存する
        problem_data.commit()
    print("Successfully finished!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "toml_path", help="the target toml file which you covert to SQLite3 database")
    parser.add_argument(
        "db_path", help="the output SQLite3 database")
    parser.add_argument(
        "-M", "--make_word_id", help="delete problems.reference and make word-id", action="store_true")
    args = parser.parse_args()
    temporary_func(args)
