import contextlib
import glob
import pathlib

from src.config import MIGRATIONS_PATH
from src.model import DatabaseConnection


def _execute_and_commit_files(
    conn: DatabaseConnection,
    files: list[str],
) -> None:
    for filepath in files:
        file = pathlib.Path(filepath)
        with contextlib.suppress(Exception):
            conn.execute(file.read_text(encoding="utf-8"))  # type: ignore
            conn.commit()


def migrate_up(conn: DatabaseConnection) -> None:
    up_files = sorted(
        glob.glob(str(MIGRATIONS_PATH / "*__up.sql")),
    )
    _execute_and_commit_files(conn, up_files)


def migrate_down(conn: DatabaseConnection) -> None:
    down_files = sorted(
        glob.glob(str(MIGRATIONS_PATH / "*__down.sql")),
        reverse=True,
    )
    _execute_and_commit_files(conn, down_files)
