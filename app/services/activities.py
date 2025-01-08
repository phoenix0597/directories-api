from app.repositories.activities import ActivityRepository
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Set


class ActivityService:
    def __init__(self, session: AsyncSession):
        self.repository = ActivityRepository(session)

    async def get_activity_tree(self, activity_id: int) -> Set[int]:
        """Get all activity IDs in the tree, including the parent"""
        activity = await self.repository.get_tree_by_id(activity_id)
        if not activity:
            return set()

        activity_ids = {activity.id}

        async def collect_children(node):
            for child in node.children:
                activity_ids.add(child.id)
                await collect_children(child)

        await collect_children(activity)
        return activity_ids
