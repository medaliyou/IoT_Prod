import asyncio
import hashlib
import logging
import time

from common.Defines import *
from common.X import X, XOps
from common.base_logger import logger
from stubs.HGW import cHGWClient
from stubs.RA import RA_Client, cRAClient


class MU:
    def __init__(self):
        self.registration_state = None
        self.RN_MU: X = None
        self.r_MU: X = None
        self.PID_MU: X = None
        self.RID_MU: X = None
        self.ID_MU: X = None
        self.K_G_MU: X = None
        self.HPW_MU: X = None
        self.PW_MU: X = None

        self.S1: dict = None
        self.S4: dict = None

        self.A4: X = None
        self.A3: X = None
        self.A2: X = None
        self.A1: X = None

    def __generate_r(self):
        self.r_MU = X(s=S_RANDOM_NUMBER)  # 128 bits Random Number

    def __generate_RN(self):
        self.RN_MU = X(s=X.S_RANDOM_NONCE)

    def __compute_PID(self):
        """
        Computes PID MU = h( ID MU ||r MU )
        :return:
        """
        self.PID_MU = XOps.hash(self.ID_MU + self.r_MU)

    def __parse_credentials(self, ID, PW) -> (X, X):
        hf = hashlib.sha256(ID.encode("UTF-8"))
        _ID_MU = hf.hexdigest()[:S_ID]
        hf = hashlib.sha256(PW.encode("UTF-8"))
        _PW_MU = hf.hexdigest()[:S_PASSWORD]
        return X(h=_ID_MU), X(h=_PW_MU)

    async def init_phase(self, ID_MU, PW_MU) -> None:
        # _RA_Client = await cRAClient()
        # response = await _RA_Client.GetID()
        # if response is not None:
        self.ID_MU, self.PW_MU = self.__parse_credentials(ID_MU, PW_MU)
        self.__generate_r()
        self.__compute_PID()
        logger.info("ID_MU={}".format(self.ID_MU.h))

    async def register_phase(self) -> None:
        _RA_Client = await cRAClient()
        response = await _RA_Client.RegisterMU(self.ID_MU.h, self.PID_MU.h)
        if response is not None:
            self.K_G_MU = X(h=response.K_G)
            self.RID_MU = X(h=response.RID)

            logger.info("RID_MU={}".format(self.RID_MU.h))
            logger.info("K_G_MU={}".format(self.K_G_MU.h))
            self.process_register_phase()

    def process_register_phase(self) -> None:
        # HPWMU = h( PWMU ||r MU )
        self.HPW_MU = XOps.hash(self.PW_MU + self.r_MU)

        # A1 = r MU ⊕ h( ID MU || PWMU )
        self.A1 = self.r_MU ^ XOps.hash(self.ID_MU + self.ID_MU)

        # A2 = h( ID MU || PWMU ||r MU || HPWMU )
        self.A2 = XOps.hash(self.ID_MU + self.ID_MU + self.r_MU + self.HPW_MU)

        # A3 = RID MU ⊕ h(r MU || HPWMU )
        self.A3 = self.RID_MU ^ XOps.hash(self.r_MU + self.HPW_MU)

        # A4 = K MUG ⊕ h( RID MU || HPWMU )
        self.A4 = self.K_G_MU ^ XOps.hash(self.RID_MU + self.HPW_MU)

        # Stores { A1 , A2 , A3 , A4 , PID MU } in the mobile device
        self.registration_state = {
            "A1": self.A1,
            "A2": self.A2,
            "A3": self.A3,
            "A4": self.A4,
            "PID": self.PID_MU
        }

        logger.warning(self.registration_state)

    async def auth_KE_phase(self, ID_MU, PW_MU, PID_SD):
        await self.__auth_KE_S1(ID_MU, PW_MU, PID_SD)
        await self.__auth_KE_S5()

    async def __auth_KE_S1(self, ID_MU, PW_MU, PID_SD):
        _ID_MU, _PW_MU = self.__parse_credentials(ID_MU, PW_MU)
        # Computes
        #   r MU = A1 ⊕ h( ID MU || PWMU )
        _r_MU = self.registration_state["A1"] ^ XOps.hash(_ID_MU + _PW_MU)
        #   HPWMU = h( PWMU ||r MU )
        _HPW = XOps.hash(_PW_MU + _r_MU)

        #   A2∗ = h( ID MU || PWMU ||r MU || HPWMU )
        _A2_star = XOps.hash(_ID_MU + _PW_MU + _r_MU + _HPW)

        logger.info("Checks A2∗ = A2")
        logger.info("A2*: {}".format(_A2_star))
        logger.info("A2: {}".format(self.registration_state["A2"]))

        # Checks A2∗ = A2
        if _A2_star != self.registration_state["A2"]:
            # Verification not successful
            logger.warning("A2* != A2")
            return

        # Indicate to Backend that Registration Was OK
        # and continue calculation

        # Generates RNMU
        self.__generate_RN()
        # Computes
        # RID MU = A3 ⊕ h(r MU || HPWMU )
        _RID_MU = self.registration_state["A3"] ^ XOps.hash(_r_MU + _HPW)
        # K MUG = A4 ⊕ h( RID MU || HPWMU )
        _K_G_MU = self.registration_state["A4"] ^ XOps.hash(_RID_MU + _HPW)

        # M1 = h( PID MU || RID MU ||K MUG ) ⊕ ( RNMU || PIDSD )
        _M1 = XOps.hash(self.PID_MU + _RID_MU + _K_G_MU) ^ (self.RN_MU + PID_SD)

        # C1 = h( ID MU || RNMU ) ⊕ h(K MUG || RNMU )
        _C1 = XOps.hash(ID_MU + self.RN_MU) ^ XOps.hash(_K_G_MU + self.RN_MU)

        # VMU = h( PID MU || RID MU || RNMU || PIDSD ||K MUG )
        _V_MU = XOps.hash(self.PID_MU + _RID_MU + self.RN_MU + PID_SD + _K_G_MU)

        '''
            Save the Objects context from the S1 State         
        '''
        self.S1 = {
            "PID_MU": self.PID_MU,
            "HPW_MU": _HPW,
            "r_MU": _r_MU,
            "M1": _M1,
            "C1": _C1,
            "V": _V_MU
        }
        logger.debug(self.S1)

        _HGW_Client = await cHGWClient()
        response = await _HGW_Client.AuthKES1(PID_MU=self.PID_MU.h, M1=_M1.h, C1=_C1.h, V_MU=_V_MU.h)
        _M5 = X(h=response.M5)
        _V_G_SD = X(h=response.V_G)
        self.S4 = {
            "M5": _M5,
            "V_G_SD": _V_G_SD
        }
        logger.debug(self.S4)

    async def __auth_KE_S5(self):

        logger.debug(self.S1)
        # RID MU is needed , so get it from S1
        _RID_MU = self.S1["RID_MU"]
        _K_G_MU = self.S1["K_G_MU"]
        _HPW_MU = self.S1["K_G_MU"]
        _r_MU = self.S1["r_MU"]
        _V_G_SD = self.S4["V_G_SD"]
        _M5 = self.S4["_M5"]

        try:
            # Computes
            # PID new MU = h ( PID MU || RNMU )
            _PID_MU_new = XOps.hash(self.PID_MU + self.RN_MU)
            # (h( IDG || RNG )||h( IDSD || RNSD )|| PID new MU ) = M5 ⊕ h ( RID MU || RNMU )
            hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new = _M5 ^ XOps.hash(_RID_MU + self.RN_MU)
            # Fucking Extract  h( IDG || RNG )||h( IDSD || RNSD ) from hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new
            _len = hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new.s
            hash_IDG_RNG_c_hash_IDSD_RNSD = X(b=hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new.b[: _len - _PID_MU_new.s])

            # VGSD *  = h( PID MU || RNMU ||h( IDG || RNG )||h( IDSD || RNSD )|| PID new MU || K MUG )
            _V_G_SD_star = XOps.hash(self.PID_MU + self.RN_MU + hash_IDG_RNG_c_hash_IDSD_RNSD_c_PIDMU_new + _K_G_MU)
            # Checks VGSD * = VGSD ?

            if _V_G_SD_star != _V_G_SD:
                # Verification not successful
                return

            # Indicate to Backend that Registration Was OK
            # and continue calculation

            # Computes
            # SK = h(h( ID MU || RNMU )||h( IDG || RNG )||h( IDSD || RNSD ))
            self.SK = XOps.hash(
                XOps.hash(self.ID_MU + self.RN_MU) + hash_IDG_RNG_c_hash_IDSD_RNSD
            )
            logger.warning("\n[SESSION KEY]={}".format(self.SK))
            # Updates
            # RID new MU = h ( PID new MU || K MUG )
            _RID_MU_new = XOps.hash(_PID_MU_new + _K_G_MU)
            # A3 new = RID new MU ⊕ h (r MU || HPWMU )
            _A3_new = _RID_MU_new ^ XOps.hash(_r_MU + _HPW_MU)

            # A4 new = K MUG ⊕ h( RID new  MU || HPWMU )
            _A4_new = _K_G_MU ^ XOps.hash(_RID_MU_new + _HPW_MU)

            # Replaces { A3 , A4 , PID MU } to { A3new , A4new , PID new  MU } in the mobile device
            logger.info("Updating Registration State ...")
            logger.info("Previous\n")
            logger.info(self.registration_state)

            # reg_state = self.__load_registration_state()
            self.registration_state["A3"] = _A3_new.h
            self.registration_state["A4"] = _A4_new.h
            self.registration_state["PID"] = _PID_MU_new.h
            # self.__save_registration_state(reg_state)
            # self.registration_state = reg_state

            logger.info("New\n")
            logger.info(self.registration_state)

            # Computes
            # M6 = h(SK || PID MU new)
            _M6 = XOps.hash(self.SK + _PID_MU_new)

            _HGW_Client = await cHGWClient()
            auth_KE_S5_message = {"M6": _M6.h, "PID": self.PID_MU.h}
            # Send { M6 } to HGW
            response = await _HGW_Client.AuthKES6(M6=_M6.h, PID_MU=self.PID_MU)
            logger.debug(response.status)

        except Exception as e:
            logger.error(e)
            # self.put_nowait_auth_queue_s(False)


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
