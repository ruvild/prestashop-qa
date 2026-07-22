from pydantic import BaseModel


class CustomerRegistrationUI(BaseModel):

    first_name: str
    last_name: str
    email: str
    password: str
    birthdate: str = ""
