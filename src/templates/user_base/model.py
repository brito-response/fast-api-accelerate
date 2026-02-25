user_model_template = lambda name:str :f"""
    from sqlalchemy import Boolean, String
    from sqlalchemy.orm import Mapped, mapped_column
    from app.core.database import Base

    class User(Base):
        __tablename__ = "tb_users"

        id: Mapped[int] = mapped_column(primary_key=True, index=True)
        email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
        password_hash: Mapped[str] = mapped_column(String(255))
        is_active: Mapped[bool] = mapped_column(Boolean, default=True)
        role: Mapped[str] = mapped_column(String(50), default="user")

"""