-- プロジェクトテーブル
CREATE TABLE project (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    jira_key VARCHAR(30),
    description TEXT,
    status VARCHAR(10) NOT NULL,
    start_date DATE,
    limit_date DATE,
    update_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 課題テーブル
CREATE TABLE issue (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    project_id BIGINT NOT NULL REFERENCES project(id),
    parent_issue_id BIGINT REFERENCES issue(id),
    type VARCHAR(10) NOT NULL,
    description TEXT,
    status VARCHAR(10),
    assignee VARCHAR(50),
    start_date DATE,
    limit_date DATE,
    update_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- サブタスクテーブル
CREATE TABLE subtask (
    id BIGSERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    issue_id BIGINT NOT NULL REFERENCES issue(id),
    status VARCHAR(10) NOT NULL,
    update_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ユーザーテーブル
CREATE TABLE "user" (
    id BIGSERIAL PRIMARY KEY,
    family_name VARCHAR(30) NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    update_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- プロジェクト-ユーザー中間テーブル
CREATE TABLE project_user (
    id BIGSERIAL PRIMARY KEY,
    project_id BIGINT NOT NULL REFERENCES project(id),
    user_id BIGINT NOT NULL REFERENCES "user"(id),
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(project_id, user_id)
);

-- 作業時間テーブル
CREATE TABLE work_time (
    id BIGSERIAL PRIMARY KEY,
    subtask_id BIGINT NOT NULL REFERENCES subtask(id),
    user_id BIGINT NOT NULL REFERENCES "user"(id),
    work_date DATE NOT NULL,
    workload_minute INTEGER NOT NULL,
    description TEXT,
    update_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    create_timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
