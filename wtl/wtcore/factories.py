import factory
from django.contrib.auth.models import User


FACTORY_USER_PASSWORD = 'password'


class SuperuserFactory(factory.DjangoModelFactory):
    FACTORY_FOR = User

    username = factory.sequence(lambda n: 'root%i' % n)
    email = factory.sequence(lambda n: 'root%i@root.root' % n)
    password = FACTORY_USER_PASSWORD
    is_staff = True
    is_active = True
    is_superuser = True

    @classmethod
    def _prepare(cls, create, **kwargs):
        password = kwargs.pop('password', None)
        user = super(SuperuserFactory, cls)._prepare(create, **kwargs)
        if password:
            user.set_password(password)
            if create:
                user.save()
        return user
