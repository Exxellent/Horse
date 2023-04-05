from flask_login import current_user

class UsersPolicy:
    def __init__(self):
        pass

    def create(self):
        return current_user.is_admin

    def delete(self):
        return current_user.is_admin

    def update(self):
        return current_user.is_admin or current_user.is_moder
    
    def check_collections(self):
        return current_user.is_user