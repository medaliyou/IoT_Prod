import asyncio
import hashlib

from common.Defines import *
from common.X import X, XOps
from common.base_logger import logger
from database.MU_Obj import update_MU_by_PID
from stubs.HGW import cHGWClient
from stubs.RA import cRAClient


def parse_credentials(ID, PW) -> (X, X):
    hf = hashlib.sha256(ID.encode("UTF-8"))
    _ID_MU = hf.digest()[:S_ID]
    hf = hashlib.sha256(PW.encode("UTF-8"))
    _PW_MU = hf.digest()[:S_PASSWORD]
    return X(b=_ID_MU), X(b=_PW_MU)


class MU:
    def __init__(self, TAG_MU: str = None):
        self.TAG_MU = TAG_MU

        self.ID_MU: X = None
        self.PW_MU: X = None

        self.PID_MU: X = None
        self.RID_MU: X = None
        self.PID_MU_new: X = None
        self.RID_MU_new: X = None
        self.PID_MU_old: X = None

        self.K_G_MU: X = None

        self.RN_MU: X = None
        self.r_MU: X = None
        self.HPW_MU: X = None

        self.A4: X = None
        self.A3: X = None
        self.A2: X = None
        self.A1: X = None
        # Targeted Smart Device SD
        self.PID_SD: X = None
        # Auth S1
        self.M1: X = None
        self.C1: X = None
        self.V_MU: X = None
        # Auth S5
        self.M5: X = None
        self.V_G_SD: X = None
        # Auth S6
        self.M6: X = None

        # Session Key
        self.SK: X = None

    def export_dict(self):
        _dict = self.__dict__.copy()
        _masked_keys = ["TAG_MU"]

        # print("*" * 100)
        # print("export_dict")
        # print("*" * 100)

        # print("self.__dict__", _dict)
        # print("*" * 100)

        try:
            for k in _dict:
                # logger.info("{}={}".format(k, _dict[k]))
                if k not in _masked_keys:
                    if isinstance(_dict[k], X):
                        _dict[k] = _dict[k].h

            # print("_dict", _dict)

            return _dict

        except Exception as e:
            logger.error(e)

    def import_dict(self, dict_obj):
        # print("*" * 100)
        # print("import_dict")
        # print("*" * 100)
        # print("dict_obj", dict_obj)
        _dict = {}
        _masked_keys = ["TAG_MU"]
        try:
            for k in dict_obj:
                # logger.warning("{} = {}".format(k, dict_obj[k]))
                if k not in _masked_keys:
                    # if isinstance(dict_obj[k], X):
                    if dict_obj[k] is not None:
                        _dict[k] = X(h=dict_obj[k])
                    else:
                        _dict[k] = None

                else:
                    _dict[k] = dict_obj[k]

            # print("_dict", _dict)

            self.__dict__.update(_dict)
            # print("self.__dict__", self.__dict__)

            # print("*" * 100)
        except Exception as e:
            logger.error(e)
            logger.error("dict key {}".format(k))

    def __generate_r(self):
        self.r_MU = X(s=S_RANDOM_NUMBER)  # 128 bits Random Number
        logger.info("self.r_MU = {}".format(self.r_MU))

    def __generate_RN(self):
        self.RN_MU = X(s=X.S_RANDOM_NONCE)
        logger.info("self.RN_MU = {}".format(self.RN_MU))

    def __compute_PID(self):
        """
        Computes PID MU = h( ID MU ||r MU )
        :return:
        """
        self.PID_MU = XOps.hash(self.ID_MU + self.r_MU)

    async def init_phase(self, ID_MU_str, PW_MU_str) -> None:
        # _RA_Client = await cRAClient()
        # response = await _RA_Client.GetID()
        # if response is not None:
        self.ID_MU, self.PW_MU = parse_credentials(ID_MU_str, PW_MU_str)
        self.__generate_r()
        self.__compute_PID()

    async def register_phase(self) -> None:
        _RA_Client = await cRAClient()
        response = await _RA_Client.RegisterMU(self.ID_MU.h, self.PID_MU.h)
        if response is not None:
            self.K_G_MU = X(h=response.K_G)
            self.RID_MU = X(h=response.RID)

            logger.info("RID_MU = {}".format(self.RID_MU))
            logger.info("K_G_MU = {}".format(self.K_G_MU))
            self.process_register_phase()

    def process_register_phase(self) -> None:
        # HPWMU = h( PWMU ||r MU )
        self.HPW_MU = XOps.hash(self.PW_MU + self.r_MU)

        # A1 = r MU ⊕ h( ID MU || PWMU )
        self.A1 = self.r_MU ^ XOps.hash(self.ID_MU + self.PW_MU)

        # A2 = h( ID MU || PWMU ||r MU || HPWMU )
        self.A2 = XOps.hash(self.ID_MU + self.PW_MU + self.r_MU + self.HPW_MU)

        # A3 = RID MU ⊕ h(r MU || HPWMU )
        self.A3 = self.RID_MU ^ XOps.hash(self.r_MU + self.HPW_MU)

        # A4 = K MUG ⊕ h( RID MU || HPWMU )
        self.A4 = self.K_G_MU ^ XOps.hash(self.RID_MU + self.HPW_MU)

        # Stores { A1 , A2 , A3 , A4 , PID MU } in the mobile device
        registration_state = {
            "A1": self.A1,
            "A2": self.A2,
            "A3": self.A3,
            "A4": self.A4,
            "PID": self.PID_MU
        }

        logger.warning(registration_state)

    async def auth_KE_phase(self, ID_MU, PW_MU, PID_SD) -> ErrorModel:
        ret = await self.__auth_KE_S1(ID_MU, PW_MU, PID_SD)
        if ret.err_no != 0:
            return ret
        return await self.__auth_KE_S5()

    async def __auth_KE_S1(self, ID_MU, PW_MU, PID_SD):
        try:

            # _ID_MU, _PW_MU = parse_credentials(ID_MU, PW_MU)
            _ID_MU, _PW_MU = X(h=ID_MU), X(h=PW_MU)
            self.PID_SD = X(h=PID_SD)
            # Computes
            #   r MU = A1 ⊕ h( ID MU || PWMU )
            _r_MU = self.A1 ^ XOps.hash(_ID_MU + _PW_MU)
            #   HPWMU = h( PWMU ||r MU )
            _HPW = XOps.hash(_PW_MU + _r_MU)
            #
            # print("A1", self.A1)
            # print("_ID_MU", _ID_MU)
            # print("_PW_MU", _PW_MU)
            # print("_r_MU", _r_MU)
            # print("r_MU", self.r_MU)
            # print("_HPW", _HPW)

            #   A2∗ = h( ID MU || PWMU ||r MU || HPWMU )
            _A2_star = XOps.hash(_ID_MU + _PW_MU + _r_MU + _HPW)

            logger.info("Checks A2∗ = A2")
            logger.info("A2*: {}".format(_A2_star))
            logger.info("A2: {}".format(self.A2))

            # Checks A2∗ = A2
            if _A2_star != self.A2:
                # Verification not successful
                logger.warning("A2* != A2")
                return ErrorModel(1, "A2* check failed")

            # return ErrorModel(0, "A2* check Success")

            # Generates RNMU
            self.__generate_RN()
            # Computes
            # RID MU = A3 ⊕ h(r MU || HPWMU )
            _RID_MU = self.A3 ^ XOps.hash(_r_MU + _HPW)
            # print("_RID_MU", _RID_MU)
            # K MUG = A4 ⊕ h( RID MU || HPWMU )
            self.K_G_MU = self.A4 ^ XOps.hash(_RID_MU + _HPW)
            # print("self.K_G_MU", self.K_G_MU)

            # M1 = h( PID MU || RID MU ||K MUG ) ⊕ ( RNMU || PIDSD )
            self.M1 = XOps.hash(self.PID_MU + _RID_MU + self.K_G_MU) ^ (self.RN_MU + self.PID_SD)
            # print("self.M1", self.M1)

            # C1 = h( ID MU || RNMU ) ⊕ h(K MUG || RNMU )
            self.C1 = XOps.hash(_ID_MU + self.RN_MU) ^ XOps.hash(self.K_G_MU + self.RN_MU)
            # print("self.C1", self.C1)

            # VMU = h( PID MU || RID MU || RNMU || PIDSD ||K MUG )
            self.V_MU = XOps.hash(self.PID_MU + _RID_MU + self.RN_MU + self.PID_SD + self.K_G_MU)
            # print("self.V_MU", self.V_MU)

            '''
                Save the Objects context from the S1 State         
            '''
            S1 = {
                "PID_SD": self.PID_MU,
                "HPW_MU": _HPW,
                "r_MU": _r_MU,
                "M1": self.M1,
                "C1": self.C1,
                "V": self.V_MU
            }
            logger.debug(S1)

            _HGW_Client = await cHGWClient()
            response = await _HGW_Client.AuthKES1(PID_MU=self.PID_MU.h, M1=self.M1.h, C1=self.C1.h, V_MU=self.V_MU.h)
            if response is not None:
                self.M5 = X(h=response.M5)
                self.V_G_SD = X(h=response.V_G)
                S4 = {
                    "M5": self.M5,
                    "V_G_SD": self.V_G_SD
                }
                logger.debug(S4)
                return ErrorModel(0, "Auth & Key Exchange S1 OK")
                # return self.M5, self.V_G_SD

            return ErrorModel(1, "Got Empty Response")

        except Exception as e:
            logger.error(e)
            return ErrorModel(1, e)

    async def __auth_KE_S5(self):

        # RID MU is needed , so get it from S1
        # _RID_MU = self.S1["RID_MU"]
        # _K_G_MU = self.S1["K_G_MU"]
        # _HPW_MU = self.S1["K_G_MU"]
        # _r_MU = self.S1["r_MU"]
        # _V_G_MU = self.S4["V_G_MU"]
        # _M5 = self.S4["_M5"]

        try:
            # Computes
            # PID new MU = h ( PID MU || RNMU )
            self.PID_MU_new = XOps.hash(self.PID_MU + self.RN_MU)
            logger.warning("self.PID_MU_new = {}".format(self.PID_MU_new))
            # (h( IDG || RNG )||h( IDSD || RNSD )|| PID new MU ) = M5 ⊕ h ( RID MU || RNMU )
            hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new = self.M5 ^ XOps.hash(self.RID_MU + self.RN_MU)
            # Fucking Extract  h( IDG || RNG )||h( IDSD || RNSD ) from hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new
            _len = hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new.s
            hash_IDG_RNG_c_hash_IDSD_RNSD = X(b=hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new.b[: _len - self.PID_MU_new.s])

            # VGSD *  = h( PID MU || RNMU ||h( IDG || RNG )||h( IDSD || RNSD )|| PID new MU || K MUG )
            _V_G_SD_star = XOps.hash(self.PID_MU + self.RN_MU + hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new + self.K_G_MU)
            # Checks VGSD * = VGSD ?

            if _V_G_SD_star != self.V_G_SD:
                # Verification not successful
                logger.warning("V_G_SD* != V_G_SD")
                return ErrorModel(1, "V_G_SD* != V_G_SD")

            # Indicate to Backend that Registration Was OK
            # and continue calculation
            # return ErrorModel(0, "V_G_SD* = V_G_SD")

            # Computes
            # SK = h(h( ID MU || RNMU )||h( IDG || RNG )||h( IDSD || RNSD ))
            self.SK = XOps.hash(
                XOps.hash(self.ID_MU + self.RN_MU) + hash_IDG_RNG_c_hash_IDSD_RNSD
            )
            logger.warning("\n[SESSION KEY]={}".format(self.SK))
            # Updates
            # RID new MU = h ( PID new MU || K MUG )
            self.RID_MU_new = XOps.hash(self.PID_MU_new + self.K_G_MU)
            # A3 new = RID new MU ⊕ h (r MU || HPWMU )
            _A3_new = self.RID_MU_new ^ XOps.hash(self.r_MU + self.HPW_MU)

            # A4 new = K MUG ⊕ h( RID new  MU || HPWMU )
            _A4_new = self.K_G_MU ^ XOps.hash(self.RID_MU_new + self.HPW_MU)

            # Replaces { A3 , A4 , PID MU } to { A3new , A4new , PID new  MU } in the mobile device
            logger.info("Updating Registration State ...")

            logger.info("Previous\n")
            logger.info("A3: {}".format(self.A3))
            logger.info("A4: {}".format(self.A4))
            logger.info("PID_MU: {}".format(self.PID_MU))
            logger.info("RID_MU: {}".format(self.RID_MU))

            """ Replacement """

            self.A3 = _A3_new
            self.A4 = _A4_new
            self.PID_MU_old = self.PID_MU
            self.PID_MU = self.PID_MU_new
            self.RID_MU = self.RID_MU_new

            # result = await save(self)
            # if result:
            #     logger.warning("Saving MU Context success !")
            # else:
            #     logger.warning("Saving MU Context failed !")

            logger.info("New\n")
            logger.info("A3_new: {}".format(self.A3))
            logger.info("A4_new: {}".format(self.A4))
            logger.info("PID_MU_new: {}".format(self.PID_MU))

            # Computes
            # M6 = h(SK || PID MU new)
            self.M6 = XOps.hash(self.SK + self.PID_MU)

            logger.info("M6 = {}".format(self.M6))
            _HGW_Client = await cHGWClient()

            # Send { M6 } to HGW
            response = await _HGW_Client.AuthKES6(M6=self.M6.h, PID_MU=self.PID_MU_old.h)
            logger.info(response)

            # Save new context
            logger.info(self.export_dict())

            result = await update_MU_by_PID(self.PID_MU_old, self.export_dict())

            if result:
                logger.warning("Updated MU Context success")
                return ErrorModel(0, str(response))

            else:
                logger.warning("Updated MU Context failed")
                return ErrorModel(1, str(response) + "\n Updated MU Context failed")

        except Exception as e:
            logger.error(e)
            return ErrorModel(1, str(e))

    async def password_update(self, ID, PW_old, PW_new):
        try:
            _ID_MU, _PW_MU_old = parse_credentials(ID, PW_old)
            # Computes
            # r MU = A1 ⊕ h( ID MU || PWMU old )
            _r_MU = self.A1 ^ XOps.hash(_ID_MU + _PW_MU_old)

            # HPWMU = h( PWMU old|| rMU )
            _HPW_MU = XOps.hash(_PW_MU_old + _r_MU)

            # A2∗ = h( ID MU || PWMU old || rMU || HPWMU )
            _A2_star = XOps.hash(_ID_MU + _PW_MU_old + _r_MU + _HPW_MU)

            # Checks A2 * = A2 ?

            logger.warning(
                "Checks A2∗ == A2"
            )
            logger.warning(
                "A2∗ = {}".format(_A2_star.h)
            )
            logger.warning(
                "A2 = {}".format(self.A2.h)
            )

            if _A2_star != self.A2:
                # Verification not successful
                logger.warning("A2* != A2")
                return ErrorModel(1, "Password Update failed! [A2* != A2]")

            _ID_MU, _PW_MU_new = parse_credentials(ID, PW_new)

            # RID MU = A3 ⊕ h(r MU || HPWMU )
            _RID_MU = self.A3 ^ XOps.hash(_r_MU + _HPW_MU)

            # K MUG = A4 ⊕ h( RID MU || HPWMU )
            _K_G_MU = self.A4 ^ XOps.hash(_RID_MU + _HPW_MU)

            # HPWMU∗∗ = h ( PWMU new ||r MU )
            _HPW_MU_star_star = XOps.hash(_PW_MU_new + _r_MU)
            # A1∗∗ = r MU ⊕ h( ID MU || PWMU new )
            _A1_star_star = _r_MU ^ XOps.hash(self.ID_MU + _PW_MU_new)
            # A2∗∗ = h( ID MU || || PWMU new || r MU || HPWMU∗∗)
            _A2_star_star = XOps.hash(self.ID_MU + _PW_MU_new + _r_MU + _HPW_MU_star_star)

            # A3** = RID MU ⊕ h(r MU || HPWMU∗∗)
            _A3_star_star = _RID_MU ^ XOps.hash(_r_MU + _HPW_MU_star_star)

            # A4** = K MUG ⊕ h( RID MU || HPWMU** )
            _A4_star_star = _K_G_MU ^ XOps.hash(_RID_MU + _HPW_MU_star_star)

            # Replaces { A1 , A2 , A3 , A4 , PID MU } with { A1∗∗ , A2∗∗ , A3∗∗ , A4∗∗ , PID MU }
            new_registration_state = {
                "A1": _A1_star_star.h,
                "A2": _A2_star_star.h,
                "A3": _A3_star_star.h,
                "A4": _A4_star_star.h,

            }
            self.A1 = _A1_star_star
            self.A2 = _A2_star_star
            self.A3 = _A3_star_star
            self.A4 = _A4_star_star
            self.HPW_MU = _HPW_MU_star_star
            self.PW_MU = _PW_MU_new

            logger.warning("Updated Password Successfully")
            logger.warning("NEW_PASSWORD={}".format(_PW_MU_new))

            # Save new context
            logger.info(self.export_dict())

            result = await update_MU_by_PID(self.PID_MU, self.export_dict())

            if result:
                logger.warning("Updated MU Context success")
                return ErrorModel(0, "Updated MU Context success")

            else:
                logger.warning("Updated MU Context failed")
                return ErrorModel(2, "Updated MU Context failed")

        except Exception as e:
            logger.error(e)
            return ErrorModel(3, str(e))


async def main(MU_Instance: MU):
    # while 1:
    await MU_Instance.init_phase("username", "password")
    await asyncio.sleep(0.001)
    await MU_Instance.register_phase()
    await MU_Instance.auth_KE_phase(
        "username",
        "password",
        "36f59919f3905e0ea44fd184a3718159da9afdc64f0dc89c250e44397a077f89"
    )

    # asyncio.sleep(0.5)


if __name__ == '__main__':
    MU = MU()
    asyncio.run(main(MU))
    # a,b = parse_credentials("username", "password")
    # print( a, b )
