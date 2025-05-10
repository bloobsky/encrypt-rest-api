import unittest
import json
from app import app
from pymongo import MongoClient
from api.conf import MONGODB_DBNAME

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.db = MongoClient().get_database(MONGODB_DBNAME)
        self.db.users.delete_many({})

    def test_registration_success(self):
        payload = {
            "email": "flaskuser@test.com",
            "password": "password123",
            "displayName": "Flask User",
            "address": "1 Flask Rd",
            "phone": "0831234567",
            "dateOfBirth": "2000-01-01",
            "disabilities": ["None"]
        }
        response = self.client.post(
            '/students/api/registration',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("email", response.get_json())

    def test_duplicate_registration(self):
        payload = {
            "email": "dupe@test.com",
            "password": "password123",
            "displayName": "Dupe"
        }
        # First registration attempt
        self.client.post(
            '/students/api/registration',
            data=json.dumps(payload),
            content_type='application/json'
        )
        # Second registration attempt with the same email
        response = self.client.post(
            '/students/api/registration',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 409)

    def test_registration_without_display_name(self):
        payload = {
            "email": "nodisplay@test.com",
            "password": "password123"
            # 'displayName' is intentionally omitted
        }
        response = self.client.post(
            '/students/api/registration',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["email"], "nodisplay@test.com")
        self.assertEqual(data["displayName"], "nodisplay@test.com")

    def test_registration_twice(self):
        payload = {
            "email": "twice@test.com",
            "password": "password123",
            "displayName": "Twice"
        }
        response1 = self.client.post(
            '/students/api/registration',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 200)
        response2 = self.client.post(
            '/students/api/registration',
            data=json.dumps(payload),
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 409)
