import uuid
from typing import Annotated

from fastapi import Path, HTTPException, Depends
from sqlalchemy import select, Select
from sqlalchemy.ext.asyncio import AsyncSession

from src.crud import user_crud
from src.dependencies.session_dependency import session_dep

from src.models.user_model import User


async def get_user_stmt(criteria):
    return select(User).where(criteria)


async def return_user_or_404(stmt: Select, session: AsyncSession):
    user = await session.scalar(stmt)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def user_by_id(user_id: uuid.UUID,
                     session: session_dep, ) -> User:
    stmt = await get_user_stmt(User.id == user_id)
    return await return_user_or_404(stmt=stmt, session=session)


async def user_by_name(user_name: str,
                       session: session_dep, ) -> User:
    stmt = await get_user_stmt(User.name == user_name)
    return await return_user_or_404(stmt=stmt, session=session)


get_by_id_dep = Annotated[User, Depends(user_by_id)]
get_by_name = Annotated[User, Depends(user_by_name)]
