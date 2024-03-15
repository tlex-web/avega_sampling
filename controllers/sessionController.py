from models.User import User
from utils.Logger import log, LogEnvironment
from config import SESSION_NAME

"""
Create an artificial user session by setting a random user id.
The user id is used to simulate a user session in order to correctly identify database transaction.
Since the application does not need to authenticate users and handle multi-user sessions,
the user id is randomly generated and used throughout the application.

The SessionController class could be extended to handle real user sessions and authentication in a future version of the application.
"""


class SessionController:
    def __init__(self) -> None:
        """
        Initializes the session controller.
        """
        self.model = User()

    def init_session(self):
        """
        Initializes a new session for a user.

        Returns:
            int: A random user id
        """

        user_id = self.model.create_user(SESSION_NAME)

        if user_id is None:
            log.error("Failed to start user session", LogEnvironment.CONTROLLERS)
            raise Exception("Failed to start user session")
        else:
            log.info(
                f"Started user session with id: {user_id}", LogEnvironment.CONTROLLERS
            )
