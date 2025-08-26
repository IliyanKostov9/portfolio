from django.test import TestCase, override_settings
from django.core.handlers.wsgi import WSGIRequest
from apps.landing_page.helpers.hash import hash


@override_settings(SECRET_KEY="dummy-key")
class ContactMeTestCase(TestCase):
    def test_post(self):
        expected_headers = """
        default-src 'self'; frame-ancestors 'self'; script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://unpkg.com; form-action 'self'; img-src 'self'; font-src https://fonts.gstatic.com https://cdnjs.cloudflare.com; style-src 'self' https://cdnjs.cloudflare.com https://fonts.googleapis.com 'sha256-47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=' 'sha256-3ITP0qhJJYBulKb1omgiT3qOK6k0iB3rMDhGfpM8b7c=' 'sha256-DqHyLrY03A99krj4zwj8j6M04dAkecX+/ck4dgG6zCk=' 'sha256-bsV5JivYxvGywDAZ22EZJKBFip65Ng9xoJVLbBg7bdo=' 'sha256-oxny43U4yMNZqsxffAINTdjzidFj6nAZr/6MrmG+WZA='
        """

        response: WSGIRequest = self.client.post(
            "/home/contact-me/",
            {
                "name": "dummy",
                "email": "dummy.dummy@mail.com",
                "message": "This is a dummy message by dummy from dummy",
            },
            follow=True,
        )

        self.assertEqual(
            hash(response.headers.get("Content-Security-Policy-Report-Only").strip()),
            hash(expected_headers),
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, "/")

        response: WSGIRequest = self.client.post(
            "/home/contact-me/",
            {
                "name": "dummy",
                "email": "This is invalid email",
                "message": "This is a dummy message by dummy from dummy",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 400)
