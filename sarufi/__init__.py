from __future__ import annotations
import os
import json
import logging
import requests
from uuid import uuid4
from pathlib import Path
from yaml import safe_load
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

    @staticmethod
    def read_file(_file: Union[Path, str]) -> Dict[Any, Any]:
        """read_file
            Reads a file and returns the contents as a dict
        Args:
            _file (Union[Path, str]): File to read(path or filename) | (intents, flows)

        Raises:
            FileNotFoundError: If file is not found

        Returns:
            Dict[Any, Any]: Contents of the file as a dict
        """
        # Get full path of file
        _file = os.path.realpath(_file)
        if os.path.exists(_file):
            try:
                if any([_file.endswith(ext) for ext in [".yaml", ".yml"]]):
                    logging.info(f"Reading {_file} as YAML")
                    return safe_load(open(_file))
                elif _file.endswith(".json"):
                    logging.info(f"Reading {_file} as JSON")
                    return json.load(open(_file))
                else:
                    raise FileNotFoundError(f"{_file} is not a valid file")
            except Exception as e:
                logging.error(e)
                logging.error("Could not read file")
        raise FileNotFoundError(f"File {_file} not found")

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

    def create_bot(
        self,
        name: str,
        description: str = None,
        flow: Dict[str, Any] = None,
        intents: Dict[str, List[str]] = None,
    ) -> Union[type[Bot], Dict[Any, Any]]:
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

    def create_from_file(
        self,
        intents: Union[Path, str] = None,
        flow: Union[Path, str] = None,
        metadata: Union[Path, str] = None,
    ) -> Union[type[Bot], Dict[Any, Any]]:
        """create_from_file

        Creates a new chatbot using sarufi engine from a file

        Args:
            intents (Union[Path, str], optional): Intent file. Defaults to None.
            flow (Union[Path, str], optional): Flow file. Defaults to None.
            metadata (Union[Path, str], optional): Metadata file. Defaults to None.

        Returns:
            Union[type[Bot], Dict[Any, Any]]: _description_
        """

        if intents:
            intents = self.read_file(intents)
        if flow:
            flow = self.read_file(flow)
        if metadata:
            metadata = self.read_file(metadata)
        else:
            metadata = {}
        return self.create_bot(
            metadata.get("name", "put name here"),
            description=metadata.get("description"),
            intents=intents,
            flow=flow,
        )

    def update_bot(
        self,
        id: int,
        name: str = None,
        description: str = None,
        intents: Dict[str, List[str]] = None,
        flow: Dict[str, Any] = None,
    ) -> Union[type[Bot], Dict[Any, Any]]:
        """update_bot

        Updates a chatbot with a specified (id) from sarufi engine

        Args:
            id (int): The ID of the chatbot to update
            name (str, optional): new chatbot name. Defaults to None.
            description (str, optional):new chatbot description . Defaults to None.
            intents (Dict[str, List[str]], optional): updated intents . Defaults to None.
            flow (Dict[str, Any], optional): updated flow . Defaults to None.

        Returns:
            Union[type[Bot], Dict[Any, Any]]: Chatbot object if bot updated successfully otherwise dict with error message
        """
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

    def update_from_file(
        self,
        id: int,
        intents: Union[Path, str] = None,
        flow: Union[Path, str] = None,
        metadata: Union[Path, str] = None,
    ) -> Union[type[Bot], Dict[Any, Any]]:
        """update_from_file

            Updates chatbot (intents, flow) using sarufi engine from a file

        Args:
            id (int): ID of the chatbot to update
            intents (Union[Path, str], optional): Intent file. Defaults to None.
            flow (Union[Path, str], optional): Flow file. Defaults to None.
            metadata (Union[Path, str], optional): Metadata file. Defaults to None.

        Returns:
            Union[type[Bot], Dict[Any, Any]]: _description_
        """

        if intents:
            intents = self.read_file(intents)
        if flow:
            flow = self.read_file(flow)
        if metadata:
            metadata = self.read_file(metadata)
        else:
            metadata = {}
        return self.update_bot(
            id=id,
            name=metadata.get("name"),
            description=metadata.get("description"),
            intents=intents,
            flow=flow,
        )

    def get_bot(self, id: int) -> Union[type[Bot], Dict[Any, Any]]:
        """get_bot

        Gets a chatbot  with a specified (id) from sarufi engine

        Args:
            id (int): The ID of the chatbot to get

        Returns:
            Union[Bot, Dict[Any, Any]]: Chatbot object if bot found otherwise dict with error message
        """
        logging.info("Getting bot with id: {}".format(id))
        url = self.BASE_URL + "chatbot/" + str(id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return Bot(response.json())
        return response.json()

    def bots(self) -> Union[List[type[Bot]], Dict]:
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

    def delete_bot(self, id: int) -> Dict[Any, Any]:
        """delete_bot

        Deletes a chatbot with a specified (id) from sarufi engine

        Args:
            id (int): The ID of the chatbot to delete

        Returns:
            Dict[Any, Any]: Dict with error message if bot not found otherwise dict with success message
        """
        logging.info("Deleting bot")
        url = self.BASE_URL + f"chatbot/{id}"
        response = requests.delete(url, headers=self.headers)
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

    def respond(
        self, message: str, message_type: str = "text", channel: str = "general"
    ):
        return self.chat(
            bot_id=self.id,
            chat_id=str(uuid4()),
            message=message,
            message_type=message_type,
            channel=channel,
        )

    def __str__(self) -> str:
        return f"Bot(id={self.id}, name={self.name})"

    def __repr__(self) -> str:
        return self.__str__()
