# データベース設計

## プロジェクト (project)

| カラム名 | 型 | 説明 |
|---|---|---|
| id | BIGINT | プライマリーキー |
| name | VARCHAR(100) | プロジェクト名 |
| jira_key | VARCHAR(30) | JIRAのプロジェクトキー |
| description | TEXT  | プロジェクトの説明 |
| status | VARCHAR(10) | プロジェクトのステータス |
| start_date | DATE | 開始日 |
| limit_date | DATE | 期限日 |
| update_timestamp | TIMESTAMP | 更新日時 |
| create_timestamp | TIMESTAMP | 作成日時 |


## 課題 (issue)

| カラム名 | 型 | 説明 |
|---|---|---|
| id | BIGINT | プライマリーキー |
| name | VARCHAR(100) | 課題名 (sumary) |
| project_id | BIGINT | プロジェクトID (FK) |
| parent_issue_id | BIGINT | 親課題ID (FK) |
| type | VARCHAR(10) | 課題タイプ |
| description | TEXT | 課題の説明 |
| status | VARCHAR(10) | 課題のステータス |
| assignee | VARCHAR(50) | 担当者ID (FK) |
| start_date | DATE | 開始日 |
| limit_date | DATE | 期限日 |
| update_timestamp | TIMESTAMP | 更新日時 |
| create_timestamp | TIMESTAMP | 作成日時 |


## サブタスク (subtask)
| カラム名 | 型 | 説明 |
|---|---|---|
| name | VARCHAR(100) | 課題名 (sumary) |
| issue_id | BIGINT | 課題ID (FK) |
| status | VARCHAR(10) | 課題のステータス |
| update_timestamp | TIMESTAMP | 更新日時 |
| create_timestamp | TIMESTAMP | 作成日時 |


## ユーザー (user)

| カラム名 | 型 | 説明 |
|---|---|---|
| id | BIGINT | プライマリーキー |
| family_name | VARCHAR(30) | ユーザー名(姓) |
| first_name | VARCHAR(30) | ユーザー名(名) |
| email | VARCHAR(100) | メールアドレス |
| password | VARCHAR(100) | ハッシュ化パスワード |
| update_timestamp | TIMESTAMP | 更新日時 |
| create_timestamp | TIMESTAMP | 作成日時 |


## プロジェクト-ユーザ中間テーブル (project_user)

| カラム名 | 型 | 説明 |
|---|---|---|
| id | BIGINT | プライマリーキー |
| project_id | BIGINT | プロジェクトID (FK) |
| user_id | BIGINT | ユーザーID (FK) |
| create_timestamp | TIMESTAMP | 作成日時 |


## 作業時間 (work_time)

| カラム名 | 型 | 説明 |
|---|---|---|
| id | BIGINT | プライマリーキー |
| subtask_id | BIGINT | 課題ID (FK) |
| user_id | BIGINT | ユーザーID (FK) |
| work_date | DATE | 作業日 |
| workload_minute | INTEGER | 作業時間(分) |
| description | TEXT | 作業内容 |
| update_timestamp | TIMESTAMP | 更新日時 |
| create_timestamp | TIMESTAMP | 作成日時 |
