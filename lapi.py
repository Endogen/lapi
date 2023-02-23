import nacl.encoding
import nacl.signing
import secrets
import requests
import decimal

from en import decode
from typing import Union
from tx import build_tx


class Wallet:
    def __init__(self, seed=None):
        if isinstance(seed, str):
            seed = bytes.fromhex(seed)

        if seed is None:
            seed = secrets.token_bytes(32)

        self.sk = nacl.signing.SigningKey(seed=seed)
        self.vk = self.sk.verify_key

    @property
    def signing_key(self):
        return self.sk.encode().hex()

    @property
    def verifying_key(self):
        return self.vk.encode().hex()

    def sign(self, msg: str):
        sig = self.sk.sign(msg.encode())
        return sig.signature.hex()


class LAPI:

    def __init__(self, wallet: Wallet, node_url: str = None):
        self.node_url = node_url if node_url else 'https://arko-mn-1.lamden.io'
        self.wallet = wallet

    def get_nonce(self, address: str):
        with requests.get(f"{self.node_url}/nonce/{address}") as res:
            return decode(res.text)

    def post_tx(self, stamps: int, contract: str, function: str, kwargs: dict):
        nonce = self.get_nonce(self.wallet.verifying_key)

        tx = build_tx(
            wallet=self.wallet,
            processor=nonce["processor"],
            stamps=stamps,
            nonce=nonce["nonce"],
            contract=contract,
            function=function,
            kwargs=kwargs)

        with requests.post(self.node_url, data=tx) as res:
            return decode(res.text)

    def send(self, amount: Union[int, float, str], to_address: str, token: str = "currency", stamps: int = 100):
        kwargs = {"amount": decimal.Decimal(str(amount)), "to": to_address}
        return self.post_tx(stamps, token, "transfer", kwargs)
