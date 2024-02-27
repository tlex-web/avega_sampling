from PyQt6.QtSql import QSqlQuery


class Seed:
    """Represents a seed in the database."""

    def create_seed(self, seed_value: str, project_id: int) -> bool:
        """Create a new seed in the database.

        Args:
            seed_value (str): Seed value.
            project_id (int): Project id.

        Returns:
            bool: True if the seed is created successfully, False otherwise.
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO seeds (seed_value, project_id) VALUES (?, ?)")
        query.addBindValue(seed_value)
        query.addBindValue(project_id)

        return query.exec()

    def get_seed(self, seed_id: int) -> dict | None:
        """Get a seed from the database.

        Args:
            seed_id (int): Seed id.

        Returns:
            dict | None: A dictionary containing the seed information if found, None otherwise.
        """

        query = QSqlQuery()
        query.prepare("SELECT * FROM seeds WHERE seed_id = ?")
        query.addBindValue(seed_id)
        query.exec()

        if query.next():
            return {
                "id": query.value("id"),
                "seed_value": query.value("seed_value"),
                "project_id": query.value("project_id"),
            }

        return None
