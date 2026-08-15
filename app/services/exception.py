

class AppError(Exception):
    "Родительский класс для всех исключений"
    def __init__(self, message : str, context : dict = None):
        super().__init__(message)
        self.message = message 
        self.context = context or None
       


class UserAlreadyExistsEmailError(AppError):
    def __init__(self, email : str):
        self.msg = f"Email - {email} занят"
        self.ctx = {"entity" : "User", "field" : "email", "value" : email}
        super().__init__(self.msg)
        self.problem_email = email

