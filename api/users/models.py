from db.base_model import Model
from sqlalchemy import Column, String, Integer, Enum, Boolean
from sqlalchemy.orm import Session
from .schema import UserRole, AccountType
from passlib.context import CryptContext
from api.users.schema import UserRegisterationRequest
from sqlalchemy import exc


class User(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(Enum(UserRole), nullable=False)
    account_type = Column(Enum(AccountType), nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


class UserManager:
    """A manager to handle creation of User for admin and non admin users"""

    context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def create_user(cls, user: UserRegisterationRequest, db: Session):
        try:
            db_user = User(
                name=user.name,
                username=user.username,
                email=user.email,
                role=user.role,
                account_type=user.account_type,
                hashed_password=cls.hash_password(user.password),
            )
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except exc.IntegrityError as e:
            db.rollback()
            raise e

    @staticmethod
    def hash_password(password):
        return UserManager.context.hash(password.get_secret_value())

    @staticmethod
    def verify_password(plain_pwd, hashed_pwd):
        return UserManager.context.verify(plain_pwd, hashed_pwd)
