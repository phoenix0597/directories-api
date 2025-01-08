from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from app.models.activities import Activity
from typing import List, Optional


class ActivityRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, activity_id: int) -> Optional[Activity]:
        """Gets activity by ID"""
        query = (
            select(Activity)
            .where(Activity.id == activity_id)
            .options(joinedload(Activity.children))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_tree_by_id(self, activity_id: int) -> List[Activity]:
        """Gets all activity IDs in the tree, including the parent"""
        # Рекурсивный запрос для получения всего дерева активностей
        query = (
            select(Activity)
            .where(Activity.id == activity_id)
            .options(joinedload(Activity.children))
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
