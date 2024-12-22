

# 機能一覧

機能は大きく4つに分類される。
- ユーザ管理機能
- Jira情報の表示・同期機能
- 工数登録機能
- 可視化機能


## ユーザ管理機能
1. サインアップ機能
1. サインイン機能
1. ユーザ情報変更機能
1. ユーザ無効化機能
1. ユーザ削除機能


## Jira情報の表示・同期機能
1. (管理者のみ)APIユーザが取得可能なプロジェクト一覧の取得
1. 上記選択プロジェクトの表示機能
1. ターゲットプロジェクトの選択　(root userのみ)
1. ターゲットプロジェクトのJira - DB間の同期
    - DBに格納されていないprojectを登録する機能
    - DBに格納されており、Jira上で編集されたprojectを更新する機能
    - DBに格納されており、Jiraから消されたprojectをDB内で無効化する機能
1. ターゲットプロジェクト内issueとDBを同期させる機能　(ユーザ操作なし)
    - DBに格納されていないissueを登録する機能
    - DBに格納されており、Jira上で編集されたissueを更新する機能
    - DBに格納されており、ターゲットプロジェクト内に存在しないissueをDB内で無効化する機能
1. ターゲットプロジェクト内subtaskとDBを同期させる機能　(ユーザ操作なし)
    - DBに格納されていないsubtaskを登録する機能
    - DBに格納されており、Jira上で編集されたsubtaskを更新する機能
    - DBに格納されており、ターゲットプロジェクト内に存在しないsubtaskをDB内で無効化する機能


## 工数登録機能
1. サブタスクに紐づく日毎の工数や詳細(以下、工数情報)を登録する機能
1. 工数情報登録後の編集機能　(登録者と管理者以外は編集不可)
1. 工数情報登録後の削除機能　(登録者と管理者以外は削除不可)

## [PENDING] 可視化機能



# API一覧

| エンドポイント | メソッド | 内容 | JWT | CSRF token | remark |
| --- | :---: | --- | :---: | :---: | --- |
| /api/csrftoken | GET | CSRF Token発行 | ？ | ？ | - |
| /api/user/signup | POST | ユーザ登録 | ？ | ？ | - |
| /api/user/signin | POST | サインイン | O | O | - |
| /api/user/logout | POST | ログアウト | ？ | ？ | - |
| /api/user/deactivate/{user_id} | POST | ユーザ無効化 | ？ | ？ | - |
| /api/project/db/all | GET | 対象プロジェクトの取得 | ？ | ？ | - |
| /api/issue/main-task/db/all | GET | 対象プロジェクトのsubtask以外の全issue取得 | ？ | ？ | - |
| /api/issue/subtask/db/all | GET | 対象プロジェクトの全subtask取得 | ？ | ？ | - |
| /api/workload/db/get/{user_id} | GET | 特定ユーザの登録工数情報取得 | ？ | ？ | - |
| /api/workload/db/search/ | GET | JSONで渡した検索条件に合う登録工数情報の取得 | ？ | ？ | - |
| /api/workload/db/{workload_id} | GET | 登録工数情報の取得 | ？ | ？ | - |
| /api/workload/db/post | POST | 工数登録 | ？ | ？ | - |
| /api/workload/db/edit/{workload_id} | PUT | 登録工数の編集 | ？ | ？ | - |
| /api/user/delete/{user_id} | POST | ユーザ削除 (管理者機能) | ？ | ？ | - |
| /api/user/root/{user_id} | POST | ユーザへの管理者権限 (管理者機能) | ？ | ？ | - |
| /api/project/jira/all | GET | 全プロジェクト取得 (管理者機能) | ？ | ？ | APIユーザ権限内の全プロジェクト |
| /api/user/activate/{user_id} | POST | 無効ユーザの有効化 (管理者機能) | ？ | ？ | - |
| /api/project/db/update | PUT | 取得したJSON情報を元にプロジェクト登録もしくは更新 (管理者機能) | ？ | ？ | - |
| /api/project/db/update/all | GET | Jiraから有効プロジェクトのproject, issue, subtaskを全更新する | ？ | ？ | - |
<!-- | /api/issue/db/all | GET | 対象プロジェクトの全issue取得 | ？ | ？ | - | -->

