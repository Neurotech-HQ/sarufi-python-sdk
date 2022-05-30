# sarufi-python-sdk

Sarufi Python SDK to help you interact with SARUFI platform

## Usage

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

## Creating Bot

1. Intents
2. Flow of a conversation
3. Be able to use the conversation created
4. Deploying a bot to a messaging channel
    a. Telegram
    b. WhatsApp
    c. Messenger
    d. Anywhere

## Conversational insuarance

### Intents

1. greetings (closed ended)
2. goodbye (closed ended)
3. purchase insuarance
    a. users name
    b. type insurance (1. Health, 2. Car, 3. House)
    c. amount
    d. pay now
4. update insuarance
5. revoke insuarance
    a. insuarance number
    b. reason for cancelling
    c. confirmation
