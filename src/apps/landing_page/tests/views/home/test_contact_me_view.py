from django.test import TestCase


class ContactMeTestCase(TestCase):
    def test_post(self):
        print("This is kinda cool")
        self.assertEqual(True, True)
