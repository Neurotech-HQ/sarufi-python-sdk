import json
import logging
import requests
from uuid import uuid4

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Sarufi(object):
    BASE_URL = "https://api.sarufi.io/"

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
        url = self.BASE_URL + "users/login"
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
        url = self.BASE_URL + "chatbots"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [Bot(bot) for bot in response.json()]
        return response.json()

    # Not implemented yet
    def get_bot(self, bot_id):
        url = self.BASE_URL + "projects/" + str(bot_id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return Bot(response.json())
        return response.json()

    def create_bot(self, name: str, description=None, flow=None, intents=None):
        logging.info("Creating bot")
        url = self.BASE_URL + "chatbot"
        data = json.dumps(
            {
                "name": name,
                "description": description,
                "intents": intents,
                "flows": flow,
            }
        )
        response = requests.post(url, data=data, headers=self.headers)
        return response.json()

    def delete_bot(self, id: int):
        logging.info("Deleting bot")
        url = self.BASE_URL + f"chatbot/{id}"
        response = requests.delete(url, headers=self.headers)
        return response.json()

    def update_bot(
        self, id: int, name: str = None, description=None, intents=None, flow=None
    ):
        logging.info("Updating bot")
        url = self.BASE_URL + f"chatbot/{id}"
        data = json.dumps(
            {
                "name": name,
                "description": description,
                "intents": intents,
                "flows": flow,
            }
        )
        response = requests.put(url, data=data, headers=self.headers)
        return response.json()

    def fetch_response(
        self,
        bot_id: int,
        chat_id: str,
        message: str,
        message_type: str = "text",
        channel: str = "general",
    ):
        url = self.BASE_URL + "conversation/"
        if channel == "whatsapp":
            url = url + "whatsapp/"

        data = json.dumps(
            {
                "chat_id": chat_id,
                "bot_id": bot_id,
                "message": message,
                "message_type": message_type,
            }
        )
        return requests.post(url, data=data, headers=self.headers)

    def chat(
        self,
        bot_id: int,
        message: str = "Hello",
        chat_id: str = str(uuid4()),
        message_type: str = "text",
        channel: str = "general",
    ):
        """
        Handle chat messages conversations

        Args:
            bot_id (_type_): bot project id
            chat_id (_type_): bot chat_id (unique)
            message (_type_): message to be sent to bot
            message_type (_type_): message type (text, image, audio, video, file)

        Returns:
            response (json): bot response
        """
        logging.info("Sending message to bot and returning response")
        response = self.fetch_response(
            bot_id=bot_id, chat_id=chat_id, message=message, message_type=message_type
        )
        logging.info(f"Status code: {response.status_code}")
        if response.status_code == 200:
            logging.info("Message sent successfully")
            return response.json()
        elif (
            response.status_code == 401
            and response.json().get("message") == "Not authenticated"
        ):
            logging.info("Token expired, updating token")
            self.token = self.get_token()
            if self.token.get("token"):
                logging.info("Token updated successfully")
                logging.info("Sending message to bot and returning response:again")
                return self.fetch_response(
                    bot_id=bot_id,
                    chat_id=chat_id,
                    message=message,
                    message_type=message_type,
                ).json()
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
        return self.data.get("intents")

    @property
    def flow(self):
        return self.data.get("flows")

    def __str__(self) -> str:
        return f"Bot(id={self.id}, name={self.name}, description={self.description})"

    def __repr__(self) -> str:
        return self.__str__()
