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
import datetime


def temporary_func(args):
    pass

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
