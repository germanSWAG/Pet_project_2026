

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


class TokenError(AppError):
    """Базовое исключение для токенов"""
    pass

class TokenExpiredError(TokenError):
    """Срок действия токена истек"""
    pass

class TokenInvalidError(TokenError):
    """Токен подделан или некорректен"""
    pass


class ServiceAuthError(AppError):
    """Ошибка сервиса по работе с пользователем"""

class JWTGenerationError(AppError):
    """Ошибка при генерации jwt токена"""
    pass