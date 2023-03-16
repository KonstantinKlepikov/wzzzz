class UserNotExistError(ValueError):
    """User not exist.
    """
    def __init__(self, user_id: int) -> None:
        self.message = f'User with {user_id} not exist.'
        super().__init__(self.message)


class UserExistError(ValueError):
    """User exist.
    """
    def __init__(self, user_id: int) -> None:
        self.message = f'User with {user_id} exist and cant be created.'
        super().__init__(self.message)
