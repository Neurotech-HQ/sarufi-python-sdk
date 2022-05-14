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
