from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Password:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        hashed_password = pwd_context.hash(plain_password)

        return hashed_password

    @staticmethod
    def is_password_valid(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
