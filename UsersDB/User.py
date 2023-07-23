class User:
    user_id = None

    def __init__(self, user_id):
        self.user_id = user_id

    def __str__(self):
        return f"Id: {self.user_id}"
