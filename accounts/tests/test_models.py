from accounts.factories import UserFactory
from accounts.models import User
from companies.factories import CompanyFactory
from companies.models import CompanyOwner
from utils.testcases import BaseTestCase


class TestModels(BaseTestCase):
    def setUp(self):
        self.company = CompanyFactory()
        self.user = UserFactory(company=self.company)

    def test_overridden_save(self):
        user = UserFactory(email="Aaron@Spindlers.ca")
        self.assertEqual(user.email_root, "spindlers.ca")
        self.assertEqual(user.email_prefix, "aaron")

    def test_user_member_of_company_member(self):
        expected_result = True
        actual_result = self.user.is_member_of_company
        self.assertEqual(expected_result, actual_result)

    def test_user_member_of_company_owner(self):
        CompanyOwner.objects.create(company=self.company, owner=self.user)
        expected_result = True
        actual_result = self.user.is_member_of_company
        self.assertEqual(expected_result, actual_result)

    def test_user_member_of_company_no_member_or_owner(self):
        self.user.company = None
        self.user.save()
        expected_result = False
        actual_result = self.user.is_member_of_company
        self.assertEqual(expected_result, actual_result)

    def test_user_email_root(self):
        user = UserFactory(email="aaron@spindlers.ca")
        self.assertEqual(user.email_root, "spindlers.ca")

    def test_user_email_prefix(self):
        user = UserFactory(email="aaron@spindlers.ca")
        self.assertEqual(user.email_prefix, "aaron")

    def test_user_address_string(self):
        company = CompanyFactory()
        user = UserFactory(address_1="123 Main St", company=company)
        user_pk = user.pk

        self.assertEqual(user.address_string, "123 Main St")

        User.objects.filter(pk=user_pk).update(
            address_1=" 123 Main St   ", city="   Toronto ", company=company
        )
        self.assertEqual(
            User.objects.get(pk=user_pk).address_string, "123 Main St Toronto"
        )

        User.objects.filter(pk=user_pk).update(
            address_1=" 123 Main St   ",
            city="   Toronto ",
            prov_state="   ON ",
            company=company,
        )
        self.assertEqual(
            User.objects.get(pk=user_pk).address_string, "123 Main St Toronto ON"
        )

        User.objects.filter(pk=user_pk).update(
            address_1=" 123 Main St   ",
            city="   Toronto ",
            prov_state="   ON ",
            country="   Canada ",
            company=company,
        )
        self.assertEqual(
            User.objects.get(pk=user_pk).address_string, "123 Main St Toronto ON Canada"
        )

        User.objects.filter(pk=user_pk).update(
            address_1=" 123 Main St   ",
            city="   Toronto ",
            prov_state="   ON ",
            country="   Canada ",
            postal_code="   M1M 1M1 ",
            company=company,
        )
        self.assertEqual(
            User.objects.get(pk=user_pk).address_string,
            "123 Main St Toronto ON Canada M1M 1M1",
        )

    def test_user_geo_code_address(self):
        user = UserFactory(address_1="123 Main St", city="Toronto", country="Canada")
        lat, lng, place_id = user.geo_code_address()
        self.assertAlmostEquals(round(lat), 44, 1)
        self.assertAlmostEquals(round(lng), -79, 1)
        self.assertIsNotNone(place_id)

    def test_user_personality_type_name(self):
        user = UserFactory(personality_type="")
        self.assertEqual(user.personality_type_name(), "")
        user.personality_type = "INTJ"
        user.save()
        self.assertEqual(user.personality_type_name(), "Architect")
        user.personality_type = "INTP"
        user.save()
        self.assertEqual(user.personality_type_name(), "Logician")
        user.personality_type = "ENTJ"
        user.save()
        self.assertEqual(user.personality_type_name(), "Commander")
        user.personality_type = "ENTP"
        user.save()
        self.assertEqual(user.personality_type_name(), "Debater")
        user.personality_type = "INFJ"
        user.save()
        self.assertEqual(user.personality_type_name(), "Advocate")
        user.personality_type = "INFP"
        user.save()
        self.assertEqual(user.personality_type_name(), "Mediator")
        user.personality_type = "ENFJ"
        user.save()
        self.assertEqual(user.personality_type_name(), "Protagonist")
        user.personality_type = "ENFP"
        user.save()
        self.assertEqual(user.personality_type_name(), "Campaigner")
        user.personality_type = "ISTJ"
        user.save()
        self.assertEqual(user.personality_type_name(), "Logistician")
        user.personality_type = "ISFJ"
        user.save()
        self.assertEqual(user.personality_type_name(), "Defender")
        user.personality_type = "ESTJ"
        user.save()
        self.assertEqual(user.personality_type_name(), "Executive")
        user.personality_type = "ESFJ"
        user.save()
        self.assertEqual(user.personality_type_name(), "Consul")
        user.personality_type = "ISTP"
        user.save()
        self.assertEqual(user.personality_type_name(), "Virtuoso")
        user.personality_type = "ISFP"
        user.save()
        self.assertEqual(user.personality_type_name(), "Adventurer")
        user.personality_type = "ESTP"
        user.save()
        self.assertEqual(user.personality_type_name(), "Entrepreneur")
        user.personality_type = "ESFP"
        user.save()
        self.assertEqual(user.personality_type_name(), "Entertainer")

    def test_user_profile_completion_percentage(self):
        user = UserFactory()
        user.short_bio = None
        user.title = None
        user.save()
        self.assertEqual(user.profile_completion_percentage(), 32)
        user.title = "CEO"
        user.save()
        self.assertEqual(user.profile_completion_percentage(), 36)
        user.short_bio = "I am a CEO"
        user.save()
        self.assertEqual(user.profile_completion_percentage(), 40)
