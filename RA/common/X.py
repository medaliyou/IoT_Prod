import hashlib
import random
from binascii import hexlify, unhexlify
from typing import Union

from common.base_logger import logger


class X:
    """
      A Unit X that encapsulates bytearrays of integers and supports
      hexadecimal string representation

      Attributes:

      - :class:`bytearray` b --> The bytearray of data
      - :class:`str` h --> The hexadecimal representation of b
      - :class:`int` s --> The length of b

      """
    S_KEY = S_RANDOM_NUMBER = S_RANDOM_NONCE = S_PASSWORD = S_ID = 16  # 16 Bytes <=> 128 bits

    BYTE_IN_BITS = 8
    DEFAULT_SIZE = 16  # 16 Bytes
    BYTE_ORDER = "big"

    _b: bytearray
    _h: str
    s: int

    def __init__(self, b: Union[bytes, bytearray] = None, h: str = None, s: int = None):
        # logger.warning("b={},h={},s={}".format(b, h, s))
        try:
            # b = 0 , h = 0, s = 0
            if b is None and h is None and s is None:
                self.b = random.getrandbits(self.DEFAULT_SIZE * self.BYTE_IN_BITS).to_bytes(self.DEFAULT_SIZE,
                                                                                            self.BYTE_ORDER)
                self.h = hexlify(self.b)
                self.s = self.DEFAULT_SIZE

            # b != 0 , h = 0, s = 0
            if b is not None and h is None and s is None:
                self.b = b
                self.h = hexlify(self.b)
                self.s = len(self.b)

            # b = 0 , h != 0, s = 0
            elif b is None and h is not None and s is None:
                self.b = unhexlify(h)
                self.h = h
                self.s = len(self.b)

            # b != 0 , h != 0, s = 0
            elif b is not None and h is not None and s is None:
                self.b = b
                # Check the submitted h
                _h = hexlify(self.b)
                if _h != h:
                    raise ValueError
                self.s = self.DEFAULT_SIZE
            #       ---
            # b = 0 , h = 0, s != 0
            if b is None and h is None and s is not None:
                self.b = random.getrandbits(s * self.BYTE_IN_BITS).to_bytes(s, self.BYTE_ORDER)
                self.h = hexlify(self.b)
                self.s = s

            # b != 0 , h = 0, s != 0
            if b is not None and h is None and s is not None:
                # ignore s
                self.b = b
                self.h = hexlify(self.b)
                self.s = len(b)

            # b = 0 , h != 0, s != 0
            elif b is None and h is not None and s is None:
                # ignore s
                self.h = h
                self.b = unhexlify(self.h)
                self.s = len(self.b)

            # b != 0 , h != 0, s != 0
            elif b is not None and h is not None and s is None:
                # ignore s
                self.b = b
                # Check the submitted h
                _h = hexlify(self.b)
                if _h != h:
                    raise ValueError
                self.s = self.DEFAULT_SIZE
        except Exception as e:
            logger.error("X.__init__() error={}".format(e))
            raise Exception('Bad input value')

        try:
            if not isinstance(self.h, str):
                self.h = self.h.decode()
        except Exception as e:
            logger.error("X error={}".format(e))

    # @property
    # def h(self):
    #     print("getter_h")
    #     return self.h
    # @property
    # def b(self):
    #     print("getter_b")
    #     return self.b

    def __str__(self):
        # return "\nb[{}]={}\nh[{}]={}".format(self.s, self.b, len(self.h), self.h)
        return "h[{}]={}".format(len(self.h), self.h)

    def __add__(self, other):
        """
        concatenation
        :param other:
        :return:
        """
        return X(b=self.b + other.b)

    def __eq__(self, other):
        """
        is equal to
        :param other:
        :return: boolean result
        """
        return self.b == other.b

    def __ne__(self, other):
        """
        is equal to
        :param other:
        :return: boolean result
        """
        return self.b != other.b

    # def bxor(self, b1, b2):
    #     l1 = len(b1)
    #     l2 = len(b2)
    #
    #     if l1 >= l2:
    #         result = bytearray(b1)
    #         for i, b in enumerate(b2):
    #             result[i] ^= b
    #     elif l1 < l2:
    #         result = bytearray(b2)
    #         for i, b in enumerate(b1):
    #             result[i] ^= b
    #
    #     return bytes(result)

    def bxor(self, b1, b2):
        l1 = len(b1)
        l2 = len(b2)
        print(l1, l2)
        if l1 > l2:
            _result = bytearray(b1)
            for i in range(l2):
                _result[i] ^= b1[l1 - 1 - i] ^ b2[l2 - 1 - i]
        elif l1 < l2:
            _result = bytearray(b2)
            for i in range(l1):
                _result = b1[l1 - 1 - i] ^ b2[l2 - 1 - i]
        else:
            _result = bytearray(b1)
            for i in range(l1):
                _result[i] = b1[l1 - 1 - i] ^ b2[l2 - 1 - i]
        return bytes(_result)

    def xor_op(self, b1, b2):
        l1 = len(b1)
        l2 = len(b2)

        if l1 > l2:
            b = bytes(l1 - l2)
            b += b2
            _xor = bytes([_a ^ _b for _a, _b in zip(b, b1)])
        elif l1 < l2:
            b = bytes(l2 - l1)
            b += b1
            _xor = bytes([_a ^ _b for _a, _b in zip(b, b2)])
        else:
            _xor = bytes([_a ^ _b for _a, _b in zip(b1, b2)])
        return _xor

    def __xor__(self, other):
        # if self.s >= other.s:
        #     _xor = bytes(c1 ^ c2 for c1, c2 in zip(self.b[-other.s:], other.b))
        # elif self.s < other.s:
        #     _xor = bytes(c1 ^ c2 for c1, c2 in zip(other.b[-self.s:], self.b))

        # _xor = bytes([_a ^ _b for _a, _b in zip(self.b, other.b)])

        # _xor = bytes((x ^ y for (x, y) in itertools.zip_longest(self.b, other.b, fillvalue=0)))

        # _xor = self.bxor(self.b, other.b)
        # l1 = len(self.b)
        # l2 = len(other.b)
        # padd_l = 0
        # if l1 > l2:
        #     padd_l = l1 - l2
        #     padd_b = bytearray(padd_l)
        #     padd_b += other.b
        #     _xor = self.bxor(padd_b, self.b)
        #
        # elif l1 < l2:
        #     padd_l = l2 - l1
        #     padd_b = bytearray(padd_l)
        #     padd_b += self.b
        #     _xor = self.bxor(padd_b, self.b)
        #
        # else:
        #     _xor = self.bxor(self.b, other.b)

        _xor = self.xor_op(self.b, other.b)
        _xor_left_striped = _xor.lstrip(b"\x00")
        if _xor_left_striped != _xor:
            logger.warning('Stripped {} leading zeros'.format((len(_xor) - len(_xor_left_striped))))
            _xor = _xor_left_striped

        _xor_right_striped = _xor.rstrip(b"\x00")
        if _xor_right_striped != _xor:
            logger.warning('Stripped {} tailing zeros'.format((len(_xor) - len(_xor_right_striped))))
            _xor = _xor_right_striped

        return X(b=_xor)


