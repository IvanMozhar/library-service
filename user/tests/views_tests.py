from django.contrib.auth import get_user_model
from django.test import TestCase, RequestFactory
from rest_framework.test import force_authenticate

from user.views import ManageUserView

User = get_user_model()


class ManageUserViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="password"
        )
        self.view = ManageUserView.as_view()
        self.factory = RequestFactory()

    def test_get_object_authenticated(self):
        """Test that authenticated user can retrieve their profile"""
        request = self.factory.get("/fake-url")
        force_authenticate(request, user=self.user)

        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user.email)

    def test_get_object_unauthenticated(self):
        """Test that unauthenticated request is not allowed"""
        request = self.factory.get("/fake-url")

        response = self.view(request)

        self.assertEqual(response.status_code, 401)
