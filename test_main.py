import json
import unittest
from abc import ABC
from flask_testing import TestCase
from main import *

event_id = 10
user_id = 27
token = ''
class TestStringMethods(TestCase, ABC):
    def setUp(self):
        pass

    def create_app(self):
        return app

    def test_00_createUser(self):
        response = self.client.post('/createUser', data=json.dumps({"username": "testname12345",
                                                                    "firstName": "test12345",
                                                                    "lastName": "test12345",
                                                                    "password": "testpassword12345",
                                                                    "email": "test12345@gmail.com",
                                                                    "phone": "12345678",
                                                                    "userStatus": 1}), content_type="application/json")
        print(response.data)
        self.assertEqual(response.json, {'status': 200, 'message': 'success'})

    def test_01_auth(self):
        global token
        response = self.client.post('/auth', data=json.dumps({
            "username": "testname12345","password": "testpassword12345"}), content_type="application/json")
        token = response.json["access_token"]

    def test_02_update_user(self):
        global token, user_id
        response = self.client.put('/users/'+str(user_id), data=json.dumps({"username": "testname12345",
                                                                    "firstName": "test12345",
                                                                    "lastName": "test12345",
                                                                    "password": "testpassword12345",
                                                                    "email": "test12345@gmail.com",
                                                                    "phone": "12345678",
                                                                    "userStatus": 1
                                                                    }), headers = {"Authorization" : "JWT " + token, "Content-type": "application/json"})
        self.assertEqual(response.json, ['User was updated', 'User_ID: ', user_id])

    def test_03_create_event(self):
        global user_id
        response = self.client.post('/events', data=json.dumps({
                                    "event_name": "Eventupdated",
                                    "date": "ggg",
                                    "description": "xzczdaacdfsdfzxcz",
                                    "status": "jjsgg1",
                                    "name": "test12345",
                                    "ownerId": user_id,
                                    "userStatus": 1}),
                                    headers = {"Authorization" : "JWT " + token, "Content-type": "application/json"})
        self.assertEqual(response.json, "Event created")

    def test_04_update_event(self):
        global token, event_id, user_id
        response = self.client.put('/events/update/' + str(event_id), data=json.dumps({
                "event_name": "Eventupdated",
                "date": "gggg",
                "description": "xzczdaacdfsdfzxcz",
                "status": "jjsgg1",
                "name": "sdgggf",
                "ownerId": user_id,
                "userStatus": 1
        }), headers={"Authorization": "JWT " + token, "Content-type": "application/json"})
        self.assertEqual(response.json, "Event was updated")

    def test_05_get_event(self):
        global token, event_id
        response = self.client.get('/' + str(event_id), headers={"Authorization": "JWT " + token})
        self.assertNotEqual(response.json, "Incorrect ID")

    def test_06_rename_event(self):
        global token, event_id
        response = self.client.post('/renamevent/' + str(event_id), data=json.dumps({"event_name": "Eventupdated"}),
                                    headers={"Authorization": "JWT " + token, "Content-type": "application/json"})
        self.assertEqual(response.json, "Event was renamed")

    def test_07_delete_event(self):
        global token, event_id
        response = self.client.delete('/events/' + str(event_id), headers={"Authorization": "JWT " + token})
        self.assertEqual(response.json, {"msg": "event deleted successfully", "id": event_id})

    def test_08_get_all_events(self):
        global token
        response = self.client.get('/events/all', headers={"Authorization": "JWT " + token})
        self.assertNotEqual(response, "Error, you have not events")

    def test_09_delete_user(self):
        global token, user_id
        response = self.client.delete('/users/' + str(user_id),
                                      headers={"Authorization": "JWT " + token, "Content-type": "application/json"})
        self.assert200(response)

    if __name__ == 'main':
        unittest.main()



