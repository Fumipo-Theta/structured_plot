from typing import Tuple


def filter_dict(ref_keys):
    """
    Filter items in a dict by reference list of keys.
    """
    return lambda dictionary: dict(filter(lambda kv: kv[0] in ref_keys, dictionary.items()))


def mix_dict(target: dict, mixing: dict, consume: bool=False)->Tuple[dict, dict]:
    """
    Overwrite items by only the key in the old dict.

    assert(mix_dict(
    {
        "xlabel": {"fontsize": 12}
    },
    {
        "xlim": [0, 1],
        "xlabel": {}
    }
    ) == ({'xlabel': {'fontsize': 12}}, {'xlim': [0, 1], 'xlabel': {}}))

    """
    d = {}
    for key in target.keys():
        if type(target[key]) is dict:
            d[key] = {
                **target[key], **(mixing.pop(key, {}) if consume else mixing.get(key, {}))}
        else:
            d[key] = mixing.pop(
                key, target[key]) if consume else mixing.get(key, target[key])
    return d, mixing
