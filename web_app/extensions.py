from repository.user_json_repo import UserJSONRepository
from service.auth_service import AuthService
from config import SECRET

user_repo = UserJSONRepository(path="user_data.json")
auth_service = AuthService(user_repo, secret=SECRET)
