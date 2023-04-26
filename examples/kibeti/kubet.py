import json
from sarufi import Sarufi

sarufi = Sarufi(api_key='YOUR_API_KEY')


def create_insuarance_bot():
    response = sarufi.create_bot(
        name="Kubeti",
        description="Nakusaidia kubeti",
        intents=json.load(open("intents.json", encoding='utf-8')),
        flow=json.load(open("flow.json", encoding='utf-8')),
    )

    print(response)


def update_bot():
    response = sarufi.update_bot(
        name="Kubeti",
        description="Nakusaidia kubeti",
        intents=json.load(open("intents.json", encoding='utf-8')),
        flow=json.load(open("flow.json", encoding='utf-8')),
        id=5,
    )
    print(response)


def chat():
    while True:
        message = input("Me : ")
        response = sarufi.chat(bot_id=5, chat_id="furaha", message=message)
        print(f"Bot: {response}")


def respond(message, chat_id):
    response = sarufi.chat(bot_id=5, chat_id=chat_id, message=message)
    return response.get("message")


if __name__ == "__main__":
    # create_insuarance_bot()
    update_bot()
    chat()
