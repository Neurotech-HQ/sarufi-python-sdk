from sarufi import Sarufi


sarufi = Sarufi('kalebu@neurotech.africa', '123')


sarufi.update_bot(
    project_name="Athony bot",
    description="My bot can do a lot",
    training_data={
        "salamu":[
            "Mambo",
            "Hi", 
            "Hello",
            "Niaje"
        ],
        "contact":[
            'naomba mawasiliano',
            'naomba number',
            'naomba namba',
            'nipe mawasiliano',
            'nipe contact'
        ]
    },
    flow={
        "salamu":{
            "message":[
                "Hi",
                "Naimani upo salama"
            ],
            "next": "end"
        },
        "contact":{
            "message":[
                "Ungependa kupata namba ya nani ?"
            ],
            "next": "chukua_namba"
        },
        "chukua_namba":{
            "message": ["Namba ya huyo mtu ni 07374734737", "Karibu tena !!"],
            "next": "end"
        }
    },
    project_id=2
)