from en import decode, encode


def format_dictionary(d: dict) -> dict:
    for k, v in d.items():
        assert type(k) == str, 'Non-string key types not allowed.'
        if type(v) == list:
            for i in range(len(v)):
                if isinstance(v[i], dict):
                    v[i] = format_dictionary(v[i])
        elif isinstance(v, dict):
            d[k] = format_dictionary(v)
    return {k: v for k, v in sorted(d.items())}


def recurse_rules(d: dict, rule: dict):
    if callable(rule):
        return rule(d)

    for key, subrule in rule.items():
        arg = d[key]

        if type(arg) == dict:
            if not recurse_rules(arg, subrule):
                return False

        elif type(arg) == list:
            for a in arg:
                if not recurse_rules(a, subrule):
                    return False

        elif callable(subrule):
            if not subrule(arg):
                return False

    return True


def dict_has_keys(d: dict, keys: set):
    key_set = set(d.keys())
    return len(keys ^ key_set) == 0


def check_format(d: dict, rule: dict):
    expected_keys = set(rule.keys())

    if not dict_has_keys(d, expected_keys):
        return False

    return recurse_rules(d, rule)


def build_tx(wallet, contract: str, function: str, kwargs: dict, nonce: int, processor: str, stamps: int):
    payload = {
        'contract': contract,
        'function': function,
        'kwargs': kwargs,
        'nonce': nonce,
        'processor': processor,
        'sender': wallet.verifying_key,
        'stamps_supplied': stamps,
    }

    payload = format_dictionary(payload)

    true_payload = encode(decode(encode(payload)))

    signature = wallet.sign(true_payload)

    metadata = {
        'signature': signature
    }

    tx = {
        'payload': payload,
        'metadata': metadata
    }

    return encode(format_dictionary(tx))
