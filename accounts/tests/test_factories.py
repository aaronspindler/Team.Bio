from accounts.factories import UserFactory
from accounts.models import User
from utils.testcases import BaseTestCase


class TestFactories(BaseTestCase):
    def test_user_factory(self):
        """
        User Factory
        """
        pre_count = User.objects.count()
        user = UserFactory()
        post_count = User.objects.count()
        self.assertGreater(post_count, pre_count)
        self.assertIsNotNone(user.first_name)
        self.assertIsNotNone(user.last_name)
        self.assertIsNotNone(user.username)
        self.assertIsNotNone(user.company)
        self.assertIsNotNone(user.email)
        self.assertIsNotNone(user.short_bio)
        self.assertIsNotNone(user.title)

    def test_multiple_users_creation(self):
        """
        Multiple User Creation
        """
        user = UserFactory()
        user2 = UserFactory()

        self.assertNotEqual(user, user2)
        self.assertNotEqual(user.username, user2.username)
        self.assertNotEqual(user.email, user2.email)
