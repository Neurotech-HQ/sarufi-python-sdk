<samp>

# sarufi-python-sdk

Sarufi Python SDK to help you interact with SARUFI platform

## Installation

Make sure you have [sarufi package](https://github.com/Neurotech-HQ/sarufi-python-sdk) installed on your machine before launching your telegram bot, you can easily install by the following command;

```bash
git clone https://github.com/Neurotech-HQ/sarufi-python-sdk
cd sarufi-python-sdk
sarufi-python-sdk $ python setup.py install
```

## Authentication

To authenticate you're bot, you have to specify your username and password for Sarufi Platform just as shown below;

```python
>>> from sarufi import Sarufi
>>> sarufi = Sarufi('username', 'password')
```

## Creating a Bot

To create you're bot with sarufi, you have to be aware of two importants idea or concepts which is **intents** and **flow**.

Here an example on how to create your bot;

```python
sarufi.create_bot(
    project_name="Athony bot",
    description="My bot can do a lot",
    training_data={
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
            "next": "chukua_namba",
        },
        "chukua_namba": {
            "message": ["Namba ya huyo mtu ni 07374734737", "Karibu tena !!"],
            "next": "end",
        },
    },
)
```

## Updating bot

Updating the bot is comparatively similar to creating a bot but this time you have to explicity specify the **project ID** of your bot.

```python
sarufi.update_bot(
    project_name="Athony bot",
    description="My bot can do a lot",
    training_data={
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
            "next": "chukua_namba",
        },
        "chukua_namba": {
            "message": ["Namba ya huyo mtu ni 07374734737", "Karibu tena !!"],
            "next": "end",
        },
    },
    project_id=2,
)
```

## Using it in a conversation

Here you have to know the bot ID and also specify your user unique ID;

Please also see [example 01]()

```python
>>> from sarufi import Sarufi 
>>> sarufi = Sarufi('kalebu@neurotech.africa', '123')
2022-08-14 13:32:33,070 - root - INFO - Getting token
>>> sarufi.bots()
2022-08-14 13:32:43,879 - root - INFO - Getting bots
[Bot(id=1, name=Conversational Banking, description=Help renting places over social platforms), Bot(id=2, name=Athony bot, description=My bot can do a lot), Bot(id=3, name=Tour, description=A tour guide chatot), Bot(id=4, name=Mwalimu Bank Bot, description=Manage your Mwalimu Bank account), Bot(id=5, name=Kubeti, description=Nakusaidia kubeti), Bot(id=6, name=Retail Bot, description=Manage simple customer service conversations), Bot(id=7, name=Tigo Conversational experience, description=None), Bot(id=8, name=Booking bot, description=Manage booking processes), Bot(id=9, name=Booking Bot, description=Manage booking processes)]
>>> sarufi.chat(1, 'salio langu')
2022-08-14 13:32:53,447 - root - INFO - Sending message to bot and returning response
2022-08-14 13:32:54,688 - root - INFO - Status code: 200
2022-08-14 13:32:54,688 - root - INFO - Message sent successfully
{'message': 'Salio lako ni {}', 'next_state': 'end', 'memory': {'memory_id': '10843b3e-7e9b-4988-a5d4-cc9dbb1c5506', 'data': {'view_balance': 'salio langu'}, 'created_at': '2022-08-14T10:33:00.099377', 'updated_at': '2022-08-14T10:33:00.099384'}}
>>> sarufi.chat(1, 'toa hela')
2022-08-14 13:33:07,612 - root - INFO - Sending message to bot and returning response
2022-08-14 13:33:08,692 - root - INFO - Status code: 200
2022-08-14 13:33:08,693 - root - INFO - Message sent successfully
{'message': 'Tafadhali ingiza namba ya wakala kwa usahihi.', 'next_state': 'withdraw_money_number', 'memory': {'memory_id': '960d5d9e-62ab-45ce-981a-7bd354f83e46', 'data': {'withdraw_money': 'toa hela'}, 'created_at': '2022-08-14T10:33:14.024100', 'updated_at': '2022-08-14T10:33:14.024108'}}
```

### Issues ?

Are you facing any issue with the usage of the package, please raise one

## Contributors

1. [kalebu](https://github.com/kalebu/)
2. [Anthony Mipawa](https://github.com/Tonyloyt)
</samp>
