

class AppError(Exception):
    """Базовая ошибка для всех исключений"""
    status_code = 500
    message = "Внутренняя ошибка сервера"
       


class UserAlreadyExistsEmailError(AppError):
    """Исключение такой пользователь уже существует"""
    status_code = 409
    message = "Пользователь с таким email. Уже существует"

class UserNotFound(AppError):
    status_code = 404
    message = "Пользователь с данным email не найден"


class TokenError(AppError):
    """Базовое исключение для токенов"""
    status_code = 401
    message = "Недействительный или истекший токен"


class JWTGenerationError(AppError):
    status_code = 500
    message = "Ошибка при генерации jwt токена"
    pass