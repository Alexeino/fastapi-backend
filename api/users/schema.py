from pydantic import BaseModel, Field, EmailStr, SecretStr
import enum


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    CUSTOMER = "CUSTOMER"


class AccountType(enum.Enum):
    RECRUITER = "RECRUITER"
    CANDIDATE = "CANDIDATE"
    MANAGEMENT = "MANAGEMENT"
    CORPORATE = "CORPORATE"


class UserRegisterationRequest(BaseModel):
    name: str = Field(min_length=2)
    username: str = Field(min_length=3)
    email: EmailStr = Field(min_length=3)
    role: UserRole = Field(default=UserRole.CUSTOMER)
    account_type: AccountType = Field(default=AccountType.RECRUITER)
    password: SecretStr


class UserResponse(BaseModel):
    name: str
    username: str
    email: EmailStr
    role: UserRole
    account_type: AccountType


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")
