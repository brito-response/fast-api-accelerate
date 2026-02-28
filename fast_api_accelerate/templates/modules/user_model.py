def user_model_template()-> str:
    return """from sqlalchemy import String, Integer, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.configs import settings
from sqlalchemy import Enum
from enum import Enum as PyEnum

class UserStatus(PyEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"

class UserModel(settings.BaseDB):
    __tablename__ = "tb_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(String(100))
    imagem: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus),default=UserStatus.ACTIVE,nullable=False)

    # ARRAY no postgres funciona normal
    roles: Mapped[list[str] | None] = mapped_column(ARRAY(String), nullable=True)

    # NOVO: relacionamento 1:N com Comment
    comments: Mapped[list["CommentModel"]] = relationship("CommentModel", back_populates="user", cascade="all, delete-orphan")

    # NOVO: relacionamento 1:N com Post
    posts: Mapped[list["PostModel"]] = relationship("PostModel", back_populates="user", cascade="all, delete-orphan")

    def get_roles(self):
        return self.roles or []

    def set_roles(self, roles: list[str]):
        self.roles = roles
"""