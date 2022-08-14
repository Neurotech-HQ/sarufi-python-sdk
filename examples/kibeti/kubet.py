import json
from sarufi import Sarufi

sarufi = Sarufi("kalebu@neurotech.africa", "123")


def create_insuarance_bot():
    response = sarufi.create_bot(
        project_name="Kubeti",
        description="Nakusaidia kubeti",
        training_data=json.load(open("intents.json")),
        flow=json.load(open("flow.json")),
    )

    print(response)


def update_bot():
    response = sarufi.update_bot(
        project_name="Kubeti",
        description="Nakusaidia kubeti",
        training_data=json.load(open("intents.json")),
        flow=json.load(open("flow.json")),
        project_id=5,
    )
    print(response)


def chat():
    while True:
        message = input("Me : ")
        response = sarufi.chat(project_id=5, chat_id="furaha", message=message)
        print(f"Bot: {response}")


def respond(message, chat_id):
    response = sarufi.chat(project_id=5, chat_id=chat_id, message=message)
    return response.get("message")


if __name__ == "__main__":
    # create_insuarance_bot()
    update_bot()
    chat()
