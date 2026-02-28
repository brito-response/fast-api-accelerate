def client_type_template()->str:
    return """from enum import Enum

class ClientType(str, Enum):
    WEB = "web"
    MOBILE = "mobile"

"""