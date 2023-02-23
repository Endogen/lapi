````python
from lapi import LAPI, Wallet

private_key = '27ae87946a3dcf563692a9ed7957401acd3ff55349d8eabd9b9b6c635ae6d29f'
wallet = Wallet(private_key)
lapi = LAPI(wallet=wallet)

tx = lapi.send(amount=1, to_address='4489524c8d7a36a488d1be063af1d89ccc57d6aabb58e75badf0f020621dd0cc')

print(tx)

kwargs = {
    "amount": 1,
    "to": '4489524c8d7a36a488d1be063af1d89ccc57d6aabb58e75badf0f020621dd0cc'
}

tx = lapi.post_tx(200, contract='currency', function='transfer', kwargs=kwargs)

print(tx)
````
