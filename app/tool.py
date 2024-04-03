import hashlib
import random
import string
from base64 import b64encode
from datetime import datetime
from decimal import Decimal
from typing import Callable, Annotated, Any

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

current_milli_time: Callable[[], str] = lambda: str(
    int((datetime.utcnow() - datetime(year=1970, month=1, day=1)).total_seconds() * 1000))
sha256_hash: Callable[[str], str] = lambda data: hashlib.sha256(data.encode()).hexdigest()
sha512_hash: Callable[[str], str] = lambda data: hashlib.sha512(data.encode()).hexdigest()
generate_random_string: Callable[[], str] = lambda: ''.join(
    random.choice(string.ascii_letters + string.digits) for _ in range(10))


def aes_128_cbc_encrypt(plain_text, key, iv):
    cipher = AES.new(bytes(key.encode("UTF-8")), AES.MODE_CBC, iv.encode("UTF-8"))
    padded_plain_text = pad(data_to_pad=plain_text.encode("UTF-8"), block_size=AES.block_size)
    encrypted = cipher.encrypt(padded_plain_text)
    return b64encode(encrypted).decode('utf-8')


def get_supply_cost(total_amount: Annotated[Any, lambda x: x.isdecimal()]) -> str:
    return str(round(Decimal(str(total_amount)) * Decimal("0.909")))


def get_tax(total_amount: Annotated[Any, lambda x: x.isdecimal()]) -> str:
    return str(round(Decimal(total_amount) * Decimal("0.091")))
