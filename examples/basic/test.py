import sys
from uuid import uuid4
from sarufi import Sarufi

# initialize the bot
sarufi = Sarufi("kalebu@neurotech.africa", "123")


def update_bot():
    sarufi.update_bot(
        id=4,
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


def chat(bot_id: int):
    chat_id = str(uuid4())
    while True:
        message = input("Me : ")
        response = sarufi.chat(
            bot_id=bot_id,
            chat_id=chat_id,
            message=message,
            channel="whatsapp",
            message_type="text",
        )
        print(f"Bot: {response}")


if __name__ == "__main__":
    # updae_bot()
    # Get bot id from system arguments
    bot_id = sys.argv[1]
    bot_id = int(bot_id) if bot_id.isdigit() else 1
    print(f"bot id: {bot_id}")
    chat(bot_id=bot_id)
