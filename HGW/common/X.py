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
    print("-"*100)
    # self.M1 = XOps.hash(self.PID_MU + _RID_MU + self.K_G_MU) ^ (self.RN_MU + self.PID_SD)
    PID_SD = X(h="142c43373b932d8b8750612da81540a6671ecde8b01e0f8c3b0bfd4cc6d5b88c")
    RN_MU=X(s=16)
    y= PID_SD + RN_MU

    print("PID_SD  =", PID_SD)
    print("RN_MU   =", RN_MU)
    print("y       =",y)

    PID_MU=X(h="997435c7241ea098406795b09cd8684770ed7dd558606e6bb0ce587c07e8dbdd")
    RID_MU=X(h="010f9b0f2207c75fd0ef7741cd02b48d6f93a11b6a141f8bb494f32b44bca77e")
    K_G_MU=X(h="4939b4941088c6015b451b4cb8e61760e23388d966861bd612d7db257af443c9")
    x=XOps.hash(PID_MU+RID_MU+K_G_MU)
    print("x       =",x)
    M1=x^y
    print("M1      =",M1)
    __concat = M1 ^ XOps.hash(PID_MU + RID_MU + K_G_MU)
    print("concat  =", __concat)
    print(__concat==y)
    print("-"*100)

if __name__ == '__main__':
    X_test()
