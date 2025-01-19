from __future__ import annotations

from typing import Protocol


class DatabaseConnection(Protocol):
    def commit(self) -> None:
        pass  # pragma: no cover

    def rollback(self) -> None:
        pass  # pragma: no cover

    def cursor(self) -> DatabaseCursor:
        pass  # pragma: no cover

    def execute(self, *args, **kwargs) -> None:
        pass  # pragma: no cover


class DatabaseCursor(Protocol):
    def execute(self, *args, **kwargs) -> None:
        pass  # pragma: no cover

    def fetchone(self, *args, **kwargs) -> tuple:
        pass  # pragma: no cover

    def fetchall(self, *args, **kwargs) -> tuple:
        pass  # pragma: no cover
