from django.db import models
from hashlib import sha512
import random
from datetime import datetime, timedelta

KEY_SIZE = 2048


def create_key(bits=KEY_SIZE):
    rand = None
    try:
        sysrand = random.SystemRandom()
        rand = sysrand.getrandbits(bits)
    except NotImplementedError:
        rand = random.getrandbits(bits)
    assert rand is not None and rand != 0
    return "%x" % rand


def hmac_sha512(message, key):
    """Yes, this is from Wikipedia."""
    block_size = sha512().block_size
    if len(key) > block_size:
        key = sha512(key).digest()
    key = key + bytearray(block_size - len(key))
    o_key_pad = key.translate(bytearray((x ^ 0x5c) for x in range(256)))
    i_key_pad = key.translate(bytearray((x ^ 0x36) for x in range(256)))
    return sha512(o_key_pad + sha512(i_key_pad + message).digest())


def get_mac(subject, message, code, key):
    mac_key = bytearray(code.decode("hex") + key.decode("hex"))
    text = subject + message
    return hmac_sha512(text.encode("utf-8"), mac_key).hexdigest()


def get_user(name):
    honey = Destination.objects.get(name="honeypot")
    try:
        user = Destination.objects.get(name=name)
        return user
    except Destination.DoesNotExist:
        return honey


class Destination(models.Model):
    name = models.CharField(max_length=255, unique=True)
    key = models.CharField(max_length=512, default=create_key)
    email = models.CharField(max_length=255)

    def __unicode__(self):
        return u"%s <%s>" % (self.name, self.email)


class Challenge(models.Model):
    destination = models.ForeignKey(Destination)
    code = models.CharField(max_length=64, unique=True,
                            default=lambda: create_key(64))
    valid_until = models.DateTimeField(default=lambda: datetime.now() + timedelta(minutes=1))

    def __unicode__(self):
        return u"%s / %s" % (self.destination.name, self.valid_until.isoformat())
