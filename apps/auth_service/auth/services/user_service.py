from datetime import datetime
from typing import Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.auth_service.auth.models import User


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_user_by_uuid(self, user_uuid: str) -> Optional[User]:
        """Get user by uuid using a direct query (handles composite primary key)."""
        result = await self.session.execute(
            select(User).where(User.uuid == user_uuid)
        )
        return result.unique().scalar_one_or_none()

    async def update_user_online_status(self, user_uuid: str, is_online: bool) -> Optional[User]:
        """Update user's online status"""
        user = await self._get_user_by_uuid(user_uuid)
        if user:
            user.is_online = is_online
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def update_user_last_activity(self, user_uuid: str, activity_date: datetime) -> Optional[User]:
        """Update user's last activity date"""
        user = await self._get_user_by_uuid(user_uuid)
        if user:
            user.last_activity_date = activity_date
            await self.session.commit()
            await self.session.refresh(user)
        return user

    async def handle_user_connected(self, user_uuid: str) -> None:
        """Handle user connection event - set is_online to True"""
        await self.update_user_online_status(user_uuid, True)

    async def handle_user_disconnected(self, user_uuid: str) -> None:
        """Handle user disconnection event - set is_online to False"""
        await self.update_user_online_status(user_uuid, False)

    async def handle_user_activity(self, user_uuid: str) -> None:
        """Handle user activity event - update last_activity_date to current UTC time"""
        await self.update_user_last_activity(user_uuid, datetime.utcnow())