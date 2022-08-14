import json
import logging
import requests
from uuid import uuid4

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Sarufi(object):
    BASE_URL = "https://api.sarufi.io/v1/"

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = self.get_token()

    @property
    def headers(self):
        if self.token.get("token"):
            return {
                "Authorization": "Bearer " + self.token.get("token"),
                "Content-Type": "application/json",
            }
        else:
            # Log error
            logging.error(self.token.get("message"))
            logging.error("Please check your credentials\nand try again")

    def get_token(self):
        logging.info("Getting token")
        url = self.BASE_URL + "auth/login"
        data = json.dumps({"username": self.username, "password": self.password})
        response = requests.post(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        return response.json()

    def update_token(self):
        self.token = self.get_token()
        if self.token.get("token"):
            return True

    def bots(self):
        logging.info("Getting bots")
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
        logging.info("Creating bot")
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
        logging.info("Deleting bot")
        url = self.BASE_URL + "projects/"
        data = json.dumps({"project_id": project_id})
        response = requests.delete(url, json=data, headers=self.headers)
        return response.json()

    # Not implemented yet
    def update_bot(
        self, project_id, project_name, description=None, training_data=None, flow=None
    ):
        logging.info("Updating bot")
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

    def fetch_response(self, project_id, chat_id, message):
        url = self.BASE_URL + "conversation/"
        data = json.dumps(
            {"chat_id": chat_id, "project_id": project_id, "message": message}
        )
        return requests.post(url, data=data, headers=self.headers)

    def chat(self, project_id, message="Hello", chat_id=str(uuid4())):
        """
        Handle chat messages conversations

        Args:
            project_id (_type_): bot project id
            chat_id (_type_): bot chat_id (unique)
            message (_type_): message to be sent to bot

        Returns:
            response (json): bot response
        """
        logging.info("Sending message to bot and returning response")
        response = self.fetch_response(project_id, chat_id, message)
        logging.info(f"Status code: {response.status_code}")
        if response.status_code == 200:
            logging.info("Message sent successfully")
            return response.json()
        elif (
            response.status_code == 401
            and response.json().get("message") == "Invalid authorization token"
        ):
            logging.info("Token expired, updating token")
            self.token = self.get_token()
            if self.token.get("token"):
                logging.info("Token updated successfully")
                logging.info("Sending message to bot and returning response:again")
                return self.fetch_response(project_id, chat_id, message).json()
        logging.error(response.json().get("message"))
        return response.json()


class Bot(object):
    """ "
    BOT OBJECT

    Helper functions to access bot data in easy way
    """

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
