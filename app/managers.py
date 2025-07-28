import sqlite3
from typing import List
from models import Actor


class ActorManager:
    def __init__(self, db_name: str, table_name: str = "actors") -> None:
        self.db_name = db_name
        self.table_name = table_name
        self._create_table()

    def _create_table(self) -> None:
        """Create the actors table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.table_name} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    first_name TEXT NOT NULL,
                    last_name TEXT NOT NULL)""")
            conn.commit()

    def create(self, first_name: str, last_name: str) -> Actor:
        """Create a new actor in the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"INSERT INTO {self.table_name} (first_name, last_name) "
                f"VALUES (?, ?)",
                (first_name, last_name)
            )
            conn.commit()
            actor_id = cursor.lastrowid
            return Actor(
                id=actor_id, first_name=first_name, last_name=last_name
            )

    def all(self) -> List[Actor]:
        """Retrieve all actors from the database."""
        with sqlite3.connect(self.db_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(
                f"SELECT id, first_name, last_name FROM {self.table_name}"
            )
            rows = cursor.fetchall()
            return [
                Actor(
                    id=row["id"],
                    first_name=row["first_name"],
                    last_name=row["last_name"]
                ) for row in rows
            ]

    def update(self, pk: int, new_first_name: str, new_last_name: str) -> None:
        """Update an actor's information based on their primary key."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE {self.table_name} SET first_name = ?, last_name = ? "
                f"WHERE id = ?",
                (new_first_name, new_last_name, pk)
            )
            conn.commit()

    def delete(self, pk: int) -> None:
        """Delete an actor from the database based on their primary key."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {self.table_name} WHERE id = ?", (pk,)
            )
            conn.commit()
