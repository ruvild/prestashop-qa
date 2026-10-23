from pydantic import BaseModel, EmailStr
from typing import List, Literal


class CustomerRegistrationUI(BaseModel):

    first_name: str
    last_name: str
    email: str
    password: str
    birthdate: str = ""


class CustomerSearchResponse(BaseModel):
    idCustomer: int
    firstname: str
    lastname: str
    email: EmailStr
    fullnameAndEmail: str
    active: int
    company: str | None = None
    idDefaultGroup: int
    groups: dict


class CustomerCreateRequest(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    defaultGroupId: int
    groupIds: List[int]
    genderId: int | None = None
    newsletterSubscribed: bool = False
    partnerOffersSubscribed: bool = False
    birthday: str | None = None
    companyName: str | None = None
    siretCode: str | None = None
    apeCode: str | None = None
    website: str | None = None
    allowedOutstandingAmount: float | None = None
    maxPaymentDays: int | None = None
    riskId: int | None = None


class CustomerCreateResponse(BaseModel):
    customerId: int
    firstName: str
    lastName: str
    email: EmailStr
    defaultGroupId: int
    groupIds: List[int]
    genderId: Literal[0, 1, 2]
    enabled: bool
    newsletterSubscribed: bool
    partnerOffersSubscribed: bool
    birthday: str | None
    companyName: str | None
    siretCode: str | None
    apeCode: str | None
    website: str | None
    allowedOutstandingAmount: float
    maxPaymentDays: int
    riskId: int
    guest: bool
