from django.contrib.auth import get_user_model
import factory
from core.utils import cryptosecure_string_generator
from .models import Client


class UserFactory(factory.DjangoModelFactory):
    """ Factory that allows us to create users in all of our tests.

    This class also enables adding a group to the users created.

    Attributes:
    -----------
    username : faker.fake.user_name
        Randomly generated username for our new user.
    first_name : faker.fake.first_name
        Randomly generated name for our new user.
    last_name : faker.fake.last_name
        Randomly generated naem for our new user.
    email : faker.fake.safe_email
        Randomly generated email address for our new user.
    passwords : string
        Randomly generated cryptosecure password for the new user.
    """
    class Meta:
        model = get_user_model()

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('safe_email')
    password = cryptosecure_string_generator()

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if create and extracted:
            # A list of groups were passed in, use them
            for group in extracted:
                self.groups.add(group)


class ClientFactory(factory.DjangoModelFactory):
    """ Factory that creates a new client along side a newly created
    user.

    Attributes:
    ----------
    user : django.contrib.auth.models.User
        The django User related to Client (i.e. contains the actual user information).
    activo : BooleanField
        Indicates whether the profile is active or not.
    """
    class Meta:
        model = Client

    user = factory.SubFactory(UserFactory)
    active = True
    commercial_contact_name = factory.Faker('name')
    commercial_contact_email = factory.Faker('safe_email')
    commercial_contact_phone = '9321434862'
    legal_business_name = factory.Faker('company')
    rfc = 'JAMP2504053G0'
    billing_address = factory.Faker('address')
    billing_email = factory.Faker('safe_email')
    billing_phone = '9321434862'
    finance_contact_name = factory.Faker('name')
    finance_contact_email = factory.Faker('safe_email')
    logistics_contact_name = factory.Faker('name')
    logistics_contact_email = factory.Faker('safe_email')
    billing_conditions = ''
    ecommerce_platform = Client.CHOICE_MAGENTO
