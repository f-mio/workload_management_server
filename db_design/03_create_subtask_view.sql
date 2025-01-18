/*
  サブタスクにprojectと親のissue id情報を付与したview
*/
CREATE VIEW IF NOT EXISTS subtask_with_parent_path AS (
    WITH RECURSIVE subtask_with_path_raw AS (
        SELECT
            st.id,
            issue.parent_issue_id AS parent_issue_id,
            1 AS level,
            issue.id::TEXT || '>' || st.id::TEXT || '.' AS path
        FROM (
            SELECT id, name, parent_issue_id
            FROM issue
            WHERE issue.is_subtask = TRUE
        ) AS st
        JOIN (
            SELECT id, parent_issue_id
            FROM issue
            WHERE is_subtask =FALSE
        ) AS issue
        ON (issue.id = st.parent_issue_id)

        UNION ALL
        SELECT 
            st.id,
            issue.parent_issue_id AS parent_issue_id,
            st.level + 1 AS level,
            issue.id::TEXT || '>' || st.path AS path
        FROM subtask_with_path_raw AS st
        JOIN (
            SELECT id, parent_issue_id
            FROM issue
            WHERE is_subtask = FALSE
        ) AS issue
        ON ( issue.id = st.parent_issue_id )
    )

    SELECT
        st.*,
        '/' || st.project_id || '/' || st_path.path AS path
    FROM (
        SELECT *
        FROM issue
        WHERE is_subtask = TRUE
    ) AS st
    LEFT JOIN (
        SELECT DISTINCT ON (id)
            id,
            path
        FROM subtask_with_path_raw
        ORDER BY
            id,
            level DESC
    ) AS st_path
    ON st_path.id = st.id
);
