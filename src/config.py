import dataclasses
import pathlib

PROJECT_ROOT = pathlib.Path(__file__).parent.parent
SRC_ROOT = PROJECT_ROOT / "src"
MIGRATIONS_PATH = SRC_ROOT / "migrations"


@dataclasses.dataclass
class DBConfig:
    host: str
    port: int
    database: str
    user: str
    password: str

    @property
    def dsn(self) -> str:
        return " ".join(
            [
                f"host={self.host}",
                f"port={self.port}",
                f"dbname={self.database}",
                f"user={self.user}",
                f"password={self.password}",
            ]
        )
