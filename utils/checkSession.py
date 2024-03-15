from models.User import User


def check_session(session_name: str, user_model: User):
    """
    Checks if the session exists.
    """
    user_id = user_model.read_user_username(session_name)

    if user_id is not None:
        return True
    else:
        return False
