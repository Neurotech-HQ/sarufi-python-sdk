<samp>

# sarufi-python-sdk

[![Downloads](https://pepy.tech/badge/sarufi)](https://pepy.tech/project/sarufi)
[![Downloads](https://pepy.tech/badge/sarufi/month)](https://pepy.tech/project/sarufi)
[![Downloads](https://pepy.tech/badge/sarufi/week)](https://pepy.tech/project/sarufi)

Sarufi Python SDK to help you interact with SARUFI platform

## Table of Contents
- [Installation](#installation)  
- [Authentication](#authentication)  
- [Creating a Bot](#creating-a-bot)  
    - [Creating a Bot from file](#creating-a-bot-from-file)  
- [Updating bot](#updating-bot)     
    - [Update a bot from file](#update-a-bot-from-file)  
- [Using it in a conversation](#using-it-in-a-conversation)    
    - [Get a bot](#get-a-bot)  
- [Deleting a bot](#deleting-a-bot) 

## Installation

Make sure you have [sarufi package](https://github.com/Neurotech-HQ/sarufi-python-sdk) installed on your machine before launching your telegram bot, you can easily install by the following command;

```bash
git clone https://github.com/Neurotech-HQ/sarufi-python-sdk
cd sarufi-python-sdk
sarufi-python-sdk $ python setup.py install
```

## Authentication

To authenticate you're bot, you have to specify your client_id and client_secret for Sarufi Platform just as shown below;

```python
>>> from sarufi import Sarufi
>>> sarufi = Sarufi('client_id', 'client_secret')
```

## Creating a Bot

To create you're bot with sarufi, you have to be aware of two importants idea or concepts which is **intents** and **flow**.

Here an example on how to create your bot;

```python
sarufi.create_bot(
    name="Athony bot",
    description="My bot can do a lot",
    intents={
        "salamu": ["Mambo", "Hi", "Hello", "Niaje"],
        "contact": [
            "naomba mawasiliano",
            "naomba number",
            "naomba namba",
            "nipe mawasiliano",
            "nipe contact",
        ],
    },
    flow={
        "salamu": {"message": ["Hi", "Naimani upo salama"], "next": "end"},
        "contact": {
            "message": ["Ungependa kupata namba ya nani ?"],
            "next_state": "chukua_namba",
        },
        "chukua_namba": {
            "message": ["Namba ya huyo mtu ni 07374734737", "Karibu tena !!"],
            "next_state": "end",
        },
    },
)
```

### Creating a Bot from file

You can create your bot from a file, Here is an example on how to create your bot from a file;

```python
from sarufi import Sarufi

sarufi = Sarufi("client_id", "client_secret")


if __name__ == "__main__":
    response = sarufi.create_from_file(
        intents="data/intents.yaml",
        flow="data/flows.yaml",
        metadata="data/metadata.yaml",
    )
    print(response.data)
```

## Updating bot

Updating the bot is comparatively similar to creating a bot but this time you have to explicity specify the **project ID** of your bot.

```python
sarufi.update_bot(
    name="Athony bot",
    description="My bot can do a lot",
    intents={
        "salamu": ["Mambo", "Hi", "Hello", "Niaje"],
        "contact": [
            "naomba mawasiliano",
            "naomba number",
            "naomba namba",
            "nipe mawasiliano",
            "nipe contact",
        ],
    },
    flow={
        "salamu": {"message": ["Hi", "Naimani upo salama"], "next": "end"},
        "contact": {
            "message": ["Ungependa kupata namba ya nani ?"],
            "next_state": "chukua_namba",
        },
        "chukua_namba": {
            "message": ["Namba ya huyo mtu ni 07374734737", "Karibu tena !!"],
            "next_state": "end",
        },
    },
    id=2,
)
```

### Update a bot from file

You can update your bot from a file as follows;

```python
from sarufi import Sarufi

sarufi = Sarufi("client_id", "xxx")


if __name__ == "__main__":
    response = sarufi.update_from_file(
        id=5,
        intents="data/intents.yaml",
        flow="data/flows.yaml",
        metadata="data/metadata.yaml",
    )
    print(response.data)
```

## Using it in a conversation

Here you have to know the bot ID and also specify your user unique ID;

```python
>>> from sarufi import Sarufi
>>> sarufi = Sarufi('client_id', 'client_secret')
2022-08-23 18:30:32,918 - root - INFO - Getting token
>>> bots = sarufi.bots()
2022-08-23 18:30:38,223 - root - INFO - Getting bots
>>> bots
[Bot(id=4, name=iBank), Bot(id=5, name=Maria)]
>>> maria = bots[1]
>>> maria.respond('Hi')
2022-08-23 18:30:52,065 - root - INFO - Sending message to bot and returning response
2022-08-23 18:30:54,126 - root - INFO - Status code: 200
2022-08-23 18:30:54,127 - root - INFO - Message sent successfully
{'message': [['vipi uhali gani?'], ['umeshindaje?'], ['mzima wewe?'], ['Hello! u hali gani ?'], ['Freshi nambie ?'], ['Hi, mzima wewe'], ['salama sijui wewe'], ['za kwako?'], ['Vipi hali yako'], ['Uhali gani?']]}
>>> maria.respond("mi mzima wa afya")
2022-08-23 18:31:02,245 - root - INFO - Sending message to bot and returning response
2022-08-23 18:31:04,237 - root - INFO - Status code: 200
2022-08-23 18:31:04,237 - root - INFO - Message sent successfully
{'message': [['Ninafurahi kujua uko salama'], ['nimefurahi kusikia kutoka kwako'], ['Nipo salama pia, nimefurahi kusikia kutoka kwako'], ['Napenda kukuona ukiwa na furaha'], ['Nimefurahi kusikia hivyo'], ['Salama kabisa'], ['Mzima kabisa']]}
```

### Get a bot

Query a bot by ID

```python
>>> from sarufi import Sarufi
>>> sarufi = Sarufi('client_id', 'client_secret')
>>> maria= sarufi.get_bot(5)
2022-08-23 18:44:05,473 - root - INFO - Getting token
>>> maria
Bot(id=5, name=Maria)
```

## Deleting a bot

Delete a bot by ID

```python
>>> from sarufi import Sarufi
>>> sarufi = Sarufi('client_id', 'client_secret')
>>> sarufi.delete_bot(5)
```

### Issues ?

Are you facing any issue with the usage of the package, please raise one

## Contributors

1. [kalebu](https://github.com/kalebu/)
2. [Anthony Mipawa](https://github.com/Tonyloyt)
</samp>
