#!/bin/zsh
createdb -U [WORKLOAD_APP_USER] --owner=[WORKLOAD_APP_USER] --encoding=utf8 --locale=ja_JP.UTF-8 --template=template0 workload_app_db
