import os
import json
import requests


class Sarufi(object):
    BASE_URL = "https://api.sarufi.io/v1/"

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

    def bots(self):
        url = self.BASE_URL + "projects"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [Bot(bot) for bot in response.json()]
        return response.json()

    # Not implemented yet
    def get_bot(self, project_id):
        url = self.BASE_URL + "projects/" + str(project_id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return Bot(response.json())
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


class Bot(object):
    def __init__(self, data):
        self.data = data

    @property
    def id(self):
        return self.data.get("id")

    @property
    def name(self):
        return self.data.get("name")

    @property
    def description(self):
        return self.data.get("description")

    @property
    def intents(self):
        return self.data.get("training_data")

    @property
    def flow(self):
        return self.data.get("flow")

    def __str__(self) -> str:
        return f"Bot(id={self.id}, name={self.name}, description={self.description})"

    def __repr__(self) -> str:
        return self.__str__()
