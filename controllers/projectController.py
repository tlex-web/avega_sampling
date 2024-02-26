from models.Projects import Project


class ProjectController:
    def __init__(self, view):
        self.view = view
        self.model = Project()
        # Setup signals and slots for project-related actions
        self.view.add_project_signal.connect(self.add_project)
        self.view.update_project_signal.connect(self.update_project)
        self.view.delete_project_signal.connect(self.delete_project)

    def add_project(self, name, user_id):
        if self.model.create_project(name, user_id):
            self.view.show_message("Project added successfully")
        else:
            self.view.show_error("Failed to add project")

    def update_project(self, project_id, name, user_id):
        if self.model.update_project(project_id, name, user_id):
            self.view.show_message("Project updated successfully")
        else:
            self.view.show_error("Failed to update project")

    def delete_project(self, project_id):
        if self.model.delete_project(project_id):
            self.view.show_message("Project deleted successfully")
        else:
            self.view.show_error("Failed to delete project")