class XOps:
    @staticmethod
    def hash(x: X):
        _h = hashlib.sha256(x.b)
        # print("digest", _h.digest())
        # print("hexdigest", _h.hexdigest())
        return X(b=_h.digest())
        # return _h.hexdigest(), _h.digest()


def X_test():
    # print("Constructor " + "#" * 40)
    #
    # x1 = X(b=random.getrandbits(128).to_bytes(16, 'little'))
    # x2 = X(b=None, s=16)
    # # x3 = X(random.getrandbits(96).to_bytes(12, 'little'))
    # x3 = X()
    # x4 = X(h=b"8fa2de055359da51a3ab847a893a73d9")
    # x5 = X(b=b'\x8f\xa2\xde\x05SY\xdaQ\xa3\xab\x84z\x89:s\xd9')
    # x6 = X(h="8fa2de055359da51a3ab847a893a73d9")

    # print(x1)
    # print(x2)
    # print(x3)
    # print(x4)
    # print(x5)
    # print(x4 == x5)
    # print(x6 == x5)

    # Test concatenation
    # print("SUM 2 " + "#" * 40)
    #
    # print(x1 + x2)
    # print(x2 + x1)
    # print(x1 + x3)
    # print(x3 + x1)
    # print(x2 + x3)
    # print(x3 + x2)

    # print("SUM 3" + "#" * 40)
    # x_sum = x1 + x2 + x3
    # print(x_sum)
    # print("HASH " + "#" * 40)
    #
    # x_h = XOps.hash(x_sum)
    # print(x_h)
    # print("EXTRACT " + "#" * 40)

    # Extract x1 and x2 from x_c = x1 + x2
    # x_c = x1 + x2
    # print(x_c)
    # _x1 = X(x_c.b[:16])
    # _x2 = X(x_c.b[16:])
    # print(x1 == _x1)
    # print(x2 == _x2)

    # print("XOR " + "#" * 100)
    # K_RA = X(h="c808f256795fe135179584a23d5e4d26")
    # r_RA = X(h="609b8d448cecc8b3351d906b6e9230c3")
    # PID_MU = X(h="504a2765e8fd4e2d7ffff4f9c8e5c22acebaae9fc5a1b4bde9a80eedce981eac")
    # # print(x1.b)
    # # print(x2.b)
    # print(PID_MU)
    # print(K_RA)
    # print(r_RA)
    #
    # x_x = PID_MU + K_RA + r_RA
    #
    # # print(x_x)
    # K_G_MU = XOps.hash(x_x)
    # print("K_G_MU",K_G_MU)
    # x_x = PID_MU + K_G_MU
    # # print(x_x)
    # RID_MU = XOps.hash(x_x)
    # print('RID_MU',RID_MU)
    #
    # print("XOR " + "#" * 100)
    # r_MU = X(h="40b7c8a76a4bc1d56f3c87e9971358a1")
    # PW_MU = X(h="b5366826197b73c94da9fd822b10dffc")
    # HPW_MU = XOps.hash(PW_MU + r_MU)
    # print("HPW_MU",HPW_MU)
    # print("XOR " + "#" * 100)
    print("-"*100)
    IDMU = X(h="d45dd5f70f97e23d2daea562ac1975b5")
    RNMU = X(h="b9af52e602cb0d73e5d9f10a0f5f7a10")
    IDG = X(h="45b5a401ab32f1d2f5c205f7597bf9a9")
    RNG = X(h="139cb5d989ac69738742b3e3ba1bbc96")
    hashed = XOps.hash(IDMU+RNMU) + XOps.hash(IDG+RNG)
    print(hashed)
    print("-"*100)

if __name__ == '__main__':
    X_test()
