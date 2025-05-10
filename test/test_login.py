import unittest
import json
from app import app
from pymongo import MongoClient
from api.conf import MONGODB_DBNAME
from api.crypto_utils import hash_password


class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.db = MongoClient().get_database(MONGODB_DBNAME)
        self.db.users.delete_many({})

        self.email = "login@test.com"
        self.password = "correctpass"

        hashed, salt = hash_password(self.password)
        self.db.users.insert_one({
            "email": self.email,
            "password": hashed,
            "salt": salt,
            "displayName": "Test"
        })

    def test_create_account(self):
        user = self.db.users.find_one({"email": self.email})
        self.assertIsNotNone(user)
        self.assertIn("password", user)
        self.assertIn("salt", user)

    def test_login_success(self):
        payload = {
            "email": self.email,
            "password": self.password
        }
        response = self.client.post(
            '/students/api/login',
            data=json.dumps(payload),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_json())

    def test_login_case_insensitive(self):
        payload = {
            "email": self.email.upper(),
            "password": self.password
        }
        response = self.client.post(
            '/students/api/login',
            data=json.dumps(payload),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.get_json())

    def test_login_invalid(self):
        payload = {
            "email": self.email,
            "password": "wrongpass"
        }
        response = self.client.post(
            '/students/api/login',
            data=json.dumps(payload),
            content_type='application/json')
        self.assertEqual(response.status_code, 403)

    def test_login_wrong_email(self):
        payload = {
            "email": "notexist@test.com",
            "password": self.password
        }
        response = self.client.post(
            '/students/api/login',
            data=json.dumps(payload),
            content_type='application/json')
        self.assertEqual(response.status_code, 403)
