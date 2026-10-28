from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.utils.password_utils import hash_password


class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def create_user(self, data: UserCreate, created_by: int) -> UserResponse:
        if self.repo.get_by_username(data.username):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already exists.")
        if self.repo.get_by_nic(data.nic):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="NIC already registered.")

        user = User(
            name=data.name,
            nic=data.nic,
            user_type=data.user_type,
            address=data.address,
            contact_number=data.contact_number,
            username=data.username,
            hashed_password=hash_password(data.password),
            remarks=data.remarks,
            created_by_user_id=created_by,
        )
        return UserResponse.model_validate(self.repo.create(user))

    def get_user(self, user_id: int) -> UserResponse:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        return UserResponse.model_validate(user)

    def list_users(self, skip: int = 0, limit: int = 100) -> list[UserResponse]:
        return [UserResponse.model_validate(u) for u in self.repo.get_all(skip, limit)]

    def update_user(self, user_id: int, data: UserUpdate) -> UserResponse:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(user, field, value)

        return UserResponse.model_validate(self.repo.update(user))

    def deactivate_user(self, user_id: int, requesting_user_id: int) -> UserResponse:
        if user_id == requesting_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot deactivate your own account.")
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
        user.is_active = False
        return UserResponse.model_validate(self.repo.update(user))
