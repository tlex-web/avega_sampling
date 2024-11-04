from models.Session import Session
from models.User import User
from library.Logger import log, LogEnvironment
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
        self.user_model = User()
        self.session_model = Session()

    def init_session(self):
        """
        Initializes a new session for a user.
        """

        user_data = self.user_model.read_user_username(SESSION_NAME)

        if user_data is not None:
            user_id = user_data["user_id"]

            # check if session exists
            session = self.session_model.get_session(user_id)

            if session is None:
                self.session_model.create_session(user_id)

                log.info(
                    f"Created session for user {user_id}", LogEnvironment.CONTROLLERS
                )

            else:
                log.info(
                    f"Continue session for user {user_id}", LogEnvironment.CONTROLLERS
                )

        else:
            user_id = self.user_model.create_user(SESSION_NAME)

            if user_id is not None:
                self.session_model.create_session(user_id)

                log.info(
                    f"Created session for user {user_id}", LogEnvironment.CONTROLLERS
                )
            else:
                log.error("Failed to create user session", LogEnvironment.CONTROLLERS)
                raise Exception("Failed to create user session")
