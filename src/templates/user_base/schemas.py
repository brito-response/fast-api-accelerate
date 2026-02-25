user_schemas_template = lambda name:str :f"""
   from pydantic import BaseModel, EmailStr

    class RegisterDTO(BaseModel):
        email: EmailStr
        password: str


    class LoginDTO(BaseModel):
        email: EmailStr
        password: str


    class TokenResponseDTO(BaseModel):
        access_token: str
        refresh_token: str | None = None
        token_type: str = "bearer"

"""