from faker import Faker
from models.customer import CustomerRegistrationUI
from schemas.customer_schemas import CustomerCreateRequest
import random

fake = Faker()


class CustomerFactory:
    @staticmethod
    def create_required_ui() -> CustomerRegistrationUI:
        return CustomerRegistrationUI(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.safe_email(),
            password=fake.password(length=12),
        )

    @staticmethod
    def create_full_ui() -> CustomerRegistrationUI:
        customer = CustomerFactory.create_required_ui()
        customer.birthdate = fake.date_of_birth(
            minimum_age=18, maximum_age=100
        ).strftime("%m/%d/%Y")
        return customer

    @staticmethod
    def create_required_api() -> CustomerCreateRequest:
        return CustomerCreateRequest(
            firstName=fake.first_name(),
            lastName=fake.last_name(),
            email=fake.safe_email(),
            password=fake.password(length=12),
            defaultGroupId=3,
            groupIds=[3],
        )

    @staticmethod
    def create_full_api() -> CustomerCreateRequest:
        customer = CustomerFactory.create_required_api()
        customer.groupIds = [1, 2, 3]
        customer.genderId = 1
        customer.newsletterSubscribed = True
        customer.partnerOffersSubscribed = True
        customer.birthday = fake.date_of_birth(
            minimum_age=18, maximum_age=100
        ).isoformat()
        customer.companyName = fake.company()
        customer.siretCode = fake.numerify("############")
        customer.apeCode = fake.bothify("####?")
        customer.website = fake.url()
        customer.allowedOutstandingAmount = round(random.uniform(0, 100), 2)
        customer.maxPaymentDays = random.randint(1, 100)
        customer.riskId = random.randint(1, 100)
        return customer
