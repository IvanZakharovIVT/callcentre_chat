from datetime import date
from typing import Any, Generic, Optional, Sequence, Type, TypeVar

from pydantic import BaseModel as BaseSchema
from sqlalchemy import BinaryExpression, Select, and_, delete, select, update
from sqlalchemy.exc import DBAPIError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from apps.core.exeptions import (
    ForeignKeyViolationError,
    ObjectDoesntExist,
    UniqueViolationError,
)
from apps.core.models import BaseDBModel

T = TypeVar('T', bound=BaseDBModel)
C = TypeVar('C', bound=BaseSchema)
U = TypeVar('U', bound=BaseSchema)


class BaseRepository(Generic[T, C, U]):
    """Базовый класс репозитория."""

    model: Type[T]
    pk_name: str = 'id'

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def _extract_unique_field_from_error(orig_error: Any) -> Optional[str]:
        """
        Извлекает имя поля, нарушившего уникальное ограничение, из сообщения ошибки.
        """
        detail: str = getattr(orig_error, 'detail', str(orig_error))
        if 'Key (' in detail:
            return detail.split('Key (')[1].split(')=')[0]
        return None

    @staticmethod
    def _extract_fk_field_from_error(orig_error: Any) -> Optional[str]:
        """
        Извлекает имя поля, связанного с нарушением внешнего ключа, из сообщения ошибки.
        """

        detail: str = getattr(orig_error, 'detail', str(orig_error))
        if 'Key (' in detail:
            return detail.split('Key (')[1].split(')=')[0]
        return None

    def _handle_integrity_error(self, error: IntegrityError) -> None:
        """
        Обрабатывает ошибки целостности базы данных (IntegrityError).

        Поддерживает asyncpg через анализ сообщения об ошибке.
        Определяет тип ошибки по содержимому строки и вызывает нужное исключение.
        """

        orig_error = error.orig

        if not orig_error:
            raise error

        error_class_name = orig_error.__class__.__name__
        error_message = str(orig_error)

        if (
            'UniqueViolationError' in error_class_name
            or 'unique constraint' in error_message.lower()
        ):
            field = self._extract_unique_field_from_error(orig_error)
            raise UniqueViolationError(field=field or 'unknown') from error

        elif 'ForeignKeyViolationError' in error_class_name or (
            'violates foreign key constraint' in error_message.lower()
        ):
            field = self._extract_fk_field_from_error(orig_error)
            raise ForeignKeyViolationError(field=field or 'district_id') from error

        raise error

    async def _save_or_handle_error(self) -> None:
        """Фиксирует транзакцию или обрабатывает возможные ошибки БД."""

        try:
            await self.session.flush()
        except IntegrityError as e:
            await self.session.rollback()
            self._handle_integrity_error(e)
        except DBAPIError:
            await self.session.rollback()
            raise

    @property
    def _base_query(self) -> Select:
        return select(self.model)

    def _filter_params(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        **kwargs,
    ) -> list[BinaryExpression | bool]:
        filters = []
        if start_date:
            filters.append(self.model.created_at >= start_date)
        if end_date:
            filters.append(self.model.created_at <= end_date)
        return filters

    @property
    def pk_column(self):
        """Возвращает колонку первичного ключа."""
        return getattr(self.model, self.pk_name)

    async def get_by_pk(self, model_pk: int | str) -> Optional[T]:
        """Получение объекта по его id."""

        stmt = self._base_query.where(self.model.id == model_pk)
        existed_object = await self.session.scalar(stmt)
        if not existed_object:
            raise ObjectDoesntExist(self.model.__name__)
        return existed_object

    async def get_all(self, **kwargs) -> Sequence[T]:
        """Возвращает список всех объектов."""

        stmt = self._base_query
        filters = self._filter_params(**kwargs)
        if filters:
            stmt = stmt.where(and_(*filters))
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def create(self, object_schema: C) -> T:
        """Создание объекта по его схеме."""

        db_obj = self.model(**object_schema.model_dump(serialize_as_any=True))
        self.session.add(db_obj)
        await self._save_or_handle_error()
        return db_obj

    async def bulk_create(self, schema_list: list[C]) -> list[T]:
        """Создание сразу нескольких объектов за одну транзакцию"""

        db_objects = [
            self.model(**object_schema.model_dump(serialize_as_any=True))
            for object_schema in schema_list
        ]
        self.session.add_all(db_objects)
        await self._save_or_handle_error()
        return db_objects

    async def bulk_update(self, schema_obj: U, **kwargs):
        stmt = update(self.model)
        filters = self._filter_params(**kwargs)
        if filters:
            stmt = stmt.where(and_(*filters))
        stmt = stmt.values(**schema_obj.model_dump(serialize_as_any=True))
        await self.session.execute(stmt)
        await self._save_or_handle_error()

    async def bulk_delete(self, **kwargs):
        stmt = delete(self.model)
        filters = self._filter_params(**kwargs)
        if filters:
            stmt = stmt.where(and_(*filters))
        await self.session.execute(stmt)
        await self._save_or_handle_error()

    async def update(self, object_pk: int | str, schema_obj: U) -> T:
        """Обновить объект по ID из Pydantic-схемы."""

        db_obj = await self.get_by_pk(object_pk)
        data = schema_obj.model_dump(serialize_as_any=True, exclude_unset=True)
        for key, value in data.items():
            setattr(db_obj, key, value)
        await self._save_or_handle_error()
        return db_obj

    async def delete(self, object_pk: int | str) -> None:
        """Удалить объект по ID."""

        db_obj = await self.get_by_pk(object_pk)
        await self.session.delete(db_obj)
        await self._save_or_handle_error()
