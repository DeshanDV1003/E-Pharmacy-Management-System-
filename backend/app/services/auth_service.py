from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.audit_log import AuditLog
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import LoginRequest, TokenResponse, UserResponse
from app.utils.jwt_utils import create_access_token
from app.utils.password_utils import verify_password

MAX_FAILED_ATTEMPTS = 5


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
        self.db = db

    def login(self, request: LoginRequest, ip_address: str | None) -> TokenResponse:
        user = self.repo.get_by_username(request.username)

        if not user:
            self._log_failed_attempt(None, request.username, ip_address)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

        if not user.is_active:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is deactivated.")

        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account is temporarily locked.")

        if not verify_password(request.password, user.hashed_password):
            user.failed_login_attempts += 1
            if user.failed_login_attempts >= MAX_FAILED_ATTEMPTS:
                from datetime import timedelta
                user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
            self.repo.update(user)
            self._log_failed_attempt(user.id, request.username, ip_address)
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")

        user.failed_login_attempts = 0
        user.locked_until = None
        user.last_login_at = datetime.now(timezone.utc)
        self.repo.update(user)
        self._log_audit(user.id, "LOGIN", ip_address)

        token = create_access_token(subject=user.id, user_type=user.user_type.value)
        return TokenResponse(access_token=token, user=UserResponse.model_validate(user))

    def _log_failed_attempt(self, user_id: int | None, username: str, ip_address: str | None) -> None:
        log = AuditLog(
            user_id=user_id,
            action="LOGIN_FAILED",
            entity_type="user",
            entity_id=user_id,
            new_value={"username": username},
            ip_address=ip_address,
        )
        self.db.add(log)
        self.db.commit()

    def _log_audit(self, user_id: int, action: str, ip_address: str | None) -> None:
        log = AuditLog(
            user_id=user_id,
            action=action,
            entity_type="user",
            entity_id=user_id,
            ip_address=ip_address,
        )
        self.db.add(log)
        self.db.commit()
