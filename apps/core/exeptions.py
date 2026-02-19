from fastapi import HTTPException, status


class MissingEnvVar(Exception):
    """Исключение, выбрасываемое, если в .env отсутствует обязательная переменная."""

    pass


class ObjectDoesntExist(HTTPException):
    """Исключение, выбрасываемое, если в модели отсутствует объект."""

    def __init__(
        self,
        model_name: str,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Объект таблицы {model_name} не найден',
        )


class PermissionDenied(HTTPException):
    """Исключение, выбрасываемое если права доступа пользователя ниже разрешений АПИ."""

    def __init__(
        self,
        detail_text: str = None,
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f'Недостаточно прав для совершения данной операции. {detail_text}',
        )


class UniqueViolationError(HTTPException):
    """Исключение, выбрасываемое при нарушении уникальности свойств БД."""

    def __init__(self, field: str = None):
        detail = (
            f'Поле {field} должно быть уникальным'
            if field
            else 'Нарушено ограничение уникальности'
        )
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class ForeignKeyViolationError(HTTPException):
    """Исключение, выбрасываемое при нарушении ограничения внешнего ключа."""

    def __init__(self, field: str = None):
        detail = (
            f'Ссылка на объект через поле {field} не существует'
            if field
            else 'Нарушено ограничение внешнего ключа'
        )
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
