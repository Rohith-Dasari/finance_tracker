import datetime
from typing import Optional
import jwt
from werkzeug.security import check_password_hash, generate_password_hash
from models.user import User
from models.credentials import Credentials
from repository.user_json_repo import UserJSONRepository


class AuthService:
    def __init__(
        self, repo: UserJSONRepository, secret: str, ttl_minutes: int = 60 * 24
    ):
        self.repo = repo
        self.secret = secret
        self.ttl_minutes = ttl_minutes

    def signup(self, username: str, password: str, phone: str) -> User:
        if self.repo.get_user(username):
            raise ValueError("User already exists")

        user = User(username, phone)
        password_hash = generate_password_hash(password)
        creds = Credentials(username, password_hash)
        self.repo.add_user(user, creds)
        return user

    def login(self, username: str, password: str) -> User:
        creds = self.repo.get_credentials(username)
        if not creds:
            raise ValueError("Invalid credentials")

        if not check_password_hash(creds.password, password):
            raise ValueError("Invalid credentials")

        return self.repo.get_user(username)

    def generate_token(self, user: User) -> str:
        payload = {
            "username": user.username,
            "exp": datetime.datetime.now(datetime.UTC)
            + datetime.timedelta(minutes=self.ttl_minutes),
            "iat": datetime.datetime.now(datetime.UTC),
        }
        return jwt.encode(payload, self.secret, algorithm="HS256")

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            return jwt.decode(token, self.secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
