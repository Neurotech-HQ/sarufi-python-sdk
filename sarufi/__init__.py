import json
import logging
import requests
from uuid import uuid4
from typing import Dict, Dict, Any, List, Optional, Union, Tuple, Callable, cast

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Sarufi(object):
    BASE_URL = "https://api.sarufi.io/"

    def __init__(self, username=None, password=None, token=None):
        self.username = username
        self.password = password
        if token:
            self.token = token
        else:
            self.token = self.get_token()

    @staticmethod
    def strip_of_nones(data: Dict):
        return {k: v for k, v in data.items() if v is not None}

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

    def bots(self) -> Union[List[Bot], Dict]:
        """bots

        Gets all user chatbots from sarufi engine

        Returns:
            Union[List[Bot], Dict]: List of chatbots if successful otherwise dict with error message

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('myname@domain.com', 'password')
        2022-08-23 15:03:00,928 - root - INFO - Getting token
        >>> sarufi.bots()
        2022-08-23 15:03:57,845 - root - INFO - Getting bots
        [Bot(id=4, name=iBank, description=PUT DESCRIPTION HERE), Bot(id=5, name=Maria, description=Swahili Cognitive Mental Health Chatbot)]

        """
        logging.info("Getting bots")
        url = self.BASE_URL + "chatbots"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return [Bot(bot, token=self.token) for bot in response.json()]
        return response.json()

    def get_bot(self, id: int) -> Union[Bot, Dict[Any, Any]]:
        """get_bot

        Gets a chatbot  with a specified (id) from sarufi engine

        Args:
            id (int): The ID of the chatbot to get

        Returns:
            Union[Bot, Dict[Any, Any]]: Chatbot object if bot found otherwise dict with error message
        """
        url = self.BASE_URL + "chatbot/" + str(id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return Bot(response.json())
        return response.json()

    def create_bot(self, name: str, description=None, flow=None, intents=None):
        """create_bot

        Creates a new chatbot using sarufi engine

        Args:
            name (str): Name of the chatbot
            description (_type_, optional): description about what the chabot does. Defaults to None.
            flow (_type_, optional): Flow to control execution of the chatbot. Defaults to None.
            intents (_type_, optional): Intents to train the chatbot. Defaults to None.

        Returns:
            Union[Bot, Dict]: Chatbot object if bot created successfully otherwise dict with error message

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('myname@domain.com', 'password')
        2022-08-23 15:03:00,928 - root - INFO - Getting token
        >>> bot = sarufi.create_bot(name='Maria')
        2022-08-23 15:03:09,891 - root - INFO - Creating bot
        >>> bot
        Bot(id=5, name=Maria, description=PUT DESCRIPTION HERE)
        """

        logging.info("Creating bot")
        url = self.BASE_URL + "chatbot"
        data = json.dumps(
            self.strip_of_nones(
                {
                    "name": name,
                    "description": description,
                    "intents": intents,
                    "flows": flow,
                }
            )
        )
        response = requests.post(url, data=data, headers=self.headers)
        if response.status_code == 200:
            return Bot(response.json(), token=self.token)
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
            self.strip_of_nones(
                {
                    "name": name,
                    "description": description,
                    "intents": intents,
                    "flows": flow,
                }
            )
        )
        response = requests.put(url, data=data, headers=self.headers)
        if response.status_code == 200:
            return Bot(response.json(), token=self.token)
        return response.json()

    def fetch_response(
        self, bot_id: int, chat_id: str, message: str, message_type: str, channel: str
    ):
        url = self.BASE_URL + "conversation/"
        if channel == "whatsapp":
            logging.info("Sending message to bot via whatsapp")
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
        chat_id: str = str(uuid4()),
        message: str = "Hello",
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
            bot_id=bot_id,
            chat_id=chat_id,
            message=message,
            message_type=message_type,
            channel=channel,
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


class Bot(Sarufi):
    """ "
    BOT OBJECT

    Helper functions to access bot data in easy way
    """

    def __init__(self, data: Dict, token=None):
        super().__init__(token=token)
        self.data = data

    @property
    def id(self):
        return self.data.get("id")

    @property
    def name(self):
        return self.data.get("name")

    @name.setter
    def name(self, name: str):
        if isinstance(name, str):
            self.data["name"] = name
            return self.update_bot(self.id, name=name)
        else:
            raise TypeError("name must be a string")

    @property
    def description(self):
        return self.data.get("description")

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.data["description"] = description
            return self.update_bot(self.id, description=description)
        else:
            raise TypeError("description must be a string")

    @property
    def intents(self):
        return self.data.get("intents")

    @intents.setter
    def intents(self, intents: Dict):
        if isinstance(intents, dict):
            self.data["intents"] = intents
            return self.update_bot(self.id, intents=intents)
        else:
            raise TypeError("intents must be a Dictionary")

    @property
    def flow(self):
        return self.data.get("flows")

    @flow.setter
    def flow(self, flow: Dict):
        if isinstance(flow, dict):
            self.data["flows"] = flow
            return self.update_bot(self.id, flow=flow)
        else:
            raise TypeError("flow must be a Dictionary")

    def __str__(self) -> str:
        return f"Bot(id={self.id}, name={self.name}, description={self.description})"

    def __repr__(self) -> str:
        return self.__str__()
