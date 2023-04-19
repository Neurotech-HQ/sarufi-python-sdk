"""
**Sarufi** is a python SDK for the [Sarufi Conversational AI Platform](https://sarufi.io/).

To get started with Sarufi, you need to create an account at [sarufi.io](https://sarufi.io/).

Here an article that explains how to get started with Sarufi: [getting-started-with-sarufi](https://blog.neurotech.africa/what-is-sarufi/)

"""
from __future__ import annotations
import os
import json
import logging
import requests
from uuid import uuid4
from pathlib import Path
from yaml import safe_load
from typing import Dict, Dict, Any, List, Union, Optional

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


class Sarufi(object):
    """Sarufi Class"""

    _BASE_URL: str = "https://api.sarufi.io/"

    def __init__(
        self,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        token: Optional[str] = None,
    ) -> None:
        """Initialize the Sarufi class with client_id and client_secret or token


        Args:
            client_id (Optional[str], optional): Sarufi API Client ID. Defaults to None.
            client_secret (Optional[str], optional): Sarufi API Client Secret. Defaults to None.
            token (Optional[str], optional): Sarufi API token. Defaults to None.

        Examples:

        >>> sarufi = Sarufi(client_id="client_id", client_secret="client_secret")
        >>> dir(sarufi)
                [
                    "...",
                    "bots",
                    "chat",
                    "create_bot",
                    "create_from_file",
                    "delete_bot",
                    "_fetch_response",
                    "get_bot",
                    "headers",
                    "token",
                    "update_bot",
                    "update_from_file",
                ]
        """
        self.__client_id = client_id
        self.__client_secret = client_secret
        if token:
            self.token = {"access_token":token}
        else:
            self.token = self.__get_token()

    def __get_token(self):
        logging.info("Getting token")
        url = self._BASE_URL + "api/access_token/"
        data = json.dumps(
            {"client_id": self.__client_id, "client_secret": self.__client_secret}
        )
        response = requests.post(
            url, data=data, headers={"Content-Type": "application/json"}
        )
        return response.json()

    def __update_token(self):
        self.token = self.__get_token()
        if self.token.get("access_token"):
            return True
        logging.error("Error updating token")

    @staticmethod
    def __strip_of_nones(data: Dict[str, str]):
        if isinstance(data, dict):
            return {k: v for k, v in data.items() if v is not None}
        logging.error("Data is not a dict")
        logging.error(data)
        logging.error(type(data))

    @staticmethod
    def _read_file(_file: Union[Path, str]) -> Dict[Any, Any]:
        """_read_file
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
                return None
        raise FileNotFoundError(f"File {_file} not found")

    @property
    def headers(self):
        if self.token.get("access_token"):
            return {
                "Authorization": "Bearer " + self.token.get("access_token"),
                "Content-Type": "application/json",
            }
        else:
            # Log error
            logging.error(self.token.get("message"))
            logging.error("Please check your credentials\nand try again")

    def _get_req(
        self,
        url: str,
        _headers: Dict[str, str] = None,
        retry: int = 1,
    ):
        """get

        Simplifies making get requests

        Args:
            url (str): _description_
            _headers (Dict[str, str], optional): Authenticated header with Bearer token. Defaults to None.
            retry (int, optional): Number of time to rety incase token fails. Defaults to 1.
        """

        response = requests.get(url, headers=_headers or self.headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 400 and (
            response.json().get("detail") == "Token invalid"
            or response.json().get("detail") == "Token Expired"
        ):
            logging.info("Token invalid[REFRESHING]")
            self.__update_token()
            if retry > 0:
                return self._get_req(url=url, retry=retry - 1)
        logging.error("Error [GET]")
        return response

    def _post_req(
        self,
        url: str,
        body: Dict[str, Any],
        _headers: Dict[str, str] = None,
        retry: int = 1,
    ) -> Union[type[Bot], Dict[Any, Any]]:
        """post

        Simplifies the process of making a post request to sarufi engine

        Args:
            url (str): URL to make the request to
            body (Dict[str, Any]): Body of the request
            _headers (Dict[str, str], optional): Request headers. Defaults to None.
            retry (int, optional): Number of time to retry when tokens are invalid . Defaults to 1.

        Returns:
            Union[type[Bot], Dict[Any, Any]]: Bot object if request is successful otherwise dict with error message
        """

        _data = json.dumps(self.__strip_of_nones(body))  # remove None values
        _headers = _headers or self.headers
        response = requests.post(url, data=_data, headers=_headers)
        if response.status_code == 200:
            return response

        elif response.status_code == 400 and (
            response.json().get("detail") == "Token invalid"
            or response.json().get("detail") == "Token Expired"
        ):
            logging.info("Token invalid[REFRESHING]")
            self.__update_token()  # Refresh token
            if retry > 0:
                # Retry
                return self._post_req(body=body, url=url, retry=retry - 1)

        logging.error("Error [POST]")
        return response

    def _put_req(
        self,
        url: str,
        body: Dict[str, Any],
        _headers: Dict[str, str] = None,
        retry: int = 1,
    ) -> Union[type[Bot], Dict[Any, Any]]:
        """put

        Simplifies the process of making a put request to sarufi engine

        Args:
            url (str): URL to make the request to
            body (Dict[str, Any]): Body of the request
            _headers (Dict[str, str], optional): Request headers. Defaults to None.
            retry (int, optional): Number of time to retry when tokens are invalid . Defaults to 1.

        Returns:
            Union[type[Bot], Dict[Any, Any]]: Bot object if request is successful otherwise dict with error message
        """

        _data = json.dumps(self.__strip_of_nones(body))
        _headers = _headers or self.headers
        response = requests.put(url, data=_data, headers=_headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 400 and (
            response.json().get("detail") == "Token invalid"
            or response.json().get("detail") == "Token Expired"
        ):
            logging.info("Token invalid[REFRESHING]")
            self.__update_token()
            if retry > 0:
                return self._put_req(url=url, body=body, retry=retry - 1)
        logging.error("Error [PUT]")
        return response

    def _delete_req(
        self,
        url: str,
        _headers: Dict[str, str] = None,
        retry: int = 1,
    ) -> Union[type[Bot], Dict[Any, Any]]:
        """delete

        Simplifies the process of making a delete request to sarufi engine

        Args:
            url (str): URL to make the request to
            _headers (Dict[str, str], optional): Request headers. Defaults to None.
            retry (int, optional): Number of time to retry when tokens are invalid . Defaults to 1.

        Returns:
            Union[type[Bot], Dict[Any, Any]]: Bot object if request is successful otherwise dict with error message
        """

        _headers = _headers or self.headers
        response = requests.delete(url, headers=_headers)
        if response.status_code == 200:
            return response
        elif response.status_code == 400 and (
            response.json().get("detail") == "Token invalid"
            or response.json().get("detail") == "Token Expired"
        ):
            logging.info("Token invalid[REFRESHING]")
            self.__update_token()
            if retry > 0:
                return self._delete_req(url=url, retry=retry - 1)
        logging.error("Error [DELETE]")
        return response

    def create_bot(
        self,
        name: str,
        description: str = None,
        industry: str = None,
        flow: Dict[str, Any] = None,
        intents: Dict[str, List[str]] = None,
        webhook_url: str = None,
        webhook_trigger_intents: List[str] = None,
        visible_on_community: bool = None,
    ) -> Union[type[Bot], Dict[Any, Any]]:
        """create_bot

        Creates a new chatbot using `sarufi API`

        Args:
            name (str): Name of the chatbot
            description (_type_, optional): description about what the chabot does. Defaults to None.
            flow (_type_, optional): Flow to control execution of the chatbot. Defaults to None.
            intents (_type_, optional): Intents to train the chatbot. Defaults to None.

        Returns:
            Union[Bot, Dict]: Chatbot object if bot created successfully otherwise dict with error message

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        2022-08-23 15:03:00,928 - root - INFO - Getting token
        >>> bot = sarufi.create_bot(name='Maria')
        2022-08-23 15:03:09,891 - root - INFO - Creating bot
        >>> bot
        Bot(id=5, name=Maria, description=PUT DESCRIPTION HERE)
        """

        logging.info("Creating bot")
        url = self._BASE_URL + "chatbot"
        data = {
            "name": name,
            "description": description,
            "intents": intents,
            "flows": flow,
            "industry": industry,
            "webhook_url": webhook_url,
            "webhook_trigger_intents": webhook_trigger_intents,
            "visible_on_community": visible_on_community,
        }
        response = self._post_req(body=data, url=url)
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
            Union[type[Bot], Dict[Any, Any]]: Chatbot object if bot created successfully otherwise dict with error message

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('client_id', 'client_secret')
        >>> bot = sarufi.create_from_file(
        ...     intents='data/intents.json',
        ...     flow='data/flow.json',
        ...     metadata='data/metadata.json'
            )"""

        if intents:
            intents = self._read_file(intents)
        if flow:
            flow = self._read_file(flow)
        if metadata:
            metadata = self._read_file(metadata)
        else:
            metadata = {}
        return self.create_bot(
            metadata.get("name", "put name here"),
            description=metadata.get("description"),
            industry=metadata.get("industry"),
            webhook_url=metadata.get("webhook_url"),
            webhook_trigger_intents=metadata.get("webhook_trigger_intents"),
            visible_on_community=metadata.get("visible_on_community"),
            intents=intents,
            flow=flow,
        )

    def update_bot(
        self,
        id: int,
        name: str = None,
        industry: str = None,
        description: str = None,
        intents: Dict[str, List[str]] = None,
        flow: Dict[str, Any] = None,
        webhook_url: str = None,
        webhook_trigger_intents: List[str] = None,
        visible_on_community: bool = None,
    ) -> Union[type[Bot], Dict[Any, Any]]:
        """update_bot

        Updates a chatbot with a specified (id) from sarufi engine

        Args:
            id (int): The ID of the chatbot to update
            name (str, optional): new chatbot name. Defaults to None.
            description (str, optional):new chatbot description . Defaults to None.
            intents (Dict[str, List[str]], optional): updated intents . Defaults to None.
            flow (Dict[str, Any], optional): updated flow . Defaults to None.
            webhook_url(str): The URL to be triggred by the chatbot at the fulfillment of intent
            webhook_trigger_intents(List[str]): Intents to be triggered by the webhook
            visible_on_community(bool): Should a bot be visible on a community page.

        Returns:
            Union[type[Bot], Dict[Any, Any]]: Chatbot object if bot updated successfully otherwise dict with error message

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> bot = sarufi.update_bot(
            ...     id=5,
            ...     name='Maria',
            ...     description='A chatbot that does this and that',
            ...     intents={...},
            ...     flow={...},
            ...     industry='healthcare',
            ...     visible_on_community=True
            ... )
        """
        logging.info("Updating bot")
        url = self._BASE_URL + f"chatbot/{id}"
        data = {
            "name": name,
            "description": description,
            "intents": intents,
            "flows": flow,
            "industry": industry,
            "webhook_url": webhook_url,
            "webhook_trigger_intents": webhook_trigger_intents,
            "visible_on_community": visible_on_community,
        }
        response = self._put_req(body=data, url=url)
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
            Union[type[Bot], Dict[Any, Any]]: Chatbot object if bot updated successfully otherwise dict with error message

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> bot = sarufi.update_from_file(
            ...     id=5,
            ...     intents='data/intents.json',
            ...     flow='data/flow.json',
            ...     metadata='data/metadata.json'
            ... )
        """

        if intents:
            intents = self._read_file(intents)
        if flow:
            flow = self._read_file(flow)
        if metadata:
            metadata = self._read_file(metadata)
        else:
            metadata = {}
        return self.update_bot(
            id=id,
            name=metadata.get("name"),
            industry=metadata.get("industry"),
            description=metadata.get("description"),
            webhook_url=metadata.get("webhook_url"),
            webhook_trigger_intents=metadata.get("webhook_trigger_intents"),
            visible_on_community=metadata.get("visible_on_community"),
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

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> bot = sarufi.get_bot(id=5)
        >>> print(bot)
        Bot(name='iBank', id=23)
        """
        logging.info("Getting bot with id: {}".format(id))
        url = self._BASE_URL + "chatbot/" + str(id)
        response = self._get_req(url=url)
        if response.status_code == 200:
            return Bot(response.json(), token=self.token)
        return response.json()

    def bots(self) -> Union[List[type[Bot]], Dict]:
        """bots

        Gets all user chatbots from sarufi engine

        Returns:
            Union[List[Bot], Dict]: List of chatbots if successful otherwise dict with error message

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        2022-08-23 15:03:00,928 - root - INFO - Getting token
        >>> sarufi.bots()
        2022-08-23 15:03:57,845 - root - INFO - Getting bots
        [Bot(id=4, name=iBank, description=PUT DESCRIPTION HERE), Bot(id=5, name=Maria, description=Swahili Cognitive Mental Health Chatbot)]

        """
        logging.info("Getting bots")
        url = self._BASE_URL + "chatbots"
        response = self._get_req(url=url)
        if response.status_code == 200:
            return [Bot(bot, token=self.token) for bot in response.json()]
        return response.json()

    def _fetch_response(
        self, bot_id: int, chat_id: str, message: str, message_type: str, channel: str
    ):
        url = self._BASE_URL + "conversation/"
        if channel == "whatsapp":
            logging.info("Sending message to bot via whatsapp")
            url = url + "whatsapp/"

        data = {
            "chat_id": chat_id,
            "bot_id": bot_id,
            "message": message,
            "message_type": message_type,
        }
        return self._post_req(url=url, body=data)

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

        Examples:
            >>> from sarufi import Sarufi
            >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
            >>> sarufi.chat(bot_id=5, chat_id='123456789', message='Hello')

            # You can also send direct from bot instance

            >>> mybot = sarufi.get_bot(id=5)
            >>> mybot.respond(chat_id='123456789', message='Hello')
        """
        logging.info("Sending message to bot and returning response")
        response = self._fetch_response(
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

        logging.error("Message not sent[CHAT]")
        return response.json()

    def chat_status(self, bot_id: int, chat_id: str):
        """
        Handle chat messages conversations

        Help to fetch the status of a chat session

        Args:
            bot_id (int): The ID of the chatbot to get
            chat_id (str): The ID of the chat session

        Returns:
            response (json): bot response

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> sarufi.chat_status(bot_id=5, chat_id='chat_id')
        >>> {'current_state': 'greetings', 'next_state':'end'}

        """
        logging.info("Sending message to bot and returning response")
        url = self._BASE_URL + "conversation/allchannels/status"
        data = {
            "chat_id": chat_id,
            "bot_id": str(bot_id),
        }
        response = self._post_req(url=url, body=data)
        if response.status_code == 200:
            logging.info("Message sent successfully")
            return response.json()

        logging.error("Message not sent[CHAT]")
        return response.json()

    def update_conversation_state(self, bot_id: int, chat_id: str, next_state: str):
        """
        Update the conversation state of a chat session

        Use this to explicitly update the conversation state of a chat session

        Args:
            bot_id (int): The ID of the chatbot to get
            chat_id (str): The ID of the chat session
            next_state(str): The next state to update to

        Returns:
            response (json): bot response

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> sarufi.update_conversation_state(bot_id=5, chat_id='chat_id', state='greetings')
        >>> {..new state machine..}

        """
        logging.info("Sending message to bot and returning response")
        url = self._BASE_URL + "conversation-state"
        data = {
            "chat_id": chat_id,
            "bot_id": str(bot_id),
            "next_state": next_state,
        }
        response = self._post_req(url=url, body=data)
        if response.status_code == 200:
            logging.info("Message sent successfully")
            return response.json()

        logging.error("Message not sent[CHAT]")
        return response.json()

    def delete_bot(self, id: int) -> Dict[Any, Any]:
        """delete_bot

        Deletes a chatbot with a specified (id) from sarufi engine

        Args:
            id (int): The ID of the chatbot to delete

        Returns:
            Dict[Any, Any]: Dict with error message if bot not found otherwise dict with success message

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> sarufi.delete_bot(5)
        {'message': 'Bot with ID 5 deleted successfully'}
        """
        logging.info("Deleting bot")
        url = self._BASE_URL + f"chatbot/{id}"
        response = self._delete_req(url=url)
        return response.json()


class Bot(Sarufi):
    """
    BOT OBJECT

    has `Helper` functions to access bot data in easy way

    Examples:

    >>> from sarufi import Sarufi
    >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
    >>> bot = sarufi.get_bot(4)

    ### Get bot name
    >>> bot.name
    'iBank'

    ### Get bot description
    >>> bot.description
    'I simulate a bank chatbot'

    ### Get bot industry
    >>> bot.industry

    ### Get bot intents
    >>> bot.intents

    ### Get bot flow
    >>> bot.flow

    ### Get bot id
    >>> bot.id
    32

    ## You can also get bot data as a dict

    >>> bot.data
    {...}

    You can also quickly update bot data from name to intents and flows

    ### Update bot name
    >>> bot.name = 'New name'

    ### Update bot description
    >>> bot.description = 'New description'
    """

    def __init__(self, data: Dict, token=None):
        super().__init__(token=token)
        self.data = data
        self.chat_id = str(uuid4())

    # Getter only
    @property
    def id(self):
        return self.data.get("id")

    @property
    def evaluation_metrics(self) -> Dict:
        """
        Returns the evaluation metrics of bot

        Returns(Dict): Evaluation Metrics of a bot

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('testing@xyz.com', '123')
        >>> mybot = sarufi.get_bot(bot_id)
        >>> mybot.evaluation_metrics
        ... None
        """
        return self.data.get("evaluation_metrics")

    # Getter and setters

    # Name attribute
    @property
    def name(self):
        return self.data.get("name")

    @name.setter
    def name(self, name: str):
        if isinstance(name, str):
            self.data["name"] = name
            r = self.update_bot(id=self.id, name=name)
            logging.info(r)
        else:
            raise TypeError("name must be a string")

    # Industry attribute
    @property
    def industry(self):
        return self.data.get("industry")

    @industry.setter
    def industry(self, industry: str):
        if isinstance(industry, str):
            self.data["industry"] = industry
            r = self.update_bot(self.id, industry=industry)
            logging.info(r)
        else:
            raise TypeError("industry must be a string")

    # Description attribute
    @property
    def description(self):
        return self.data.get("description")

    @description.setter
    def description(self, description: str):
        if isinstance(description, str):
            self.data["description"] = description
            r = self.update_bot(self.id, description=description)
            logging.info(r)
        else:
            raise TypeError("description must be a string")

    # visible_on_community attribute
    @property
    def visible_on_community(self):
        return self.data.get("visible_on_community")

    @visible_on_community.setter
    def visible_on_community(self, visible_on_community: bool):
        if isinstance(visible_on_community, bool):
            self.data["visible_on_community"] = visible_on_community
            r = self.update_bot(self.id, visible_on_community=visible_on_community)
            logging.info(r)
        else:
            raise TypeError("visible_on_community must be a boolean")

    # intents attribute
    @property
    def intents(self):
        return self.data.get("intents")

    @intents.setter
    def intents(self, intents: Dict):
        if isinstance(intents, dict):
            self.data["intents"] = intents
            r = self.update_bot(self.id, intents=intents)
            logging.info(r)
        else:
            raise TypeError("intents must be a Dictionary")

    def add_intent(self, intents: Dict[str, List[str]]):
        """add_intent

        Appends an intent to the bot's intents

        Args:
            intents (Dict[str, List[str]]): The intents to add

        Raises:
            TypeError: If intent is not a dictionary

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('testing@gmail.com', '123')
        >>> chatbot = sarufi.get_bot(1)
        >>> chatbot.add_intent({'greeting': ['hello', 'hi']})
        """
        if isinstance(intents, dict):
            updated_intents = self.intents
            updated_intents.update(intents)
            self.intents = updated_intents
            logging.info(f'A new intents "{list(intents.keys())}" has been added')
        else:
            raise TypeError("intent must be a dictionary {intent_name: [utterances]}")

    # flow attribute
    @property
    def flow(self):
        return self.data.get("flows")

    @flow.setter
    def flow(self, flow: Dict):
        if isinstance(flow, dict):
            self.data["flows"] = flow
            r = self.update_bot(self.id, flow=flow)
            logging.info(r)
        else:
            raise TypeError("flow must be a Dictionary")

    def add_flow(self, flow: Dict[str, Any]):
        """add_flow

        Appends a flow to the bot's flows

        Args:
            flow (Dict[str, Any]): The flow to add

        Raises:
            TypeError: If flow is not a dictionary

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('testing@gmail.com', '123')
        >>> sarufi.get_bot(1)
        >>> chatbot.add_flow({'greeting': {'message': ['hello'], 'next_state': 'greeting'}})
        """
        if isinstance(flow, dict):
            updated_flows = self.flow
            updated_flows.update(flow)
            self.flow = updated_flows
            logging.info(f'A new flow "{list(flow.keys())}" has been added')
        else:
            raise TypeError("flow must be a dictionary {flow_name: flow_data}")

    # webhooh_url attribute
    @property
    def webhook_url(self) -> str:
        """
        Returns the Webhook to be triggered by the chatbot

        Returns(str): The Webhook of a chatbot

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('testing@xyz.com', '123')
        >>> mybot = sarufi.get_bot(bot_id)
        >>> mybot.webhook_url
        ... https://www.xyz.com/hook
        """
        return self.data.get("webhook_url")

    @webhook_url.setter
    def webhook_url(self, url: str) -> str:
        """Set up a new webhook URL for the chatbot

        Args:
            url (str): The new webhook URL (eg. https://www.xyx.com/hook)

        Returns:
            str: The updated Webhook URL for the chatbot

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('testing@xyz.com', '123')
        >>> mybot = sarufi.get_bot(bot_id)
        >>> mybot.webhook_url = "https://www.xyx.com/hook"
        ...https://www.xyz.com/hook"
        """
        if isinstance(url, str):
            self.data["webhook_url"] = url
            r = self.update_bot(self.id, webhook_url=url)
            logging.info(r)
        else:
            raise TypeError("webhook_url must be a string")

    # webhook_trigger_intents attribute
    @property
    def webhook_trigger_intents(self) -> List[str]:
        """
        Returns Intents that trigger the webhook

        Returns(List[str]): List of intents that trigger the webhook

        Examples:
        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('testing@xyz.com', '123')
        >>> mybot = sarufi.get_bot(bot_id)
        >>> mybot.webhook_trigger_intents
        ... ['greeting']
        """
        return self.data.get("webhook_trigger_intent")

    @webhook_trigger_intents.setter
    def webhook_trigger_intents(self, intents: List[str]) -> List[str]:
        if isinstance(intents, list):
            self.data["webhook_trigger_intents"] = intents
            r = self.update_bot(self.id, webhook_trigger_intents=intents)
            logging.info(r)
        else:
            raise TypeError("intents Trigger must be a list of strings")

    # Get response from a bot
    def respond(
        self,
        message: str,
        message_type: str = "text",
        channel: str = "general",
        chat_id: str = None,
    ) -> Dict | None:
        """respond to a message

        Args:
            message (str): The message to send
            message_type (str, optional): The type of message. Defaults to "text".
            channel (str, optional): The channel to send the message to. Defaults to "general".
            chat_id (str, optional): The chat id to send the message to. Defaults to None.

        Returns:
            Dict | None: The response from the bot

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> chatbot = sarufi.get_bot(1)
        >>> chatbot.respond('hello')
        {'message': ['Hello, how can I help you?'], 'next_state': 'greeting'}
        """
        return self.chat(
            bot_id=self.id,
            chat_id=chat_id or self.chat_id,
            message=message,
            message_type=message_type,
            channel=channel,
        )

    def predict_intent(
        self,
        message: str,
    ) -> Dict[bool, str, float]:
        """predict an intent of a message

        Gets an intent prediction on the message provided

        Args:
            message (str): the message you want to predict

        Returns:
            Dict[bool, str, float]: An object containing the intent, status and the confidence of prediction

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> bot = sarufi.get_bot(id=5)
        >>> print(bot.predict_intent("your message"))
        {
            intent: "an_intent",
            status: true
            confidence: 0.75,
        }
        """

        url = self._BASE_URL + "predict/intent"
        response = self._post_req(
            url, {"bot_id": self.data.get("id"), message: message}
        )
        return response.json()

    def chat_state(self, chat_id: str) -> Union[Dict, None]:
        """chat_state

        Returns the current state and the next state of the chat

        Args:
            chat_id (str): The chat id to get the state of

        Returns:
            Union[Dict, None]: The state of the chat

        Examples:
            >>> from sarufi import Sarufi
            >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
            >>> chatbot = sarufi.get_bot(1)
            >>> chatbot.chat_state('chat_id')
            >>> {'current_state': 'greeting', 'next_state': 'main_menu'}
        """
        return self.chat_status(bot_id=self.id, chat_id=chat_id)

    def delete(self):
        """
        delete the bot with the given id

        Examples:

        >>> from sarufi import Sarufi
        >>> sarufi = Sarufi('your-client-id', 'your-client-secret')
        >>> chatbot = sarufi.get_bot(1)
        >>> chatbot.delete()
        """
        return self.delete_bot(self.id)

    def __str__(self) -> str:
        return f"Bot(id={self.id}, name={self.name})"

    def __repr__(self) -> str:
        return self.__str__()
