# workload management (server side)


# 概要

## 本アプリについて
workload managementはプロジェクトの工数管理を行うためのアプリケーションです。各担当者が、タスクレベルでの工数を日毎に記録できるアプリケーションです。  
このリポジトリではサーバ部分を実装します。

## 本アプリを用いて実現したいこと
- 期間(月,クォータ等)で工数を見える化し、管理,編集コストを低減させる。
  - 各人の工数を見える化する
  - プロジェクト単位で工数を見える化する

## 使用技術 (現時点で使用予定のものを記載)
### サーバ
![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.5-blue)
![Pytest](https://img.shields.io/badge/Pytest-8.3.3-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.36-blue)

### DataBase
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.8-blue)


## ディレクトリ構成
ディレクトリ構成は下記になります。

```text
./
├── app/                     # "app" is a Python package
│   ├── __init__.py
│   ├── api/                 # "routers" is a "Python subpackage"
│   │   ├── __init__.py
│   │   ├── current/         # api version 1
│   │   │   ├── __init__.py  # makes "routers" a "Python subpackage"
│   │   │   ├── users.py     # "users" submodule
│   │   │   ├── issues.py    # "issues" submodule
│   │   │   └── workloads.py # "workloads" submodule
│   │   └── vXX/             # api version XX
│   │       └── ...
│   ├── services/            # [TODO] common method in this project
│   │   ├── __init__.py
│   │   ├── common1.py       # [TODO]
│   │   └── ...              # [TODO]
│   ├── models/              # Pydantic models (types)
│   │   ├── __init__.py
│   │   ├── users.py         # user types
│   │   ├── jira_types.py    # jira issue types
│   │   └── workloads.py     # workload types
│   ├── db/                  # Pydantic models (types)
│   │   ├── __init__.py
│   │   ├── migration/       # For migration files (alembic)
│   │   │   ├── env.py
│   │   │   ├── README
│   │   │   ├── script.py.mako
│   │   │   └── versions/
│   │   │       └── ... ...
│   │   └── models/          # DB models
│   │       ├── users.py     # user table definition
│   │       ├── projects.py  # project table definition
│   │       ├── issues.py    # issues table definition
│   │       ├── subtasks.py  # subtask table definition
│   │       └── workloads.py # workload table definition
│   ├── config.py
│   └── main.py              # "main" module
├── .env                     # environment file
├── alembic.ini              # alembic setting file
├── README.md
├── DATABASE.md              # Database table
└── DATABASE_ER_DIAGRAM.dio  # DR diagram
```

### 環境設定ファイル .env
```text
# FastAPIのホスト情報
FAST_API_HOST="0.0.0.0"
# シークレットキー
SECRET_KEY_FOR_JWT_TOKEN="secret key for jwt"
SECRET_KEY_FOR_CSRF_TOKEN="secret key for csrf token"
# DB
DB_PROTOCOL="postgresql+psycopg2"
WORKLOAD_SECRET_KEY='YOUR_OWN_RANDOM_GENERATED_SECRET_KEY'
WORKLOAD_DB_NAME='workload_app_db'
WORKLOAD_DB_HOST='your db host'
WORKLOAD_DB_PORT='your db port'
WORKLOAD_DB_USER_NAME='your db role name'
WORKLOAD_DB_USER_PASS='your db role password'
WORKLOAD_DATABASE_URI='${DB_PROTOCOL}://${WORKLOAD_DB_USER_NAME}:${WORKLOAD_DB_USER_PASS}@${WORKLOAD_DB_HOST}:${WORKLOAD_DB_PORT}/${WORKLOAD_DB_NAME}'
# jira fundamental information
JIRA_URL="your jira url"
JIRA_WORKLOAD_API_TOKEN="your jira api token"
JIRA_MANAGER_EMAIL="your email address"
# WORKLOAD APP
WORKLOAD_APP_ROOT_USER_EMAIL="your email address"
```


# 環境構築

## DB作成
```bash
$ createdb -U {WORKLOAD_APP_USER} --owner={WORKLOAD_APP_USER} --encoding=utf8 --locale=ja_JP.UTF-8 --template=template0 workload_app_db
```

## Python環境
```bash
$ cd /path/to/project_dir/
$ pip install -r requirements.txt
```

## migrate
```bash
$ alembic revision --autogenerate
$ alembic upgrade head
```


```bash
$ alembic revision "create subtask_with_parent_path view"
```
上記で作成されたマイグレーションファイルにビュー作成用のコマンドを記載する。  
記載内容は、【db_design】内の【6bd6e0fcfde7_create_view_subtask_with_parent_path.py】と同様に記載すること。
```bash
$ alembic upgrade {作成されたrevisionバージョン}
```


# 利用に関して

## 日本語版
```text
本ソフトウェアは、私的利用に限り、無償で使用することができます。  
商用目的での使用、または商業的な価値を生む活動に使用する場合は、事前に開発者（[f-mio](https://github.com/f-mio)）の許可を得る必要があります。  
本ソフトウェアの改変や再配布は、開発者の許可を得た場合にのみ可能です。  

本ソフトウェアの使用により生じたいかなる損害や問題についても、開発者は一切の責任を負いません。
```

## English version
```text
This software may be used free of charge for personal use only.  
For any commercial use, or activities generating commercial value, prior permission must be obtained from the developer ([f-mio](https://github.com/f-mio)).  
Modification or redistribution of this software is permitted only with the developer's approval.  

The developer assumes no responsibility for any damages or issues caused by the use of this software.
```
