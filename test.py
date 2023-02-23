from lapi import LAPI, Wallet


node_url = 'https://arko-mn-1.lamden.io'
lapi = LAPI()

wallet = Wallet('27ae87946a3dcf563692a9ed7957401acd3ff55349d8eabd9b9b6c635ae6d6b3')

kwargs = {
    "amount": 1,
    "to": '4489524c8d7a36a488d1be063af1d89ccc57d6aabb58e75badf0f020621dd0cc'
}

tx = lapi.post_transaction(wallet, 200, contract='currency', function='transfer', kwargs=kwargs)

print('result', tx)
