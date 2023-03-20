from uuid import UUID
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.crud.base_crud import CRUDBase
from app.models.user_follow_model import UserFollow as UserFollowModel
from app.models.user_model import User
from app.schemas.user_follow_schema import IUserFollowCreate, IUserFollowUpdate


class CRUDUserFollow(CRUDBase[UserFollowModel, IUserFollowCreate, IUserFollowUpdate]):
    async def follow_a_user_by_target_user_id(
        self,
        *,
        user: User,
        target_user: User,
        db_session: AsyncSession | None = None,
    ) -> UserFollowModel:
        db_session = db_session or super().get_db().session
        new_user_follow = IUserFollowCreate(
            user_id=user.id, target_user_id=target_user.id
        )
        db_obj = UserFollowModel.from_orm(new_user_follow)

        reverse_follow = await self.get_follow_by_user_id_and_target_user_id(
            user_id=target_user.id, target_user_id=user.id
        )
        if reverse_follow:
            db_obj.is_mutual = True
            reverse_follow.is_mutual = True
            db_session.add(reverse_follow)
        db_session.add(db_obj)

        user.following_count += 1
        target_user.follower_count += 1

        db_session.add(user)
        db_session.add(target_user)
        await db_session.commit()
        await db_session.refresh(db_obj)
        return db_obj

    async def unfollow_a_user_by_id(
        self,
        *,
        user_follow_id: UUID,
        user: User,
        target_user: User,
        db_session: AsyncSession | None = None,
    ) -> UserFollowModel:
        db_session = db_session or super().get_db().session

        follow_user_obj = await self.get(id=user_follow_id)
        await db_session.delete(follow_user_obj)

        reverse_follow = await self.get_follow_by_user_id_and_target_user_id(
            user_id=target_user.id, target_user_id=user.id
        )
        if reverse_follow:
            reverse_follow.is_mutual = False
            db_session.add(reverse_follow)

        user.following_count -= 1
        target_user.follower_count -= 1

        db_session.add(user)
        db_session.add(target_user)
        await db_session.commit()
        return follow_user_obj

    async def get_follow_by_user_id(
        self, *, user_id: UUID, db_session: AsyncSession | None = None
    ) -> list[UserFollowModel] | None:
        db_session = db_session or super().get_db().session
        followed = await db_session.execute(
            select(UserFollowModel).where(UserFollowModel.user_id == user_id)
        )
        return followed.scalars().all()

    async def get_follow_by_target_user_id(
        self, *, target_user_id: UUID, db_session: AsyncSession | None = None
    ) -> list[UserFollowModel] | None:
        db_session = db_session or super().get_db().session
        followed = await db_session.execute(
            select(UserFollowModel).where(
                UserFollowModel.target_user_id == target_user_id
            )
        )
        return followed.scalars().all()

    async def get_follow_by_user_id_and_target_user_id(
        self,
        *,
        user_id: UUID,
        target_user_id: UUID,
        db_session: AsyncSession | None = None,
    ) -> UserFollowModel | None:
        db_session = db_session or super().get_db().session
        followed_user = await db_session.execute(
            select(UserFollowModel).where(
                and_(
                    UserFollowModel.user_id == user_id,
                    UserFollowModel.target_user_id == target_user_id,
                )
            )
        )
        return followed_user.scalar_one_or_none()


user_follow = CRUDUserFollow(UserFollowModel)
