from app.repository import Repository
from app.services.exception import AccessError, UserNotFound
from app.schemas.dto import RecordsUsers
from typing import Any




class AdminPanel():
    def __init__(self, repository : Repository):
        self.repository = repository


    async def verify_admin(self, id : int) -> True:
        status = await self.repository.get_status_user(id)
        if status != True:
            raise AccessError
        return status

    async def get_all_users(self, page : int, page_size : int) -> dict[str, Any]:
        offset = (page - 1) * page_size
        all_users = await self.repository.get_all_users(offset, page_size)
        return all_users

    async def get_user_admin_service(self, id : int) -> dict:
        user = await self.repository.get_user_by_id(id=id)
        if not user:
            raise UserNotFound
        return user

