import os
import json
import requests


class Sarufi(object):
    BASE_URL = "http://api.sarufi.io/v1/"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = self.get_token()
        if self.token.get("token"):
            self.headers = {
                "Authorization": "Bearer " + self.token.get("token"),
                "Content-Type": "application/json",
            }

    def get_token(self):
        url = self.BASE_URL + "auth/login"
        data = json.dumps({"username": self.username, "password": self.password})
        response = requests.post(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        return response.json()

    def list_bots(self):
        url = self.BASE_URL + "projects"
        response = requests.get(url, headers=self.headers)
        return response.json()

    # Not implemented yet
    def get_bot(self, project_id):
        url = self.BASE_URL + "projects/" + str(project_id)
        response = requests.get(url, headers=self.headers)
        return response.json()

    def create_bot(self, project_name, description=None, training_data=None, flow=None):
        url = self.BASE_URL + "projects"
        data = json.dumps(
            {
                "name": project_name,
                "description": description,
                "training_data": training_data,
                "flow": flow,
            }
        )
        response = requests.post(url, data=data, headers=self.headers)
        return response.json()

    # Not implemented yet
    def delete_bot(self, project_id):
        url = self.BASE_URL + "projects/"
        data = json.dumps({"project_id": project_id})
        response = requests.delete(url, json=data, headers=self.headers)
        return response.json()

    # Not implemented yet
    def update_bot(
        self, project_id, project_name, description=None, training_data=None, flow=None
    ):
        url = self.BASE_URL + "projects/"
        data = json.dumps(
            {
                "name": project_name,
                "description": description,
                "training_data": training_data,
                "flow": flow,
                "project_id": project_id,
            }
        )
        response = requests.put(url, data=data, headers=self.headers)
        return response.json()

    def chat(self, project_id, chat_id, message):
        url = self.BASE_URL + "conversation/"
        data = json.dumps(
            {"chat_id": chat_id, "project_id": project_id, "message": message}
        )
        response = requests.post(url, data=data, headers=self.headers)
        return response.json()
