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
from contextlib import closing


def insert(cursor, table_name, tuple_values):
    return cursor.executemany(f"insert into {table_name} values ({','.join(['?']*len(tuple_values[0]))})", tuple_values)

def reset_table(cursor, table_name, column_settings):
    print(f"creating table \"{table_name}\"...", end="")
    cursor.execute(f"drop table if exists {table_name}")
    cursor.execute(
        f"create table {table_name}({column_settings})")
    print("done.")

def temporary_func(args):
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

