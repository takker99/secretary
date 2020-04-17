# source directory

## descriptions

**Note**: 関係データベースの仕様は取りやめた。

- main.py
  - the start up script
  - All about command-line arguments are dealt with in this script
- ~~loader.py~~
  - ~~a script to load SQLite3 database~~
  - ~~toml形式でgit管理しているデータをsqlite3形式に変換する。~~
- model.py
  - ~~sqlite3 databseを管理するclassの実装~~

~~## toml<-->sqlite3の変換formatについて~~
~~

```toml
[[todo_list]]
todo_id=1
content=
```

~~

## 見送った機能

1. repeat機能
これがあると計画立てがかなり楽になるのだが、無限リストやタスク再生の処理の実装方法を構築できなかった。今後の課題とする。

