def init_dtos_template() -> str:
    return """
from .login import LoginRequest\n
from .refresh import RefreshTokenResponse\n
from .token import TokenResponse\n
from .refreshrequest import RefreshRequest\n\n
__all__ = ['LoginRequest','RefreshTokenResponse','TokenResponse','RefreshRequest']
"""