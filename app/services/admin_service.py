from app.repository import Repository
from app.services.exception import AccessError



class AdminPanel():
    def __init__(self, repository : Repository):
        self.repository = repository


    async def verify_admin(self, id : int) -> True:
        status = await self.repository.get_status_user(id)
        if status != True:
            raise AccessError
        return status

    async def get_all_users(self, ) -> list[dict]:
        all_users = await self.repository.get_all_users()
        return all_users

