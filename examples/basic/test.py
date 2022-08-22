import sys
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


def chat(project_id=2):
    while True:
        message = input("Me : ")
        response = sarufi.chat(project_id=project_id, chat_id="furaha", message=message)
        print(f"Bot: {response}")


if __name__ == "__main__":
    # updae_bot()
    # Get project id from system arguments
    project_id = sys.argv[1]
    project_id = int(project_id) if project_id.isdigit() else 1
    print(f"Project id: {project_id}")
    chat(project_id=project_id)


# Project id: 1
# Me : Hi
# Bot: {'message': 'Hi Karibu\nNikusaidie nini leo', 'next_state': 'end', 'memory': {'memory_id': '454e7410-003c-4699-9e43-a4fee46e7b0e', 'data': {'greetings': 'Hi'}, 'created_at': '2022-05-30T12:41:59.273215', 'updated_at': '2022-05-30T12:41:59.273222'}}
# Me : Tuma hela
# Bot: {'message': 'Tafadhali Ingiza namba ya simu ya mpokeaji.', 'next_state': 'send_money_number', 'memory': {'memory_id': 'ce9b0e14-1a73-455e-b9b2-7272f04e0394', 'data': {'send_money': 'Tuma hela'}, 'created_at': '2022-05-30T12:42:04.284956', 'updated_at': '2022-05-30T12:42:04.284963'}}
# Me : 0945884584
# Bot: {'message': 'Ungependa kutuma kiasi gani ?', 'next_state': 'send_money_amount', 'memory': {'memory_id': 'ce9b0e14-1a73-455e-b9b2-7272f04e0394', 'data': {'send_money': 'Tuma hela', 'send_money_number': '0945884584'}, 'created_at': '2022-05-30T12:42:04.284956', 'updated_at': '2022-05-30T12:42:31.255242'}}
# Me : 6000
# Bot: {'message': 'Thibitisha kutuma {} kwa {}\n1.Ndio\n2.Hapana', 'next_state': 'choice_send_money_thibitisha', 'memory': {'memory_id': 'ce9b0e14-1a73-455e-b9b2-7272f04e0394', 'data': {'send_money': 'Tuma hela', 'send_money_number': '0945884584', 'send_money_amount': '6000'}, 'created_at': '2022-05-30T12:42:04.284956', 'updated_at': '2022-05-30T12:42:36.464027'}}
# Me : 1
