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
>>> while True:
...     me = input('Me ')
...     respond = sarufi.chat(1, 'bongo', me)
...     print('you : ', respond)
... 
Me Hi
you :  {'message': 'Hi Karibu\nNikusaidie nini leo'}
Me Tuma hela
you :  {'message': 'Tafadhali Ingiza namba ya simu ya mpokeaji.'}
Me 0757294146
you :  {'message': 'Ungependa kutuma kiasi gani ?'}
Me 500
you :  {'message': 'Thibitisha kutuma {} kwa {}\n1.Ndio\n2.Hapana'}
Me 1
you :  {'message': 'Imebitishwa kutuma fedha kwa {}. imetumwa kwenda {}.\nSalio lako jipya ni {}\nKaribu tena'}
```

### Issues ?

Are you facing any issue with the usage of the package, please raise one

## Contributors

1. [kalebu](https://github.com/kalebu/)

</samp>
