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
![FastAPI](https://img.shields.io/badge/FastAPI-XX.X-blue)
![Pytest](https://img.shields.io/badge/Pytest-XX.X-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-XX.X-blue)

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
│   │   ├── models/          # DB models
│   │   │   ├── users.py     # user table definition
│   │   │   ├── projects.py  # project table definition
│   │   │   ├── issues.py    # issues table definition
│   │   │   ├── subtasks.py  # subtask table definition
│   │   │   └── workloads.py # workload table definition
│   │   └── database.py      # workload table definition
│   ├── config.py
│   └── main.py              # "main" module
├── alembic.ini              # alembic setting file
├── README.md
├── DATABASE.md              # Database table
└── DATABASE_ER_DIAGRAM.dio  # DR diagram
```

.env
```text
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
