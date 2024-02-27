from PyQt6.QtSql import QSqlQuery


class Project:
    """
    Represents a project in the database.
    """

    def create_project(self, name: str, user_id: int) -> bool:
        """Create a new project in the database

        Args:
            name (str): Name of the project
            user_id (int): User id

        Returns:
            bool: True if the project is created successfully, False otherwise.
        """

        query = QSqlQuery()
        query.prepare("INSERT INTO projects (project_name, user_id) VALUES (?, ?)")
        query.addBindValue(name)
        query.addBindValue(user_id)

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
