import unittest
from app import app
from pymongo import MongoClient
from api.conf import MONGODB_DBNAME
from api.crypto_utils import encrypt


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.db = MongoClient().get_database(MONGODB_DBNAME)
        self.db.users.delete_many({})
        self.db.users.insert_one({
            "email": "user@test.com",
            "token": "token123",
            "expiresIn": 2147483647,
            "displayName": encrypt("Flask User"),
            "address": encrypt("1 Test Rd"),
            "phone": encrypt("0839998888"),
            "dateOfBirth": encrypt("1990-01-01"),
            "disabilities": encrypt("None")
        })

    def test_get_user_info(self):
        response = self.client.get(
            '/students/api/user',
            headers={
                "X-Token": "token123"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["displayName"], "Flask User")

    def test_user_without_token(self):
        response = self.client.get('/students/api/user')
        self.assertEqual(response.status_code, 400)
        self.assertIn("message", response.get_json())
        self.assertEqual(response.get_json()["message"], "Token missing!")

    def test_user_wrong_token(self):
        response = self.client.get(
            '/students/api/user',
            headers={
                "X-Token": "wrongtoken"})
        self.assertEqual(response.status_code, 403)
        self.assertIn("message", response.get_json())
        self.assertEqual(
            response.get_json()["message"],
            "Invalid or expired token!")
