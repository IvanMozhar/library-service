from django.contrib.auth import get_user_model
from django.test import TestCase
from user.serializers import UserSerializer

User = get_user_model()


class TestUserSerializer(TestCase):

    def test_serialize_model(self):
        """Test serializing a user model"""
        user = User.objects.create_user(
            email="test@example.com", password="testpass123"
        )
        serializer = UserSerializer(user)

        data = serializer.data
        self.assertEqual(set(data.keys()), set(["id", "email", "is_staff"]))
        self.assertEqual(data["email"], user.email)
        self.assertFalse(data["is_staff"])

    def test_create_user_with_serializer(self):
        """Test creating a user with the serializer"""
        data = {"email": "testcreate@example.com", "password": "testpass"}
        serializer = UserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertTrue(User.objects.filter(email="testcreate@example.com").exists())
        self.assertTrue(user.check_password("testpass"))

    def test_update_user_with_serializer(self):
        """Test updating a user with the serializer"""
        user = User.objects.create_user(
            email="testupdate@example.com", password="oldpass"
        )
        serializer = UserSerializer(user, data={"password": "newpass123"}, partial=True)

        self.assertTrue(serializer.is_valid())
        updated_user = serializer.save()
        self.assertTrue(updated_user.check_password("newpass123"))

    def test_read_only_fields(self):
        """Test that read-only fields are handled correctly"""
        user = User.objects.create_user(
            email="readonlytest@example.com", password="testpass123", is_staff=True
        )
        data = {
            "email": "readonlytest@example.com",
            "is_staff": False,
        }
        serializer = UserSerializer(user, data=data, partial=True)
        self.assertTrue(serializer.is_valid())

        updated_user = serializer.save()
        self.assertTrue(updated_user.is_staff)
