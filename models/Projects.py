from PyQt6.QtSql import QSqlQuery


class Project:
    """
    Represents a project in the database.
    """

    def create_project(
        self,
        project_name: str,
        user_id: int,
        seed: int,
        lower_bound: int,
        upper_bound: int,
        n: int,
        n_groups: int,
        generated_sequence: str,
    ) -> bool:
        """Create a new project in the database

        Args:
            project_name (str): Project name
            user_id (int): User id
            seed (int): Seed value
            lower_bound (int): Lower bound
            upper_bound (int): Upper bound
            n (int): Number of elements
            n_groups (int): Number of groups
            generated_sequence (str): Generated sequence

        Returns:
            bool: True if the project is created successfully, False otherwise.
        """

        query = QSqlQuery()
        query.prepare(
            "INSERT INTO projects (project_name, user_id, seed, lower_bound, upper_bound, n, n_groups, generated_sequence) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
        )
        query.addBindValue(project_name)
        query.addBindValue(user_id)
        query.addBindValue(seed)
        query.addBindValue(lower_bound)
        query.addBindValue(upper_bound)
        query.addBindValue(n)
        query.addBindValue(n_groups)
        query.addBindValue(generated_sequence)

        return query.exec()

    def update_project(self, name: str, project_id: int, user_id: int) -> bool:
        """Update a project in the database

        Args:
            name (str): New project name
            project_id (int): Project id
            user_id (int): User id

        Returns:
            bool: True if the project is updated successfully, False otherwise.
        """

        query = QSqlQuery()
        query.prepare(
            "UPDATE projects SET project_name = ? WHERE project_id = ? AND user_id = ?"
        )
        query.addBindValue(name)
        query.addBindValue(project_id)
        query.addBindValue(user_id)

        return query.exec()

    def delete_project(self, project_id: int) -> bool:
        """Delete a project from the database

        Args:
            project_id (int): Project id

        Returns:
            bool: True if the project is deleted successfully, False otherwise.
        """

        query = QSqlQuery()
        query.prepare("DELETE FROM projects WHERE project_id = ?")
        query.addBindValue(project_id)

        return query.exec()

    def get_project(self, project_id: int) -> dict | None:
        """Get a project from the database

        Args:
            project_id (int): Project id

        Returns:
            dict | None: A dictionary representing the project if found, None otherwise.
        """

        query = QSqlQuery()
        query.prepare("SELECT * FROM projects WHERE project_id = ?")
        query.addBindValue(project_id)
        query.exec()

        if query.next():

            return {
                "project_id": query.value("project_id"),
                "project_name": query.value("project_name"),
                "user_id": query.value("user_id"),
            }

        return None
