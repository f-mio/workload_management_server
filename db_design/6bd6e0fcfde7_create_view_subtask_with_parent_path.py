"""create view subtask_with_parent_path

Revision ID: 6bd6e0fcfde7
Revises: b93beea1ba37
Create Date: 2025-01-22 21:35:01.545756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.db.migrations.operations.base import create_view, drop_view
from app.db.migrations.operations.views import ReplaceableObject


# revision identifiers, used by Alembic.
revision: str = '6bd6e0fcfde7'
down_revision: Union[str, None] = 'b93beea1ba37'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


SUBTASK_VIEW_TEXT: str = """
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
;
"""

subtask_view = ReplaceableObject(
    "subtask_with_parent_path",
    SUBTASK_VIEW_TEXT
)

def upgrade() -> None:
    op.create_view(subtask_view)


def downgrade() -> None:
    op.drop_view(subtask_view)
